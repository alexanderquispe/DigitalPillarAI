import requests, pandas as pd, warnings


from .utils.utils import clean_lines, save_txt, only_valid_caracter
from .utils_regex.regex import regex_result, PD_1, PC_1, in_regex, _in_regex


def lines_to_df(source):
    if "http" in source:
        text = save_txt(source)
    else:
        text = source
    info = clean_lines(text)
    data = pd.DataFrame({"info": info})
    data["text"] = data["info"].apply(lambda x: only_valid_caracter(x))
    return data


def get_rows(df, n=200):
    df = df.iloc[n:]
    return df


def detect_row(df, col="text", new_col="annex", patter=r"^annex"):
    try:
        df[new_col] = df[col].apply(lambda x: x if in_regex(x, patter) else None)
        return df
    except:
        return None


def detect_first(df, col="text", new_col="pd", patterns=PD_1["description"]):
    df[new_col] = df[col].apply(lambda x: x if _in_regex(x, patterns) else None)
    return df.dropna(subset=new_col)


def detect_second(df, col="text", new_col="pd", patterns=PD_1["implementation"]):
    df[new_col] = df[col].apply(lambda x: x if _in_regex(x, patterns) else None)
    return df.dropna(subset=new_col)


def filter_detect(df1, df2, annex=None):
    if annex is not None:
        annex_i = annex.dropna(subset="annex").index[0]
        df1 = df1.query("index < @annex_i")
        df2 = df2.query("index < @annex_i")
    df1_i = df1.index[0]
    df2 = df2.query("index > @df1_i")
    if len(df2) > 0:
        df2_i = df2.index[0]
        df1_i = df1.index[-1]
        return df1_i, df2_i

    return df1_i, df1_i + 400


def proccess_loop(data, n, patter1=PD_1["description"], patter2=PD_1["implementation"]):
    data = get_rows(data, n)

    annex = detect_row(data)  # type: ignore
    first = detect_first(data, patterns=patter1).dropna(subset="pd")
    second = detect_second(data, patterns=patter2).dropna(subset="pd")
    if n < 100:
        annex = None
    rows_begin, rows_end = filter_detect(first, second, annex)
    filter_data = data.query("index <= @rows_end and index >= @rows_begin")
    return filter_data


def get_context(
    url, patter1=PD_1["description"], patter2=PD_1["implementation"], n1=400
):
    data = lines_to_df(url)
    n = n1
    result = None
    while True:
        try:
            filter_data = proccess_loop(data, n, patter1, patter2)
            text = filter_data["info"].values
            text = "\n".join(text)
            result = text
            break
        except:
            if n < 10:
                break
            n -= 10
    return result


def get_components(description=None, url=None):
    pc = None
    if description is None and url is None:
        return pc
    if description is not None:
        pc = get_context(description, PC_1["components"], patter2=PC_1["other"])
    if url is not None:
        pc = get_context(url, PC_1["components"], patter2=PC_1["other"])
    return pc
