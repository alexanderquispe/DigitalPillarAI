import json
from pypdf import PdfReader


url_test = './sample-pdf/sample_pdf.pdf'
url_test = './sample-pdf/sample_pdf-copy.pdf'
# pdf = PdfReader('./sample-pdf/sample_pdf.pdf')

# page_content = {
# }

# for indx, pdf_page in enumerate(pdf.pages):

# 	page_content[indx + 1] = pdf_page.extract_text()

# print(page_content)



from azure.core.exceptions import ResourceNotFoundError
from azure.ai.formrecognizer import FormRecognizerClient, FormTrainingClient, DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential


credentials = json.load(open('./pass_keys.json'))

ENDPOINT = credentials['ENDPOINT']
APIKEY = credentials['API-KEY']


# DocumentAnalysisClient.begin
document_analysis_client = DocumentAnalysisClient(ENDPOINT, AzureKeyCredential(APIKEY))


# poller = form_client.begin_recognize_content_from_url(url_test)


with open(url_test, "rb") as f:
    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-document", f.read(), pages='1, 5 '
    )

# with open(url_test, 'rb') as f1:
# 	file_content = f1.read().decode('utf-8')
# 	print(file_content)

# # import 

result = poller.result()
# json_string = json.dumps(result.__dict__, indent=4)

import pickle
# with open('save.pkl' as )
with open('save.pkl', 'wb') as f:
	pickle.dump(result, f)


with open(url_test, "rb") as f:
    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-layout", f.read()#, pages='1, 5 '
    )

result = poller.result()

with open('layout_build.pkl', 'wb') as f:
	pickle.dump(result, f)



# Imprime la cadena JSON resultante
# print(json_string)

# text = ''
# for page in result.pages:
# 	for line in page.lines:
# 		text+=line.content + ' '

# text = text.strip()
# print(text)

# print(dir(result))
# print(len(result.pages))
# for page in result.pages:
#     print("----Analyzing layout from page #{}----".format(page.page_number))
#     print(
#         "Page has width: {} and height: {}, measured with unit: {}".format(
#             page.width, page.height, page.unit
#         )
#     )
