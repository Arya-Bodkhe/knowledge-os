import os
import tempfile

from fastapi import APIRouter, UploadFile, File

from backend.app.services.pdf_service import extract_text

router = APIRouter()


@router.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    file_extension = os.path.splitext(file.filename)[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=file_extension
    ) as temp_file:
        temp_file.write(await file.read())
        temp_path = temp_file.name

    try:
        text = extract_text(temp_path)

        return {
            "filename": file.filename,
            "characters_extracted": len(text),
            "message": "Document processed successfully."
        }

    finally:
        os.remove(temp_path)