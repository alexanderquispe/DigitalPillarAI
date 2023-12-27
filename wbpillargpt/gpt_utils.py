import pandas as pd
import openai, os, requests
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

## pip install faiss-gpu : if you have a dedicated GPU
# pip install faiss-cpu
from langchain.vectorstores import FAISS

from .z_secrets import openai_key

openai.api_key = openai_key
os.environ["OPENAI_API_KEY"] = openai_key


# data = pd.read_csv("data/csv/01_merged_data_with_powerbi.csv")

test_url = "https://documents1.worldbank.org/curated/en/746421608001638858/text/Bosnia-and-Herzegovina-Firm-Recovery-and-Support-Project.txt"


def is_digital_project(url_txt):
    """
    The function `is_digital_project` takes a URL as input and determines if the document at that URL
    discusses digital topics, returning a binary value (1 for yes, 0 for no) and a justification for the
    decision.

    :param url_txt: The `url_txt` parameter is a string that represents the URL of a text document that
    you want to analyze
    :return: The function `is_digital_project` returns a tuple containing two values. The first value is
    either 1 or 0, indicating whether the document is discussing digital topics or not. The second value
    is a string explaining why the document is considered to be discussing digital topics.
    """

    query = f'is the document discussing digital topics? and why?, separate the boolean and why by ";"'
    is_digital = False
    try:
        response = requests.get(url_txt)
    except:
        return is_digital, None

    txt_content = response.text

    # The code snippet `text_splitter = CharacterTextSplitter(separator="\n", chunk_size=2000,
    # chunk_overlap=300, length_function=len)` is creating an instance of the `CharacterTextSplitter`
    # class. This class is used to split a long text document into smaller chunks or segments.
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=2000, chunk_overlap=300, length_function=len
    )
    texts = text_splitter.split_text(txt_content)
    embeddings = OpenAIEmbeddings()
    # The code snippet `doc_search = FAISS.from_texts(texts, embeddings)` is creating an instance of the
    # `FAISS` class and using it to create a vector store from the given texts. This vector store is used
    # to perform similarity search based on the embeddings of the texts.
    doc_search = FAISS.from_texts(texts, embeddings)
    chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
    docs = doc_search.similarity_search(query)
    # It is responsible for
    # running a question-answering chain to determine if the document is discussing digital topics and
    # provide a justification for the decision.
    try:
        response_text = chain.run(input_documents=docs, question=query)
        answer, why = response_text.split("; ")
        is_digital = "yes" in answer.lower()
        return is_digital, why
    except:
        text = [doc.page_content for doc in docs]
        context = "\n".join(text)
        return is_digital, context
