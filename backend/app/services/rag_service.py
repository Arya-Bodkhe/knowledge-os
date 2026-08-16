from backend.app.services.embedding_service import generate_embeddings
from backend.app.services.vector_store import search_documents
from backend.app.services.gemini_service import generate_answer


def answer_question(question: str, n_results: int = 3) -> str:
    # Convert the user's question into an embedding
    query_embedding = generate_embeddings([question])[0]

    # Retrieve the most relevant document chunks
    results = search_documents(query_embedding, n_results)

    documents = results.get("documents", [[]])[0]

    # Handle the case where no relevant documents are available
    if not documents:
        return "I could not find relevant information in the uploaded documents."

    # Combine retrieved chunks into context for Gemini
    context = "\n\n".join(documents)

    # Generate an answer using the retrieved context
    return generate_answer(question, context)