
# Modified from tutorial on: https://www.youtube.com/watch?v=6efwN_US-zk
import uuid
import hashlib
import os
import getpass
from typing import List, Tuple
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from rank_bm25 import BM25Okapi
from pinecone import Pinecone, ServerlessSpec
import concurrent
from openai import OpenAI
import time 

load_dotenv()

## Initialize OpenAI and Pinecone clients
openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

def get_openai_embeddings(input_data):
    response = openai_client.embeddings.create(input=input_data, 
                                               model="text-embedding-3-small")
    return response.data[0].embedding

class ContextualRetrieval:
    """
    A class that implements the Contextual Retrieval system.
    """

    def __init__(self):
        """
        Initialize the ContextualRetrieval system.
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100,
        )

        self.embeddings = get_openai_embeddings
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )

    def process_document(self, document: str, document_name="") -> Tuple[List[Document], List[Document]]:
        """
        Process a document by splitting it into chunks and generating context for each chunk.
        """

        start_time = time.time()
        chunks = self.text_splitter.create_documents([document])
        for chunk in chunks:
            chunk.metadata["document_name"] = document_name
        end_time = time.time()
        # print(f"Time taken to split document into chunks: {end_time - start_time} seconds")

        start_time = time.time()
        contextualized_chunks = self._generate_contextualized_chunks(document, chunks)
        end_time = time.time()
        # print(f"Time taken to generate contextualized chunks: {end_time - start_time} seconds")
        return chunks, contextualized_chunks

    def _generate_contextualized_chunks(self, document: str, chunks: List[Document], parallel_processes: int = 20) -> List[Document]:
        """
        Generate contextualized versions of the given chunks.
        """
        contextualized_chunks = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=parallel_processes) as executor:
            futures = []
            for chunk in chunks:
                futures.append(executor.submit(self._generate_context, document, chunk))

            for future in concurrent.futures.as_completed(futures):
                document, chunk, context = future.result()
                contextualized_content = f"{context}\n\n{chunk.page_content}"
                contextualized_chunks.append(Document(page_content=contextualized_content, metadata=chunk.metadata))
        return contextualized_chunks

    def _generate_context(self, document: str, chunk: str) -> str:
        """
        Generate context for a specific chunk using the language model.
        """
        prompt = ChatPromptTemplate.from_template("""
        <document> 
        {document} 
        </document> 
        Here is the chunk we want to situate within the whole document 
        <chunk> 
        {chunk} 
        </chunk> 
        Please give a short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval of the chunk. Answer only with the succinct context and nothing else. 
        """)
        messages = prompt.format_messages(document=document, chunk=chunk.page_content)
        response = self.llm.invoke(messages)
        return document, chunk, response.content

    def create_bm25_index(self, chunks: List[Document]) -> BM25Okapi:
        """
        Create a BM25 index for the given chunks.
        """
        tokenized_chunks = [chunk.page_content.split() for chunk in chunks]
        return BM25Okapi(tokenized_chunks)
    
    def parallel_upsert(self, index, vectors):
        """
        Upsert vectors into a Pinecone index in parallel.
        """
        index.upsert(vectors=vectors)

    def get_parallel_embeddings(self, i, chunk):
        # add a uuid as well 
        uuid_id = str(uuid.uuid4())
        id = f"{chunk.metadata['document_name']}_{i}_{uuid_id}"
        output = self.embeddings(chunk.page_content)
        metadata = {
            "text": chunk.page_content,
            "document_name": chunk.metadata.get("document_name")
        }
        return {"id": id, "values": output, "metadata": metadata}

    def create_pinecone_index(self, index_name: str, chunks: List[Document]):
        """
        Create a Pinecone index for the given chunks.
        """
        # Check if the index already exists
        if index_name not in pc.list_indexes().names():
            # Create a new index
            pc.create_index(
                index_name,
                dimension=len(self.embeddings(chunks[0].page_content)),
                spec=ServerlessSpec(
                    cloud="aws",
                    region=os.getenv("PINECONE_REGION"),
                ),
            )

        else: 
            print(f"Index {index_name} already exists")
        # Connect to the index
        index = pc.Index(index_name)

        finalized_vectors = []
        # Prepare data for upsert
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(self.get_parallel_embeddings, i, chunk) for i, chunk in enumerate(chunks)]
            
            for future in concurrent.futures.as_completed(futures):
                finalized_vectors.append(future.result())

        finalized_vectors = sorted(finalized_vectors, key=lambda x: x['id'])
        # for i in range(len(vectors)):
        #     print(vectors[i])

        # Upsert data into the index in batches and in parallel
        batch_size = 100
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for i in range(0, len(finalized_vectors), batch_size):
                print(f"Upserting batch {i//batch_size + 1} of {len(finalized_vectors)//batch_size + 1}")
                batch = finalized_vectors[i:i + batch_size]
                futures.append(executor.submit(self.parallel_upsert, index, batch))
            for future in concurrent.futures.as_completed(futures):
                pass # basically just wait for all the threads to finish

    def query_pinecone_index(self, index_name: str, query: str, top_k: int = 3, include_values: bool = True, include_metadata: bool = True):
        """
        Query a Pinecone index.
        """
        index = pc.Index(index_name)
        query_vector = self.embeddings(query)
        results = index.query(vector=query_vector, top_k=top_k, include_values=include_values, include_metadata=include_metadata)
        return results['matches']

    @staticmethod
    def generate_cache_key(document: str) -> str:
        """
        Generate a cache key for a document.
        """
        return hashlib.md5(document.encode()).hexdigest()

    def generate_answer(self, query: str, relevant_chunks: List[str]) -> str:
        prompt = ChatPromptTemplate.from_template("""
        Based on the following information, please provide a concise and accurate answer to the question.
        If the information is not sufficient to answer the question, say so.

        Question: {query}

        Relevant information:
        {chunks}

        Answer:
        """)
        messages = prompt.format_messages(query=query, chunks="\n\n".join(relevant_chunks))
        response = self.llm.invoke(messages)
        return response.content

def index_documents(): 
    cr = ContextualRetrieval()
    for file in os.listdir("precedents/"):
        filename = "precedents/" + file
        print(f"Indexing {filename}")
        with open(filename, "r") as f:
            original_chunks, contextualized_chunks = cr.process_document(f.read(), filename)
            cr.create_pinecone_index("contextual-summary", contextualized_chunks)

def closest_matching_documents(query: str, top_k: int = 3): 
    cr = ContextualRetrieval()
    results = cr.query_pinecone_index("contextual-summary", query, top_k=top_k*30, include_values=False, include_metadata=True)
    document_names = set()
    for result in results: 
        document_names.add(result.metadata["document_name"])
        if len(document_names) == top_k: 
            break
    return list(document_names)


if __name__ == "__main__":
    index_documents() 
    print(closest_matching_documents("What is the capital of France?"))