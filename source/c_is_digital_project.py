import pandas as pd, numpy as np, time
import openai, os, requests
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from tqdm import tqdm

## pip install faiss-gpu : if you have a dedicated GPU
# pip install faiss-cpu
from langchain.vectorstores import FAISS
from PyPDF2 import PdfReader

openai_key = "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"
openai.api_key = openai_key
os.environ["OPENAI_API_KEY"] = openai_key


# def is_digital_project(pdf_path):

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

    query = f'is the document discussing digital topics? and why?, separate by ";"'
    try:
        response = requests.get(url_txt)
    except:
        return None, None

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
        is_digital = 1 if "yes" == answer.lower() else 0
        return is_digital, response_text
    except:
        text = [doc.page_content for doc in docs]
        context = "\n".join(text)
        return None, context


def add_dp(data, txt_url_column="txturl"):
    """
    The function `add_dp` takes a DataFrame and adds two new columns indicating whether a given URL is a
    digital project and whether it is a digital response.

    :param data: The "data" parameter is a pandas DataFrame that contains the data you want to process.
    It should have a column named "txturl" which contains the URLs you want to check
    :param txt_url_column: The parameter "txt_url_column" is the name of the column in the "data"
    dataframe that contains the text URLs, defaults to txturl (optional)
    :return: the modified data with two additional columns: "is_digital_project" and
    "is_digital_response".
    """
    txt_urls = data[txt_url_column].values
    results = []
    for i in tqdm(txt_urls):
        results.append(is_digital_project(i))

    results = data[txt_url_column].apply(lambda x: is_digital_project(x))
    data["is_digital_project"] = results.apply(lambda x: x[0])
    data["is_digital_response"] = results.apply(lambda x: x[1])
    return data
