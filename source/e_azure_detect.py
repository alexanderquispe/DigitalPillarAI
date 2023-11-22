# work with pdf
# some titles and header are images

import json, pandas as pd, numpy as np
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import pickle


class AzureDocument:
    def __init__(
        self, credential_path="pass_keys.json", endpoint="ENDPOINT", apikey="API-KEY"
    ):
        credential = json.load(open(credential_path))
        azure_model = "prebuilt-layout"
        ENDPOINT = credential[endpoint]
        APIKEY = credential[apikey]

        client = DocumentAnalysisClient(ENDPOINT, AzureKeyCredential(APIKEY))
        self.document_analysis_client = client

    def process_document(
        self,
        file_path,
        azure_model="prebuilt-layout",
        name="sample.pkl",
        save=True,
        force=False,
    ):
        with open(file_path, "rb") as f:
            poller = self.document_analysis_client.begin_analyze_document(
                azure_model, f.read()
            )
        result = poller.result().to_dict()
        if save:
            with open(name, "wb") as f:
                pickle.dump(result, f)
        return result, name
