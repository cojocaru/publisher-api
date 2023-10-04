from dotenv import load_dotenv
import openai
from config import settings

from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

def setup():
    # Load environment variables
    load_dotenv()
    
    # Set OpenAI API Key
    openai.api_key = settings.OPENAI_API_KEY
    
    loader = DirectoryLoader('documents', glob="**/*.txt", loader_cls=TextLoader)
    raw_documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(raw_documents)
    
    db = FAISS.from_documents(documents, OpenAIEmbeddings())
    
    return db

def rag_augmented_prompt(db, query: str, days, network):
    # get top 3 results from knowledge base
    results = db.similarity_search(query, k=days)
    
    # get the text from the results
    source_knowledge = "\n".join([x.page_content for x in results])

    augmented_prompt = f"""Given the following content,
    
    please generate a list of {days} {network} posts
    
    that would resonate with an audience interested in these topics.
    
    Content: {source_knowledge}"""
    
    # feed into an augmented prompt
    # augmented_prompt = f"""Using the contexts below, answer the query.

    # Contexts:
    # {source_knowledge}

    # Query: {query}"""
    return augmented_prompt

# This part runs only if the script is executed directly
if __name__ == "__main__":
    db = setup()
    query = "What means enshrining?"
    print(rag_augmented_prompt(db, query))
