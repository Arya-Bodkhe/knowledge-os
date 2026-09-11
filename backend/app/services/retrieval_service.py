import re

from backend.app.services.embedding_service import generate_embeddings
from backend.app.services.vector_store import collection


STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for",
    "from", "how", "in", "is", "it", "of", "on", "or", "that",
    "the", "this", "to", "was", "what", "when", "where", "which",
    "who", "why", "with"
}


def _tokenize(text: str) -> set[str]:
    words = re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())
    return {word for word in words if word not in STOP_WORDS}


def _keyword_score(query: str, document: str) -> float:
    query_terms = _tokenize(query)
    document_terms = _tokenize(document)

    if not query_terms:
        return 0.0

    matches = query_terms.intersection(document_terms)

    return len(matches) / len(query_terms)


def _section_bonus(query: str, document: str) -> float:
    query_terms = _tokenize(query)
    first_lines = document.strip().splitlines()[:3]

    heading_text = " ".join(first_lines).lower()

    section_terms = {
        "aim",
        "objective",
        "conclusion",
        "introduction",
        "problem",
        "methodology",
        "result",
        "discussion"
    }

    matched_sections = query_terms.intersection(section_terms)

    if not matched_sections:
        return 0.0

    return sum(
        1.0
        for term in matched_sections
        if re.search(rf"\b{term}\s*:", heading_text)
    )


def retrieve_documents(query: str, n_results: int = 3):
    query_embedding = generate_embeddings([query])[0]

    candidate_count = max(n_results * 5, 10)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=candidate_count,
        include=["documents", "metadatas", "distances"]
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    candidates = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):
        semantic_score = 1 / (1 + distance)
        keyword_score = _keyword_score(query, document)
        section_bonus = _section_bonus(query, document)

        final_score = (
            0.60 * semantic_score
            + 0.30 * keyword_score
            + 0.10 * section_bonus
        )

        candidates.append({
            "document": document,
            "metadata": metadata,
            "distance": distance,
            "semantic_score": semantic_score,
            "keyword_score": keyword_score,
            "score": final_score,
        })

    candidates.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return candidates[:n_results]