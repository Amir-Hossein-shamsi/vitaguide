import os
from dotenv import load_dotenv
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore

# Custom function to load documents with specified encoding
def load_documents(directory, encoding='utf-8'):
    documents = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, 'r', encoding=encoding) as file:
                text = file.read()
                documents.append(Document(page_content=text, metadata={"source": filepath}))
        except UnicodeDecodeError:
            print(f"Failed to decode {filepath} with encoding {encoding}. Trying 'latin-1'.")
            try:
                with open(filepath, 'r', encoding='latin-1') as file:
                    text = file.read()
                    documents.append(Document(page_content=text, metadata={"source": filepath}))
            except UnicodeDecodeError:
                print(f"Failed to decode {filepath} with 'latin-1'. Skipping this file.")
    return documents

def ingestion_docs():
    load_dotenv()
    
    # Load documents using the custom loader
    raw_documents = load_documents("articles")
    print(f"Loaded {len(raw_documents)} documents!")
    
    # Split the documents into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
    split_docs = text_splitter.split_documents(raw_documents)
    
    # Create embeddings for the documents
    embeddings = OllamaEmbeddings(model="nomic-embed-text:v1.5")
    
    # Update metadata for each document
    for doc in split_docs:
        new_url = doc.metadata.get("source", "")
        if new_url != '':
            doc.metadata.update({"source": new_url.replace("\\\\","").replace("articles", "https://www.fitday.com/fitness-articles/nutrition/for-men").replace("\\\\","")})
    
    # Store the embeddings in a Pinecone vector store
    vector_store = PineconeVectorStore.from_documents(
        split_docs, 
        embeddings, 
        index_name="fitday-articles"
    )
    
    return vector_store

if __name__ == '__main__':
    vector_store = ingestion_docs()
    print("**** Loading to VectorStore Done ****")