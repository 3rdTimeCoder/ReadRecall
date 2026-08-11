from enum import Enum


class IngestionType(str, Enum):
    """Supported file types for book ingestion.

    Members:
        epub: EPUB ebook format.
        pdf: PDF document format.
    """
    epub = "epub"
    pdf = "pdf"