from enum import Enum


class IngestionType(str, Enum):
    epub = "epub"
    pdf = "pdf"