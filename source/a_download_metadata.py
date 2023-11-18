import requests, json, os, tqdm
import pandas as pd, numpy as np

cod_country = "CM"

url = f"https://search.worldbank.org/api/v2/wds?format=json&fct=docty_exact,count_exact,lang_exact,disclstat_exact&rows=0&apilang=en&docty_key=540656&order=desc&os=0&srt=docdt&countrycode_exact={cod_country}"

"""
@author: tjhon
"""


def get_value(data, key):
    try:
        value = data[key]
        try:
            return value.strip()
        except:
            return value
    except KeyError:
        return np.nan


a = os.path.exists("data/api/json")

keys_in_json = [
    "id",
    "projectid",
    "repnb",
    "theme",
    "pdfurl",
    "txturl",
    "url",
    "url_friendly_title",
    "lang",
    "display_title",
    "author",
    "docdt",
    "volnb",
    "count",
    "disclosure_date",
    "disclastat",
    "owner",
    "origu",
    "versiontyp",
    "colti",
    "dois",
]


TOTAL = 10508


"""
@author: tjhon
"""


def json_range(from_, to_):
    """
    The function `json_range` retrieves data from the World Bank API within a specified range, saves it
    as both a JSON file and a CSV file, and returns a pandas DataFrame.

    :param from_: The starting index of the range for the API request
    :param to_: The `to_` parameter represents the end value of the range. It is used to determine the
    number of rows to retrieve from the API
    :return: The function `json_range` returns a pandas DataFrame object.
    """
    rows = to_ - from_
    file_name = f"wb_{from_}_to_{to_}"
    dir_json = f"data/api/json/{file_name}"
    dir_csv = f"data/api/csv/{file_name}"
    to_request = f"https://search.worldbank.org/api/v2/wds?format=json&docty_key=620265&rows={rows}&os={from_}"
    docs = requests.get(to_request).json()["documents"]
    json_file = dir_json + ".json"
    if os.path.exists(json_file):
        df = pd.read_json(json_file)
        return df
    files = list(docs.keys())
    data = {key: [] for key in keys_in_json}
    for file in tqdm.tqdm(files, ncols=100):
        if file != "facets":
            w = docs[file]
            for key in keys_in_json:
                data[key].append(get_value(w, key))
    df = pd.DataFrame(data).reset_index()
    df.to_csv(dir_csv + ".csv", index=False)
    df.to_json(json_file)
    return df


# The code is retrieving data from the World Bank API in batches of 500 rows at a time.
by = 500
begin = np.arange(0, TOTAL, by)
final = begin + by
final[-1] = TOTAL

all_data = pd.DataFrame()

# The code snippet is iterating over pairs of values `b` and `f` using the `zip` function. These pairs
# represent the starting and ending indices of the range for retrieving data from the World Bank API.
for b, f in tqdm.tqdm(zip(begin, final)):
    df = json_range(b, f)
    all_data = pd.concat([all_data, df])
all_data.to_csv("data/csv/00_final_data.csv")
