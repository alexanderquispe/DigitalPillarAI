import pandas as pd
import openai, os, re, json
from .utils.pillars import user_message

category_names = [
    "Digital Public Platforms Category",
    "Digital Skills Category",
    "Digital Financial Services Category",
    "Digital Safeguards Category",
    "Digital Businesses Category",
    "Digital Infrastructure Category",
]


def get_completion_from_messages(
    messages, model="gpt-4", temperature=0, max_tokens=500
):
    response = openai.chat.completions.create(
        model=model, messages=messages, temperature=temperature, max_tokens=max_tokens
    )
    return response.choices[0].message.content  # type: ignore


def classification(text):
    try:
        mssg = user_message(text)
        response = get_completion_from_messages(mssg)
        return json.loads(response)  # type: ignore
    except:
        return "None"


categories = [
    "Digital Infrastructure Category",
    "Digital Public Platforms Category",
    "Digital Financial Services Category",
    "Digital Businesses Category",
    "Digital Skills Category",
    "Digital Safeguards Category",
]

# from .f_8k_tokens import all_resumen


# def valid_tokens(row, n_=5000):
#     pc = "project_components"
#     azure_str = "_azure"
#     pd = "project_description"
#     pc_azure = pc + azure_str
#     pd_azure = pd + azure_str
#     if row[pc] is not None:
#         return all_resumen(row[pc], cut_off=n_)
#     elif row[pc] is None and row[pc_azure] is not None:
#         return all_resumen(row[pc_azure], cut_off=n_)
#     if row[pd] is not None:
#         return all_resumen(row[pd], cut_off=n_)
#     else:
#         return all_resumen(row[pd_azure], cut_off=n_)


def cat_value(x, c):
    value = x.get(c).get("classification") == "yes"
    return value


def cat_score(x, c):
    return x.get(c).get("score", 0)


def what_category(dict_to_clas):
    found_categories = []
    dict_cat = {}
    for cate in categories:
        is_digital = cat_value(dict_to_clas, cate)
        dict_cat[cate] = is_digital
        # found_cat_score
        # df[cate] = df["classification"].apply(lambda x: cat_value(x, cate))
        # df[cate + "_score"] = df["classification"].apply(lambda x: cat_score(x, cate))
    return dict_cat


def is_digital_filter2(dic_list):
    cats = list(dic_list.keys())

    def values_list(dc, cat):
        category = dc.get(cat)
        result = {
            "name": cat,
            "is_digital": category.get("classification"),
            "explanation": category.get("explanation"),
            "score": category.get("score", 0),
        }
        return result

    digital_categories = [values_list(dic_list, cat) for cat in cats]
    digital_found = [
        digital_gpt
        for digital_gpt in digital_categories
        if digital_gpt.get("is_digital") == "yes"
    ]
    digital = False
    if len(digital_found) > 0:
        digital = True
    return digital
