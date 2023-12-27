from fastapi import FastAPI

from wbpillargpt.z_utils import url_api_wb, data_from_country, get_content
from wbpillargpt.gpt_utils import is_digital_project
from wbpillargpt.proj_extract import get_context, get_components
from wbpillargpt.pillars import classification, is_digital_filter2, what_category

app = FastAPI()


@app.get("/")
def read_root():
    return {"API": "World Bank"}


@app.get("/country/{country_code}")
def projects_inside(country_code: str):
    docs, total = data_from_country(cod_country=country_code)
    return {"country_code": country_code, "total": total, "content": docs}


# P039086
@app.get("/project_id/{proj_id}")
def process_project_id(proj_id):
    url = url_api_wb(project_id=proj_id)
    content = get_content(url)
    txt_url = content.get("txturl")
    is_digital, why = is_digital_project(txt_url)
    content["is_digital"] = is_digital
    # content["why_fs"] = why

    # content["project_description"] = None
    # content["project_components"] = None
    # content["is_digital_ss_gpt"] = False
    content["pillars"] = []

    if not is_digital:
        return content

    ref = {}
    try:
        # Attemp with regex
        proj_desc = get_context(txt_url)
        proj_comp = get_components(txt_url)

        ref["project_description"] = proj_desc
        ref["project_components"] = proj_comp
    except:
        # Attemp with azure api
        pass
    # second_attemp
    what_category_list = {}
    is_digital = False
    if ref["project_components"] is not None:
        text_clasification = classification(proj_comp)
        is_digital = is_digital_filter2(text_clasification)
        what_category_list = what_category(text_clasification)
        print(is_digital, what_category_list)

    content["is_digital"] = is_digital
    content["pillars"] = what_category_list

    # content['type_of_digital_project'] =

    important = {
        "projectid": content["projectid"],
        "url": content["txturl"],
        "is_digital": content["is_digital"],
    }
    important.update(what_category_list)

    return important
