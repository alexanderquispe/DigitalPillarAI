import openai, pandas as pd, os


from langchain.text_splitter import CharacterTextSplitter


from z_secrets import openai_key

openai.api_key = openai_key
os.environ["OPENAI_API_KEY"] = openai_key

a = """
Step 3: Preprocess your text data
Before you can generate summaries using OpenAI’s GPT-3 API, you’ll need to preprocess your text data to ensure it’s in the correct format. Specifically, you’ll need to split your text into smaller chunks that are suitable for input into the API.

You can use the split_text function below to split your text into smaller chunks of up to 2048 characters each:
"""

prompt = "Summarize the following text in less than 200 words:"


def split_text(text):
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=100, chunk_overlap=30, length_function=len
    )
    texts = text_splitter.split_text(text)
    texts = [{"content": f"{prompt} {text}", "role": "user"} for text in texts]
    return texts


def summary_text(text):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-16k", messages=[text], temperature=0
    )
    return response.choices[0].message.content


def all_resumen(texts_all):
    texts = split_text(texts_all)
    texts_summary = [summary_text(text) for text in texts]
    summary = "\n".join(texts_summary)  # type: ignore
    return summary
