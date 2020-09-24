XAUTHTOKEN = ''
XUSERID = ''

import yaml
import os
import pprint
import json
from urllib.request import urlopen
from requests import get, post
from rocketauth import get_tokens, auth_login, auth_logout


def get_dm_list(token):
    #headers = {'X-Auth-Token': XAUTHTOKEN,
    #           'X-User-Id': XUSERID}
    r = get('http://localhost:3000/api/v1/im.list.everyone', headers = token)
    return r.json()

def list_dm_participants(token):
    dms = get_dm_list(token)['ims']
    for dm in dms:
        print("id: ", dm['_id'], "\tusers: ", dm['usernames'])

def get_messages(dmid, token):
    #headers = {'X-Auth-Token': XAUTHTOKEN,
    #           'X-User-Id': XUSERID}
    payload = {'roomId' : dmid}
    r = get('http://localhost:3000/api/v1/im.history', params=payload, headers = token)
    return r.json()




#(XAUTHTOKEN, XUSERID) = get_tokens()
if __name__ == '__main__':
    token = auth_login()
    menu = """
0: List all DMS
1: Get all messages from a DM
choice: """
    choice = input(menu)

    if choice == '0':
        list_dm_participants(token)
    elif choice == '1':
        choice = input('Enter ID: ')
        pprint.pprint( get_messages( choice, token ) )

    auth_logout(token)
