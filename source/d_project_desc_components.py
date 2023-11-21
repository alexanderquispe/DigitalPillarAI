import requests
from utils.utils import clean_lines


class ExtractProjects:
    def __init__(self, url):
        self.url = url
