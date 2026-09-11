import uuid
import chromadb


client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="knowledge_os"
)


def add_documents(
    chunks: list[str],
    embeddings: list[list[float]],
    document_name: str
):
    ids = [str(uuid.uuid4()) for _ in chunks]

    metadatas = [
        {
            "document": document_name,
            "chunk_index": i
        }
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )


def search_documents(
    query_embedding: list[float],
    n_results: int = 3
):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )

    return results