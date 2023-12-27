import re, requests, warnings

warnings.filterwarnings("ignore")


def save_txt(url, _file="", online=True):
    response = requests.get(url)
    text = response.text
    if online:
        return text
    # try:
    #     with open(_file, "wb") as f:
    #         f.write(response.content)
    # except:
    #     pass
    return text


def read_local(_file):
    with open(_file, "rb") as f:
        text = f.read()
        try:
            text = text.decode("utf-8")
        except:
            text = text.decode("latin-1")
    return text


def clean_lines(text):
    dots = re.compile(r"\s*\.{2,}\s*\w*")
    lines = text.split("\n")
    lines = [re.sub(dots, "", line) for line in lines]
    lines = [re.sub(r"^\ufeff|\s+", " ", line).strip() for line in lines]
    lines = [line for line in lines if len(line) > 0]
    return lines


roman_dict = {"I": "II", "II": "III", "III": "IV"}


def only_valid_caracter(text):
    matches = re.findall(r"\w+", text)
    matches = [x.lower() for x in matches]
    return " ".join(matches)


def find_components(str_description):
    match_components = re.search(
        r"([A-Z])\.\s*(Description of )?(Project|Phase [I1-9]?) Components",
        str_description,
        flags=re.IGNORECASE,
    )
    if match_components:
        start_letter = match_components.group(
            1
        )  # This captures the letter before "PROJECT COMPONENTS"
        next_letter = chr(
            ord(start_letter) + 1
        )  # This gets the next letter in the alphabet
        start_index_components_within_description = match_components.start()
        end_index_components_within_description = str_description.find(
            f"{next_letter}. ", start_index_components_within_description
        )
        extracted_components_within_description = str_description[
            start_index_components_within_description:end_index_components_within_description
        ].strip()
    else:
        extracted_components_within_description = None
    return extracted_components_within_description


def find_project_description(str_elements):
    find = "PROJECT DESCRIPTION"
    toc_start_index = str_elements.find(find)
    pattern = rf"([I]{1,3})\.\s+{find}"
    match = re.search(
        pattern,
        str_elements[toc_start_index + len("PROJECT DESCRIPTION") :],
        flags=re.IGNORECASE,
    )
    if not match:
        extracted_description_body = None
        extracted_components = None
        return extracted_description_body, extracted_components
    roman_numeral = match.group(1)  # type: ignore
    next_roman = roman_dict.get(roman_numeral, "UNKNOWN")

    main_body_start_index = match.start() + toc_start_index + len(find)  # type: ignore
    main_body_end_index_pattern = rf"({next_roman}\.\s+)?[A-Z\s]*IMPLEMENTATION"
    main_body_end_match = re.search(
        main_body_end_index_pattern, str_elements[main_body_start_index:]
    )
    if not main_body_end_match:
        extracted_description_body = None
        extracted_components = None
        return extracted_description_body, extracted_components

    main_body_end_index = main_body_end_match.start() + main_body_start_index
    extracted_description_body = str_elements[
        main_body_start_index:main_body_end_index
    ].strip()
    extracted_components = find_components(extracted_description_body)
    return extracted_description_body, extracted_components


def extract_project_info_from_url(url):
    cleaned_content = clean_lines(save_txt(url))
    cleaned_content = "\n".join(cleaned_content)
    elements = find_project_description(cleaned_content)
    return elements


def count_tokens(text):
    if isinstance(text, str):
        tokens = re.findall(r"\w+|[.,!?;]", text)
        return len(tokens)
    return 0
