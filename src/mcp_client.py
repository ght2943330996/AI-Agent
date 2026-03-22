from typing import List, Dict, Any, Optional
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# MCP客户端类，参见MCP文档: https://modelcontextprotocol.io/docs/develop/build-client
#
# 实现说明：
#   stdio_client 内部使用 anyio TaskGroup / CancelScope，要求从进入到退出都在
#   同一个 asyncio Task 中执行。为了支持多个 MCPClient 实例同时存活（多会话场景），
#   每个客户端在 init() 时会启动一个独立的后台 Task 来持有连接生命周期，
#   工具调用通过 asyncio.Queue 传递给该 Task 执行，从而避免跨 Task 的 scope 错误。
class MCPClient:
    def __init__(self, name: str, command: str, args: List[str],
                 env: Optional[Dict[str, str]] = None,
                 version: Optional[str] = None):
        self.name = name
        self.version = version or "0.0.1"
        self.command = command
        self.args = args
        self.env = env or {}
        self.tools: List[Dict[str, Any]] = []

        # 内部状态（由后台 Task 管理）
        self._ready_event: asyncio.Event = asyncio.Event()
        self._call_queue: asyncio.Queue = asyncio.Queue()   # (tool_name, params, Future)
        self._stop_event: asyncio.Event = asyncio.Event()
        self._bg_task: Optional[asyncio.Task] = None
        self._init_error: Optional[Exception] = None        # 连接失败时保存异常

    # ------------------------------------------------------------------
    # 公共接口
    # ------------------------------------------------------------------

    async def init(self):
        # await self._connect_to_server()

        """启动后台 Task，连接 MCP 服务器并获取工具列表。"""
        self._bg_task = asyncio.create_task(
            self._run(), name=f'mcp-{self.name}'
        )
        # 等待连接就绪（或失败）
        await self._ready_event.wait()
        if self._init_error:
            raise self._init_error

    async def close(self):
        """通知后台 Task 退出，等待其结束。"""
        self._stop_event.set()
        if self._bg_task and not self._bg_task.done():
            try:
                await asyncio.wait_for(self._bg_task, timeout=5)
            except (asyncio.TimeoutError, asyncio.CancelledError, Exception):
                self._bg_task.cancel()
                try:
                    await self._bg_task
                except Exception:
                    pass

    def get_tools(self) -> List[Dict[str, Any]]:
        return self.tools
    #用于agent调用工具，返回工具执行结果
    async def call_tool(self, name: str, params: Dict[str, Any]) -> Any:
        """在后台 Task 中执行工具调用，通过 Future 返回结果。"""
        if not self._ready_event.is_set() or self._init_error:
            raise Exception("MCP client 未初始化")
        loop = asyncio.get_event_loop()
        future: asyncio.Future = loop.create_future()
        await self._call_queue.put((name, params, future))
        return await future

    # ------------------------------------------------------------------
    # 后台 Task：持有完整的 stdio_client / ClientSession 生命周期
    # ------------------------------------------------------------------

    #连接到MCP服务器 参见MCP文档: https://modelcontextprotocol.io/docs/develop/build-client
    async def _run(self):
        server_params = StdioServerParameters(
            command=self.command,
            args=self.args,
            env=self.env if self.env else None,
        )
        try:
            async with stdio_client(server_params) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()

                    tools_result = await session.list_tools()
                    self.tools = [
                        {
                            'name': tool.name,
                            'description': tool.description,
                            'inputSchema': tool.inputSchema,
                        }
                        for tool in tools_result.tools
                    ]
                    print(f"连接服务器的工具: {[t['name'] for t in self.tools]}")

                    # 标记就绪，唤醒 init() 的等待
                    self._ready_event.set()

                    # 持续处理工具调用请求，直到收到停止信号
                    while not self._stop_event.is_set():
                        try:
                            name, params, future = await asyncio.wait_for(
                                self._call_queue.get(), timeout=0.5
                            )
                        except asyncio.TimeoutError:
                            continue

                        try:
                            result = await session.call_tool(name, arguments=params)
                            if not future.done():
                                future.set_result(result)
                        except Exception as e:
                            if not future.done():
                                future.set_exception(e)

        except Exception as e:
            self._init_error = e
            self._ready_event.set()   # 解除 init() 的阻塞，让它抛出异常
            print(f"连接失败: {e}")
