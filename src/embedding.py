from typing import List, Dict
import os
import requests
from dotenv import load_dotenv
from vector_store import VectorStore, VectorStoreItem

# 自动加载.env
load_dotenv()

#嵌入检索类
class EmbeddingRetriever:
    def __init__(self, embedding_model: str):
        self.embedding_model = embedding_model     #获取嵌入模型
        self.vector_store = VectorStore()          #初始化向量存储

    #嵌入文档并添加到向量存储
    async def embed_document(self, document: str) -> List[float]:
        embedding = await self._embed(document)
        await self.vector_store.add_item(VectorStoreItem(
            embedding=embedding,
            document=document
        ))
        return embedding

    #嵌入查询
    async def embed_query(self, query: str) -> List[float]:
        embedding = await self._embed(query)
        return embedding

    #调用嵌入API
    async def _embed(self, document: str) -> List[float]:
        response = requests.post(
            f"{os.getenv('EMBEDDING_BASE_URL')}/embeddings",
            headers={
                'Content-Type': 'application/json',
                'Authorization': f"Bearer {os.getenv('EMBEDDING_KEY')}",
            },
            json={
                'model': self.embedding_model,
                'input': document,
            }
        )
        data = response.json()      #json转字典
        # print(data['data'][0]['embedding'])    #查看向量化结果
        return data['data'][0]['embedding']

    #检索最相关的文档
    async def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        query_embedding = await self.embed_query(query)
        return await self.vector_store.search(query_embedding, top_k)
