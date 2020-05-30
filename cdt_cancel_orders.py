#!/usr/bin/env python3

import csv
import re
import requests

USERNAME = ''
TAURUS_COOKIE = ''

CREATE_SESSION_URL = 'http://ncdt1-slb.centertel.pl:7004/jbpm/soap?operation.invoke=createSession'
TRANSFER_TO_NODE_URL = 'http://ncdt1-slb.centertel.pl:7004/jbpm/soap?operation.invoke=transferToNode'


def get_session_key(username, password):
    response = requests.get(f'{CREATE_SESSION_URL}&username={username}&password={password}')
    result = re.search(r'&lt;result\s*xsi:type="xsd:string"&gt;([^;&]+)&lt;/result&gt;', response.text)
    session_key = result.group(1)
    return session_key


def transfer_to_node(session_key, document_id, node_name):
    requests.get(f'{TRANSFER_TO_NODE_URL}&sessionKey={session_key}&documentId={document_id}&nodeName={node_name}')


SESSION_KEY = get_session_key(USERNAME, TAURUS_COOKIE)

with open('data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    i = 1
    for row in csv_reader:
        DOCUMENT_ID = row[0].strip()
        NODE_NAME = 'plbCancelOffer'
        transfer_to_node(SESSION_KEY, DOCUMENT_ID, NODE_NAME)
        print(f'{i}. {DOCUMENT_ID} anulowane!')
        i += 1
