from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_pages(pages: List[str], chunk_size: int = 700, overlap: int = 80) -> List[str]:
    """
    Chunks the list of pages into smaller pieces using RecursiveCharacterTextSplitter.

    :param pages: List of strings, where each string is the text of a page.
    :param chunk_size: The maximum size of each chunk (default 700).
    :param overlap: The number of overlapping characters between chunks (default 80).
    :return: List of chunked strings.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        length_function=len
    )
    
    full_text = "".join(pages)
    chunks = text_splitter.split_text(full_text)
    return chunks
