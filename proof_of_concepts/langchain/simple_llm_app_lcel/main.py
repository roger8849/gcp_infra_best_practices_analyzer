pip install -U langchain langchain-openai


LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY="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"
LANGCHAIN_PROJECT="gcp-best-practices-analyzer"


from langchain_openai import ChatOpenAI

llm = ChatOpenAI()
llm.invoke("Hello, world!")