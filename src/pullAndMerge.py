# import zipfile
# import cloudconvert

import os
import json
import base64
import requests
from SFConnect import SFConnect
from TokenMerge import TokenMerge

def lambda_handler(event, context):
    cloud_key = os.environ['cloudconvert']
    eventParams = event['queryStringParameters']

    instance = eventParams['instance']
    sessionID = eventParams['sessionID']
    query = eventParams['query']
    param1 = eventParams['param1']
    documentID = eventParams['documentID']
    folderID = eventParams['folderID']

    sfc = SFConnect(sessionID, instance)

    query_names_ids = dict()
    query_segments = [x.strip() for x in query.split(',')]
    for query_segment in query_segments:
        query_parts = query_segment.split(']')
        query_names_ids[query_parts[0][1:]] = query_parts[1]

    query_names_soql = dict()
    for query_name in query_names_ids.keys():
        query_result = sfc.fetch_query(query_names_ids[query_name])
        query_names_soql[query_name] = query_result

    context = dict()
    for query_name in query_names_soql:
        query_soql = query_names_soql[query_name]
        merged_soql = query_soql.replace(':param1', param1)
        context[query_name] = json.loads(sfc.fetch_dataset(merged_soql))["records"]

    doc_path = '/tmp/temp_doc.docx'
    sfc.fetch_document(documentID, doc_path)

    mdoc = TokenMerge(doc_path)
    mdoc.add_context(context)
    mdoc.merge('/tmp/out_doc.docx')

    with open('/tmp/out_doc.docx', 'rb') as f:
        rbytes = f.read()
        encoded_file = base64.b64encode(rbytes)

    payload = {
        "apikey": cloud_key,
        "inputformat": "docx",
        "outputformat": "pdf",
        "input": "base64",
        "file": encoded_file,
        "filename": 'out_doc.docx',
        "wait": True,
        "download": "inline"
    }

    c = requests.post("https://api.cloudconvert.com/convert", data=payload, stream=True)
    with open("/tmp/merged-doc.pdf", 'wb') as f:
        for chunk in c.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    upload_resp = sfc.push_document('/tmp/merged-doc.pdf', folderID)

    lambda_response = dict()
    lambda_response['statusCode'] = 200
    lambda_response['headers'] = {}
    lambda_response['body'] = json.dumps(context) + json.dumps(upload_resp)

    return lambda_response
