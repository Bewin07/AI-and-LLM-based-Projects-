from pdfreader import read_pdf
from chunker import chunk_pages
from embedder import embed_chunks
from vectorstore import store_in_pinecone
from typing import List

pdf_path =r"resources\Attention is all u need new.pdf"
def run(pdf_path=r"resources\Attention is all u need new.pdf"):
    # Read HR Policy PDF and extract text
    pages = read_pdf(pdf_path)

    # Chunk the data into smaller pieces
    chunks = chunk_pages(pages)

    # # Embed the chunks using OpenAI's embedding model to create vector representations
    embedded_chunks = embed_chunks(chunks)

    # # Store the chunks and their embeddings in Pinecone vector database
    store_in_pinecone(chunks, embedded_chunks)
    # print(len(embedded_chunks))
    # print(embedded_chunks[0])
    
if __name__ == "__main__":
    run()