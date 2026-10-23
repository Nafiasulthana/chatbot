"""PDF processing module."""

from pypdf import PdfReader
from io import BytesIO


def process_pdf(uploaded_file) -> str:
    try:
        pdf_bytes = BytesIO(uploaded_file.read())
        pdf_reader = PdfReader(pdf_bytes)

        text = ""

        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        # 🔥 clean text
        text = " ".join(text.split())

        return text

    except Exception as e:
        raise Exception(f"Error processing PDF {uploaded_file.name}: {str(e)}")