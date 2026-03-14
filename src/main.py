import asyncio
import os
from pathlib import Path
from mcp_client import MCPClient
from agent import Agent
from embedding import EmbeddingRetriever
from util import log_title


# 获取当前工作目录
current_dir = os.getcwd()

# 初始化MCP客户端
fetch_mcp = MCPClient('fetch', 'uvx', ['mcp-server-fetch'])
file_mcp = MCPClient('file', 'npx', ['-y', '@modelcontextprotocol/server-filesystem', current_dir])


# 测试ChatOpenAI类
# async def main():
#     from chat_openai import ChatOpenAI
#     llm = ChatOpenAI('deepseek-reasoner', '你是一个智能新闻助手')    # 模型+系统提示词
#     response = await llm.chat('你好')
#     print(response['content'])
#     print(response['toolCalls'])


# 测试mcp服务
# async def main():
#     fetch_mcp = MCPClient('fetch', 'uvx', ['mcp-server-fetch'])
#     await fetch_mcp.init()
#     tools = fetch_mcp.get_tools()
#     print(tools)
#     await fetch_mcp.close()


# 测试llm+mcp
# async def main():
#     agent = Agent('deepseek-chat', [fetch_mcp, file_mcp])
#     await agent.init()
#     response = await agent.invoke(
#         f"爬取https://www.datalearner.com/leaderboards的内容,"
#         f"在{current_dir}/knowledge中，每个模型创建一个md文件保存基本信息"
#     )
#     print(response)


# llm+mcp+rag
async def main():
    # prompt = f"根据knowledge文件的模型信息,对比claude_Opus_4.5和Gemini_3.0_Pro的优缺点,并给出两个模型的具体使用场景,把结果保存到{current_dir}/test中"
    prompt = f"根据张三的信息,为他制定一个学习计划,把结果保存到{current_dir}/test中"

    context = await retrieve_context(prompt)

    # Agent    # 模型名称+系统提示词+上下文
    agent = Agent('deepseek-chat', [fetch_mcp, file_mcp], '', context)
    await agent.init()
    response = await agent.invoke(prompt)
    print(response)
    await agent.close()


# RAG检索
async def retrieve_context(prompt: str) -> str:
    embedding_retriever = EmbeddingRetriever("BAAI/bge-m3")     #嵌入模型名称
    knowledge_dir = Path(current_dir) / 'knowledge'         #RAG知识库目录

    files = list(knowledge_dir.iterdir())
    for file in files:
        if file.is_file():
            content = file.read_text(encoding='utf-8')
            await embedding_retriever.embed_document(content)

    context_results = await embedding_retriever.retrieve(prompt)
    log_title('上下文')
    print(context_results)

    return '\n'.join(item['document'] for item in context_results)


if __name__ == '__main__':
    asyncio.run(main())
