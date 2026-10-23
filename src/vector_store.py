"""Simple in-memory document store (no Pinecone)."""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


class VectorStore:
    """Simple in-memory document storage."""

    def __init__(self):
        self.documents = []
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,          # 🔥 reduced for better LLM handling
            chunk_overlap=50,
            separators=["\n\n", "\n", " ", ""]
        )

    def add_documents(self, documents: list):
        for doc in documents:
            chunks = self.text_splitter.split_text(doc['content'])

            for i, chunk in enumerate(chunks):
                self.documents.append({
                    'content': chunk,
                    'filename': doc['filename'],
                    'chunk_id': i,
                    'metadata': {
                        'source': doc['filename'],
                        'chunk': i
                    }
                })

    def get_retriever(self, k=3):
        return SimpleRetriever(self.documents, k)


class SimpleRetriever:
    """Simple retriever using keyword overlap."""

    def __init__(self, documents, k=3):
        self.documents = documents
        self.k = k

    def get_relevant_documents(self, query):
        query_words = set(query.lower().split())

        scored_docs = []
        for doc in self.documents:
            doc_words = set(doc['content'].lower().split())

            overlap = len(query_words.intersection(doc_words))
            score = overlap / len(query_words) if query_words else 0

            scored_docs.append((doc, score))

        scored_docs.sort(key=lambda x: x[1], reverse=True)
        top_docs = scored_docs[:self.k]

        return [
            Document(page_content=doc['content'], metadata=doc['metadata'])
            for doc, _ in top_docs
        ]