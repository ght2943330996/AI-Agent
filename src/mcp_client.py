from typing import List, Dict, Any, Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

#MCP客户端类,参见MCP文档: https://modelcontextprotocol.io/docs/develop/build-client
class MCPClient:
    def __init__(self, name: str, command: str, args: List[str], env: Optional[Dict[str, str]] = None, version: Optional[str] = None):
        self.name = name
        self.version = version or "0.0.1"
        self.command = command         # 命令行程序路径
        self.args = args             # 命令行参数列表
        self.env = env or {}         # 环境变量字典
        # self.session: Optional[ClientSession] = None
        self.tools: List[Dict[str, Any]] = []

        #用于关闭MCP客户端的上下文管理器
        self._stdio_context = None
        self._read = None
        self._write = None

    #初始化MCP客户端，连接到MCP服务器获取可用工具列表
    async def init(self):
        await self._connect_to_server()

    #关闭MCP客户端
    async def close(self):
        if self.session:
            try:
                await self.session.__aexit__(None, None, None)
            except:
                pass
        if self._stdio_context:
            try:
                await self._stdio_context.__aexit__(None, None, None)
            except:
                pass

    #获取可用工具列表
    def get_tools(self) -> List[Dict[str, Any]]:
        return self.tools

    #agent调用工具给chatopenai
    async def call_tool(self, name: str, params: Dict[str, Any]):
        if not self.session:
            raise Exception("MCP client 未初始化")
        result = await self.session.call_tool(name, arguments=params)
        return result

    #连接到MCP服务器 参见MCP文档: https://modelcontextprotocol.io/docs/develop/build-client
    async def _connect_to_server(self):
        try:
            server_params = StdioServerParameters(
                command=self.command,
                args=self.args,
                env=self.env if self.env else None
            )

            # 保存上下文管理器以便正确清理
            self._stdio_context = stdio_client(server_params)  #调用stdio_client函数
            self._read, self._write = await self._stdio_context.__aenter__()     #__aenter__ 是为了后续手动退出。

            # 创建会话
            self.session = ClientSession(self._read, self._write)
            await self.session.__aenter__()

            # 初始化会话
            await self.session.initialize()

            # 获取工具列表
            tools_result = await self.session.list_tools()
            self.tools = [
                {
                    'name': tool.name,
                    'description': tool.description,
                    'inputSchema': tool.inputSchema
                }
                for tool in tools_result.tools
            ]

            print(
                f"\n连接服务器的工具: {[tool['name'] for tool in self.tools]}"
            )
        except Exception as e:
            print(f"连接失败: {e}")
            raise e
