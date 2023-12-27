import numpy as np, re

PD_1 = {
    "description": [r"([a-z]{1,3}\s+)?(?:project|program)\s+description$"],
    "implementation": [
        r"([a-z]{1,3}\s+)?(?:project|program|institutional)?\s*implementation(\s*\w+){0,3}",
        r"key risks",
    ],
}

PC_1 = {
    "components": [r"([a-z]{1,3}\s+)?(?:project|program|phase \d+)\s*components$"],
    "other": [
        r"([a-z]{1,3}\s+)?(program|project|summary project)?\s+(financing|beneficiaries|cost and financing)$",
        r"([a-z]{1,3}\s+)?(geographic targeting|lessons learned and reflected in the project design|theory of change|updated program results|results chain|total costs|project coordination)$",
    ],
}


def in_regex(value, regex):
    find = re.match(regex, value)
    if find:
        return True
    return None


def _in_regex(value, regex_list, r=None):
    for regex in regex_list:
        if re.match(regex, value):
            return True
    return r


def regex_result(values, manual=None):
    if manual is None:
        return
    result = []
    for value in values:
        value_result = _in_regex(value, manual)
        result.append(value_result)
    return result
