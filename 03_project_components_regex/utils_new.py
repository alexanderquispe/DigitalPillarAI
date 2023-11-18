import os, re, requests
import numpy as np, pandas as pd
from tqdm import tqdm
import warnings

warnings.filterwarnings('ignore')

from .regex_new import *

txt_dir = 'files\\txt'
def read_txt(url, _id, path_txt = txt_dir, force = False):
	_file = f'{path_txt}\{_id}.txt'
	# print(_file)
	_exists =  os.path.exists(_file)

	def save_txt() :
		response = requests.get(url)
		text = response.text
		try:
			with open(_file, 'wb') as f:
				f.write(response.content)
		except:
			pass
		return text
	def read_local():
		with open(_file, 'rb') as f:
			text = f.read()
			try:
				text = text.decode('utf-8')
			except:
				text = text.decode('latin-1')
		return text

	if not _exists:
		save_txt()
	elif _exists or force:
		read_local()

	try:
		text = read_local() 
	except:
		text = save_txt()

	lines = text.split('\n')
	dots = re.compile(r'\s*\.{2,}\s*\w*')

	lines = [re.sub(dots, '', line) for line in lines]
	lines = [re.sub(r'^\ufeff|\s+', ' ', line).strip() for line in lines]

	# re.sub(r'\s+', " ", ).strip()
	lines = [line for line in lines if len(line) > 0]
	text_lines = pd.DataFrame({'lines': lines})
	text_lines['text'] = text_lines['lines'].str.lower()
	text_lines['len_text'] = text_lines['lines'].apply(
		lambda x: len(x)
	)
	text_lines['n_words'] = text_lines['lines'].apply(
		lambda x: len(x.split(" "))
	)
	return text_lines


table = r'table of contents'

def toc_contents(data, n=5, n_relevant = 100):
	data['toc'] = \
		data.apply(
			lambda x: 'toc'
			if re.search(table, x['text'])
			else None, axis = 1
		)
	# data = data.
	not_relevant = data.groupby('lines')\
		.size().reset_index(name = 'l')\
		.sort_values('l', ascending = False)\
		.query('l > @n_relevant')\
		['lines']
	not_relevant = list(not_relevant)

	data = data.query('lines not in @not_relevant')

	content_toc = data.fillna(method = 'ffill').dropna()
	toc = content_toc.iloc[:50].query('n_words < @n')
	content = content_toc.iloc[50:].drop(columns = 'toc')

	return toc, content


# For structured TOC

def search_desc_text(data, col = 'text', n=4, main = 'description', up_r = 'description_', down_r = 'implementation_', target = None):
	all_data = data.copy()
	data = data.query('n_words < @n')
	col_ref = data[col].to_numpy()
	rows_regex = get_regex_result(col_ref, main, r = False)
	col_target_df = data[rows_regex]
	col_ref_target = col_target_df[col]

	up_regex = get_regex_result(col_ref_target, target=[up_r])
	down_regex = get_regex_result(col_ref_target, target=[down_r])

	up_df = col_target_df[up_regex]
	down_df = col_target_df[down_regex]

	up = up_df['lines'].to_numpy()
	down = down_df['lines'].to_numpy()
	l_up = len(up) 


	if len(up) > 0 and len(down) > 0:

		up_value = up[l_up - 1]
		down_value = down[0]
		values = [up_value, down_value]
		# return values


		all_data['h2'] = all_data.apply(
			lambda row:
			row['lines'] 
			if row['lines'] in values
			else None, axis = 1 
		)
		target_data = \
			all_data.fillna(method='ffill')\
			.query('h2 == @up_value')

		return target_data 
	else:
		return []

def extract_names(df, name='lines') -> str:
	t = df['lines'].values
	text = "\n".join(t)
	return text 


def search_desc_text_strong(data, col = 'text', n=5, main = 'description', up_r = 'description1', down_r = 'implementation1', target = None):
	all_data = data.copy()
	data = data.query('n_words < @n')
	col_ref = data[col].to_numpy()
	rows_regex = get_regex_result(col_ref, main, r = False)
	col_target_df = data[rows_regex]
	col_ref_target = col_target_df[col]

	up_regex = get_regex_result(col_ref_target, target=[up_r])
	down_regex = get_regex_result(col_ref_target, target=[down_r])

	up_df = col_target_df[up_regex]
	down_df = col_target_df[down_regex]

	up = up_df['lines'].to_numpy()
	down = down_df['lines'].to_numpy()
	l_up = len(up) 



	if len(up) > 0 and len(down) > 0:
		# print('up', up)
		# print('down', down)

		up_value = up[l_up - 1]
		down_value = down[0]
		values = [up_value, down_value]
		# print('\n')
		# print("\t", up_value)
		# print("\t", down_value)
		
		# return values


		all_data['h2'] = all_data.apply(
			lambda row:
			row['lines'] 
			if row['lines'] in values
			else None, axis = 1 
		)
		target_data = \
			all_data.fillna(method='ffill')\
			.query('h2 == @up_value')

		return target_data 
	else:
		return []