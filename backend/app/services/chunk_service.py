def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    chunks = []
    current_chunk = ""

    for line in lines:
        if len(current_chunk) + len(line) + 1 <= chunk_size:
            current_chunk += line + "\n"
        else:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())

            overlap_text = current_chunk[-overlap:] if current_chunk else ""
            current_chunk = overlap_text + line + "\n"

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks