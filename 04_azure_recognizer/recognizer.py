import json, pandas as pd, numpy as np

from azure.ai.formrecognizer import \
	 DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import pickle
import os



class AzureDocument:

	def __init__(self, credentials_path_json='../pass_keys.json', endpoint_name = 'ENDPOINT', apikey = 'API-KEY'):

		credentials = json.load(open(credentials_path_json))
		azure_model = 'prebuilt-layout'

		ENDPOINT = credentials['ENDPOINT']
		APIKEY = credentials['API-KEY']

		client = DocumentAnalysisClient(ENDPOINT, AzureKeyCredential(APIKEY))

		self.document_analysis_client = client
		
	
	def process_document(
		self, file_path, azure_model='prebuilt-layout',
		name = "sample",
		save = True, 
		force = False
		):
		# exists = os.path.exists(name) 

		# if not force | exists:
		# 	print()
		# 	return name


		with open(file_path, "rb") as f:
			poller = self.document_analysis_client.begin_analyze_document(
				azure_model, f.read()
			)
		result = poller.result().to_dict()
		self.result = result

		self._get_role()
		self._get_filtered_roles()
		self.convert_roles_in_data()
		# if save:

		self.all_data = {
			'roles': self.roles,
			'results': poller.result(),
			'rest_data_dict': self.rest_data,
			'results_dict': result,
			'data_dict': self.data,
			'data_process': self.data_context
		}

		if save:
			with open(name, 'wb') as f:
				pickle.dump(self.all_data, f)
		return name
		
	def _get_role(self):
		roles = [
			paragraph.get('role') 
			for paragraph in self.result['paragraphs']
		]
		roles = list(set(roles))
		self.roles = roles
	
	def _get_filtered_roles(self,
		omit = ['footnote', 'pageHeader', 'pageNumber'], 
		relevance = ['title', 'sectionHeading']
		):

		paragraphs = self.result['paragraphs']

		filter_paragraph = [
			paragraph for paragraph in paragraphs if paragraph.get('role') not in omit 
		]
		filtered_data = [{'role': item.get('role'), 'content': item.get('content')} for item in paragraphs if item.get('role') not in omit]
		with_data = [{'role': item.get('role'), 'content': item.get('content')} for item in paragraphs if item.get('role') in omit]

		self.data = pd.DataFrame(filtered_data)
		self.rest_data = with_data
		

	def convert_roles_in_data(self):
		data = self.data
		data['row_id'] = data.index.map(lambda x: f'{x+1:03d}')
		data['role_content'] = data.apply(
			lambda row: f"{row['row_id']}_{row['role']}_{row['content']}" if not pd.isna(row['role']) else row['role'], axis=1
		)
		data['role_content'].fillna(method='ffill', inplace=True)
		# data = data[data['role'].isna()]
		data.dropna(subset=['role_content'], inplace=True)
		data = data.groupby('role_content')['content'].apply(lambda x: '\n'.join(x)).reset_index()
		data[['row_id', 'role', 'text_role']] = data['role_content'].str.split('_', expand=True)
		data.rename(columns={'content': 'paragraph_content'}, inplace=True)

		data.drop(columns=['row_id', 'role_content'], inplace=True)
		data = data[['role', 'text_role', 'paragraph_content']]
		self.data_context = data