from backend.app.services.retrieval_service import retrieve_documents
from backend.app.services.gemini_service import generate_answer


def answer_question(question: str, n_results: int = 3) -> str:
    # Retrieve the most relevant document chunks
    results = retrieve_documents(question, n_results)

    # Extract document text from retrieval results
    documents = [
        result["document"]
        for result in results
    ]

    # Handle the case where no relevant documents are available
    if not documents:
        return "I could not find relevant information in the uploaded documents."

    # Combine retrieved chunks into context for Gemini
    context = "\n\n".join(documents)

    # Generate an answer using the retrieved context
    return generate_answer(question, context)