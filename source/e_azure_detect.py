# work with pdf
# some titles and header are images

import json, pandas as pd, numpy as np
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import pickle, os


class AzureDocument:
    def __init__(
        self, credential_path="pass_keys.json", endpoint="ENDPOINT", apikey="API-KEY"
    ):
        credential = json.load(open(credential_path))
        ENDPOINT = credential[endpoint]
        APIKEY = credential[apikey]

        client = DocumentAnalysisClient(ENDPOINT, AzureKeyCredential(APIKEY))
        self.document_analysis_client = client

    def process_document(
        self,
        url,
        azure_model="prebuilt-layout",
        name="sample.pkl",
        save=True,
        force=False,
    ):
        if os.path.exists(name):
            fff = open(name, "wb")
            result = pickle.load(fff)
        else:
            poller = self.document_analysis_client.begin_analyze_document_from_url(
                azure_model, url
            )
            result = poller.result().to_dict()
        self.result = result
        if save:
            with open(name, "wb") as f:
                pickle.dump(result, f)
        return result, name

    def lines_data(self, url_pdf):
        try:
            self.process_document(url_pdf)
            paragraphs = self.result["paragraphs"]
            data_lines = [item.get("content") for item in paragraphs]
            return "\n".join(data_lines)
        except:
            return "None"
