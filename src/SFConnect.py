import json
import base64
import shutil
import requests


class SFConnect(object):

    session_id = None
    instance_url = None

    def __init__(self, session_id, instance_url):
        self.session_id = session_id
        self.instance_url = instance_url

    def base_url(self):
        return self.instance_url[0:self.instance_url.find('/services')] + '/services/data/v28.0'

    def base_headers(self):
        return {'Authorization': 'OAuth ' + self.session_id}

    def fetch_query(self, query_id):
        query_rec_url = self.base_url() + '/sobjects/MergeQuery__c/' + query_id
        resp = requests.get(query_rec_url, headers=self.base_headers())
        query_data = resp.json()
        return query_data['SOQL__c']

    def fetch_dataset(self, query):
        rec_data_url = self.base_url() + '/query/?q=' + query
        rd = requests.get(rec_data_url, headers=self.base_headers())
        return rd.text

    def fetch_document(self, document_id, output_path):
        doc_body_url = self.base_url() + '/sobjects/Document/' + document_id + '/body'
        resp = requests.get(doc_body_url, stream=True, headers=self.base_headers())
        with open(output_path, 'wb') as f:
            resp.raw.decode_content = True
            shutil.copyfileobj(resp.raw, f)

    def push_document(self, input_path, folder_id):
        payload = dict()
        payload["Description"] = 'Test Generated Output File'
        payload["Keywords"] = ''
        payload["FolderId"] = folder_id
        payload["Name"] = "Generated Output"
        payload["Type"] = "pdf"

        with open(input_path, "r") as source_file:
            encoded_string = base64.b64encode(source_file.read())

        payload["body"] = encoded_string

        post_headers = self.base_headers()
        post_headers['Content-Type'] = 'application/json'

        doc_post_url = self.base_url() + '/sobjects/Document/'
        resp = requests.post(doc_post_url, headers=post_headers, data=json.dumps(payload))
        return resp.text