import numpy as np, re


all_regex = {
	'description_':[
		# III PROJECT DESCRIPTION  PROJECT DESCRIPTION

		r'([a-z]+\.\s*)?([a-z]{0,3}\.\s*)(?:roject|project|projection|program|project|strategic|institutional|projects)(?:\s+and)?\s+(?:description|context)$',
		# r'([a-z]{0,3}+\s*)?(?:roject|project|projection|program|project|strategic|institutional|projects)(?:\s+and)?\s+(?:description|context)$',
		r'description of phase \d+$'
	],
	'implementation_': [
		r'([a-z]+\.\s*)?([a-z]{0,3}\.\s*)(?:project|program|institutional)?\s*implementation(\s*\w+){0,3}$',
		r'key risks'
	],
	'components_': [
		r'^([a-z]+\.)\s*(?:project|phase \d+)?\s*.*components$'
	],
	'after_c': [
		r'(project|program) (approach|description|development( objetive( and key indicators)?( level result indicators)?)?)$'
	] ,
	'before_c': [
		r'^([a-z]+\.)\s*(program|project|summary project)?\s+(financing|beneficiaries|cost and financing)$',
        r'^([a-z]+\.)\s*(geographic targeting|lessons learned and reflected in the project design|theory of change|updated program results)$'
	],
	'description1':[
		r'\s*project description'
	],
	'implementation1':[
		# r'\s*(implementation|iii. procurement)'
		# r'\s*((?!support|phase|risk|annex|onal)(implementation|iii. procurement)'
		r'\s*((?!support|phase|risk|annex|rional|unit)(implementation|iii\. procurement))'
	],
	"components_1":[
		r'\s*project components'
	], 
	"before_c1":[
		 r'(\w*\s*project\s+(cost|beneficiaries|monitoring|financ|design))|(analytical under|support plan)'
	]
}

def _in_regex(value, regex_list, r = None):
    for regex in regex_list:
        if re.search(regex, value):
            return True
    return r

proj_desc = ['description_', 'implementation_']

proj_comp = ['components_', 'before_c']

def get_regex(keys):
	regex_s = []
	for k in keys:
		r_k = all_regex.get(k)
		regex_s += r_k
	return regex_s

def get_regex_result(values, target='description', r = None, manual = None):
    if target == 'description':
        regex_list = get_regex(proj_desc)
    elif target == 'component':
        regex_list = get_regex(proj_comp)
    elif manual is not None:
        r = False
        regex_list = [manual]
    else:
        r = False
        regex_list = get_regex(target)
    # print(regex_list)
    n_value_list = []

    for value in values:
        value_eval = _in_regex(value, regex_list, r = r)
        n_value_list.append(value_eval)
    return np.array(n_value_list)
        


#  II. PROJECT DESCRIPTION
#   II.   Project Description
# II. PROJECT DESCRIPTION
# PROJECT DESCRIPTION 
# (ii) PROJECT DESCRIPTION

# Implementation Support Plan
#  III. IMPLEMENTATION ARRANGEMENTS 
# III.   Procurement
# A. Institutional and Implementation Arrangements
# IMPLEMENTATION ARRANGEMENTS 
#   (iii) IMPLEMENTATION ARRANGEMENTS 

# A Project Components
# A, PROJECT COMPONENTS
# A. Project Components
# A. Project Components
# B. Project Components 
# B.       Project Component
#  Project Components
# Project components
#        Project Components
# Project Components
# A. Project Components for Phase I

# B. Project Cost 
# B. Project Financing
# B. Project Financing
#    Project Financing
#  2. Project Cost and Financing
# B. Project Cost and Financing
# C. Analytical Underpinnings 
# Project Beneficiaries
# C. Project Beneficiaries 
#  IMPLEMENTATION SUPPORT PLAN
# Lessons Learned and Reflected in the Project Design
# Project Monitoring and Evaluation System
#   D. Project Cost and Financing (US$, millions)