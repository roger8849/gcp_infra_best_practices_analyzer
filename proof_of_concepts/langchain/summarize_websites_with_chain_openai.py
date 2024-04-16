import openai
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms.openai import OpenAI
from langchain.chains.summarize import load_summarize_chain

from langchain.document_loaders import UnstructuredURLLoader

from google.cloud import secretmanager

def access_secret(project_id, secret_id, version_id="latest"):
    """Accesses the payload for the given secret version."""

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    secret_path = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(request={"name": secret_path})

    # Extract the secret payload.
    secret_payload = response.payload.data.decode("utf-8")

    return secret_payload


# List of urls as parameter to
urls = ["https://cloud.google.com/architecture/best-practices-vpc-design"]

# create instance of UnstructuredURLLoader class
loader = UnstructuredURLLoader(urls=urls)

print(type(loader))


# Create list of Documents. One for each website content
data = loader.load()


print(type(data), type(data[0]))


print(data)


print(data[0].page_content)


chunk_size = 3000
chunk_overlap = 200

text_splitter = CharacterTextSplitter(
    # separator = "\n\n"
    chunk_size=chunk_size,  # Maximum size of a chunk
    chunk_overlap=chunk_overlap,  # Maintain continuity, have some overlap of chunks
    length_function=len,  # Count number of characters to measure chunk size
)
texts = text_splitter.split_text(data[0].page_content)

# Create Document objects for each text chunk
docs = [Document(page_content=t) for t in texts[:]]


print(len(docs))


print(docs[0].page_content)


openai_api_key = access_secret(project_id='castilla-lived', secret_id='open_ai_api_key')


llm = OpenAI(temperature=0, openai_api_key=openai_api_key)


# To summarize multiple documents
# chain = "map_reduce" - find summary for each Document and then summarize all summaries
map_reduce_chain = load_summarize_chain(llm, chain_type="map_reduce")


# Perform summarization using run
# docs - list of documents to summarize
output = map_reduce_chain.run(docs)
# install tiktoken
print('######################################')
print('final summary of the entire web page')
print(output)
