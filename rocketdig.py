XAUTHTOKEN = ''
XUSERID = ''

import yaml
import os
import pprint
import json
from urllib.request import urlopen
from requests import get, post
from rocketauth import get_tokens


def get_dm_list():
    headers = {'X-Auth-Token': XAUTHTOKEN,
               'X-User-Id': XUSERID}
    r = get('http://localhost:3000/api/v1/im.list.everyone', headers = headers)
    return r.json()

def list_dm_participants():
    dms = get_dm_list()['ims']
    for dm in dms:
        print("id: ", dm['_id'], "\tusers: ", dm['usernames'])

def get_messages(dmid):
        headers = {'X-Auth-Token': XAUTHTOKEN,
                   'X-User-Id': XUSERID}
        payload = {'roomId' : dmid}
        r = get('http://localhost:3000/api/v1/im.history', params=payload)
        return r.json()




(XAUTHTOKEN, XUSERID) = get_tokens()
if __name__ == '__main__':
    menu = """
0: List all DMS
1: Get all messages from a DM
choice: """
    choice = input(menu)

    if choice == '0':
        list_dm_participants()
    elif choice == '1':
        choice = input('Enter ID: ')
        pprint.pprint( get_messages( choice ) )
