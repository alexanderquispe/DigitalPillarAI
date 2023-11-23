import requests, json, os, tqdm, pycountry
import pandas as pd, numpy as np, warnings

warnings.filterwarnings("ignore")


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


def data_country(cod_country):
    """
    The function `data_country` retrieves data from the World Bank API for a specific country and saves
    it in both JSON and CSV formats.

    :param cod_country: The parameter "cod_country" is a string that represents the country code. It is
    used to filter the data from the World Bank API based on the specified country
    :return: The function `data_country` returns a pandas DataFrame containing data related to a
    specific country. If there are no documents available for the given country, an empty DataFrame is
    returned.
    """
    main_url = f"https://search.worldbank.org/api/v2/wds?format=json&fct=docty_exact,count_exact,lang_exact,disclstat_exact&rows=0&apilang=en&docty_key=540656&order=desc&os=0&srt=docdt&countrycode_exact={cod_country}"

    response = requests.get(main_url)
    total_docs = response.json()["total"]
    if total_docs < 1:
        return pd.DataFrame()

    dir_json = f"data/api/json/{cod_country}"
    dir_csv = f"data/api/csv/{cod_country}"
    to_request = f"https://search.worldbank.org/api/v2/wds?format=json&fct=docty_exact,count_exact,lang_exact,disclstat_exact&rows={total_docs}&apilang=en&docty_key=540656&order=desc&os=0&srt=docdt&countrycode_exact={cod_country}"

    docs = requests.get(to_request).json()["documents"]

    json_file = dir_json + "_country.json"
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
    df["cod_country"] = cod_country
    df.to_csv(dir_csv + "_country.csv", index=False)
    df.to_json(json_file)
    return df


# The code is retrieving data from the World Bank API for each country and saving it in a CSV file.

countries = list(pycountry.countries)
countries = [x.alpha_2 for x in countries]

all_data = pd.DataFrame()
for country in countries:
    try:
        info = data_country(country)
        all_data = pd.concat([all_data, info])
    except:
        pass

all_data.to_csv("data/csv/00_all_country_data.csv", index=False)
