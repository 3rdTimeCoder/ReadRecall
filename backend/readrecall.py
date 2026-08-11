import click
from enum import Enum
from ingestion.ingestion_pipeline import ingest_books
from retrieval.retrieval_pipeline import recall as recall_book


class RecallAction(str, Enum):
    ingest = "ingest"
    recall = "recall" 


def prompt_user(prompt: str) -> str:
    """Prompts the user for input and returns the response.

    Args:
        prompt: The message displayed to the user.

    Returns:
        The non-empty string entered by the user.
    """
    answer = ""
    while not answer:
        answer = input(prompt)
    
    return answer


def ingest():
    """Prompts the user for a directory path and file type, then ingests the books."""
    dir = prompt_user("Please enter the directory path: ")
    type = prompt_user("Please enter the books' file type. [epub | pdf]: ")
    success = ingest_books(dir_path=dir, type=type)
    if success: click.echo(f"The books in {dir} have been successfully ingested.")
    else: click.echo("Something went wrong! Ingestion could not complete. Please try again.")


def recall():
    """Prompts the user for a query and searches the ingested library for matching books."""
    query = prompt_user("What book do you need help recalling today?\n")
    recall_book(query=query)


@click.command()
@click.option('--action', '-a', type=RecallAction, help='Choose which action to take. Ingest or Recall')
def readrecall(action):
    """
    A simple CLI tool to use ReadRecall.

    ReadRecall identifies which book you're thinking of from your personal library
    based on a vague memory fragment. Use the --action flag to either ingest books
    into the library or recall a book from memory.

    Args:
        action: The action to perform — either 'ingest' or 'recall'.
    """
    click.echo(f"Welcome to ReadRecall!")
    if action == RecallAction.ingest:
        ingest()
    elif action== RecallAction.recall:
        recall()



if __name__ == '__main__':
    readrecall()