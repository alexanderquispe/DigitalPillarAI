import requests, json, pandas as pd
import numpy as np, warnings, tqdm, pycountry




def url_api_wb(
    project_id: str=None,
    country_code: str=None,
    start_date: str=None,
    end_date: str = None, 
    lndinstr: str = None
) -> str:
    mainURL = "https://search.worldbank.org/api/v2/wds?format=json&fct=docty_exact,count_exact,lang_exact,disclstat_exact&docty_key=540656"

    if project_id is not None:
        return mainURL + "&projectid=" + project_id + "&rows=1"
    if country_code is not None:
        mainURL += "&countrycode_exact=" + country_code
    if lndinstr is not None:
        mainURL += "&lndinstr=" + lndinstr.replace(" ", "+")
    if start_date is not None:
        mainURL += "&strdate=" + start_date
    if end_date is not None:
        mainURL += "&enddate=" + end_date
    return mainURL 

def principal_data(documents):
    return {
        "projectid" : documents.get('projectid'),
        "repnb": documents.get('repnb'),
        "txturl": documents.get('txturl'),
        "pdfurl": documents.get('pdfurl')
    }

def get_content(url):
    info = requests.get(url).json()['documents']
    unique_info = list(info.keys())[0]
    return principal_data(info[unique_info])


    

def data_from_country(cod_country:str):
    cod_country =  cod_country.upper()
    url = url_api_wb(country_code=cod_country)
    # print(url)
    info = requests.get(url).json()
    total = info.get('total')
    url = url + f"&rows={total}"

    docs = requests.get(url).json()['documents']

    
    docs_keys = list(docs.keys())
    # print(docs_keys)
    main_info = []
    for doc in docs_keys:
        if doc != "facets":
            # print(docs[doc].get("projectid"))
            ref  = principal_data(docs[doc])
            main_info.append(ref)
    return main_info, total

    


