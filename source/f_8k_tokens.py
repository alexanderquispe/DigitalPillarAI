import openai, pandas as pd, os, re


from langchain.text_splitter import CharacterTextSplitter


from .z_secrets import openai_key

openai.api_key = openai_key
os.environ["OPENAI_API_KEY"] = openai_key


prompt = "Summarize the following text in less than 200 words, focusing in the project components:"


def count_tokens(text):
    if isinstance(text, str):
        tokens = re.findall(r"\w+|[.,!?;]", text)
        return len(tokens)
    return 0


def split_text(text, cut_off):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=cut_off,
        chunk_overlap=30,
        length_function=count_tokens,
    )
    texts = text_splitter.split_text(text)
    texts = [{"content": f"{prompt} {text}", "role": "user"} for text in texts]
    return texts


def summary_text(text):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-16k", messages=[text], temperature=0
    )
    return response.choices[0].message.content


def all_resumen(texts_all, cut_off=5000):
    text_o = texts_all
    l_text = count_tokens(text_o)
    if l_text < cut_off:
        return text_o
    texts = split_text(text_o, cut_off)
    texts_summary = [summary_text(text) for text in texts]
    text_o = "\n".join(texts_summary)  # type: ignore
    text_o = text_o.split(" ")[:cut_off]
    text_o = " ".join(text_o)

    return text_o
