XAUTHTOKEN = ''
XUSERID = ''
"""
use emoji yaml files like the ones found here:
https://github.com/lambtron/emojipacks
"""

import yaml
import os
import pprint
import json
from copy import copy
from urllib.request import urlopen
from requests import get, post
from rocketauth import auth_choice, auth_logout

#retrieve emoji yaml file
def get_emoji_yaml( emoji_url ):
    emoji_response = urlopen(emoji_url)
    emoji_yaml = yaml.load(emoji_response.read())
    return emoji_yaml

def batch_save_emojis( emoji_yaml, token ):
    #make dir for temp saving files
    tmpdir = "/tmp/" + emoji_yaml['title']
    os.mkdir(tmpdir)

    emojis = emoji_yaml['emojis']
    emoji_files = []
    print(emojis)
    for emoji in emojis:
        name = emoji['name']
        url = emoji['src']
        filename = name + url[url.rfind('.'):]
        # print(name)
        # print(url)
        # print(filename)
        filename = tmpdir + '/' + filename
        f = open(filename, 'wb')
        response = get(url)
        f.write(response.content)
        emoji_files.append( (filename, name) )
    for emoji in emoji_files:
        emoji_create_api_call(emoji[0], emoji[1], token)

    #get rid of emoji files
    os.system('rm -rf ' + tmpdir)

def batch_add_emojis_dir(dirname, token):
    for emoji in os.listdir(dirname):
        fname = dirname + '/' + emoji
        ename = emoji[:emoji.rfind('.')]
        emoji_create_api_call(fname, ename, token)

'''
ideally, should be able to make API call using requests.
Have not succedded, should look something like:

headers = {'X-Auth-Token': '',
           'X-User-Id': ''}
data = {'emoji': open('bender.png', 'rb'),
        'name': 'bender' }
r = requests.post('http://localhost:3000/api/v1/emoji-custom.create', data=data, headers = headers)
r.txt

until that is working, using os.system instead
'''
def emoji_create_api_call(emojifile, emojiname, token):
    cmd = 'curl -H "X-Auth-Token: %s" '%token['X-Auth-Token']
    cmd+= '-H "X-User-Id: %s" '%token['X-User-Id']
    cmd+= '-F "emoji=@'
    cmd+= emojifile + '" '
    cmd+= '-F "name=' + emojiname + '" '
    cmd+= 'http://localhost:3000/api/v1/emoji-custom.create'
    print(emojiname)
    print(cmd)
    print()
    os.system(cmd)

#return dictionary of emojis including rocket generated emoji ids
def get_emoji_list(token):
    #headers = {'X-Auth-Token': XAUTHTOKEN,
    #           'X-User-Id': XUSERID}
    headers = copy(token)
    headers.pop('type')
    r = get('http://localhost:3000/api/v1/emoji-custom.list', headers = headers)
    return r.json()

def remove_all_emojis( emoji_list, token ):
    #headers = {'X-Auth-Token': XAUTHTOKEN,
    #           'X-User-Id': XUSERID,
    headers = copy(token)
    headers.pop('type')
    headers["Content-type"] = "application/json"
    for emoji in emoji_list:
        print(emoji)
        emoji_id = emoji['_id']
        data = {"emojiId" : emoji_id}
        r = post('http://localhost:3000/api/v1/emoji-custom.delete', data = json.dumps(data), headers = headers)
        print(r.text)


#(XAUTHTOKEN, XUSERID) = get_tokens()
if __name__ == '__main__':
    token = auth_choice()
    menu = """
0: list custom emojis
1: batch add emojis from yaml
2: batch add emojis from folder
3: batch delete all custom emojis
choice: """
    choice = input(menu)

    if choice == '0':
        pprint.pprint(get_emoji_list( token ))
    elif choice == '1':
        emoji_yaml_url = input("URL for YAML file: ")
        emoji_yaml = get_emoji_yaml(emoji_yaml_url)
        batch_save_emojis( emoji_yaml, token )
    elif choice == '2':
        dirname = input('directory: ')
        batch_add_emojis_dir(dirname, token)
    elif choice == '3':
        emoji_list = get_emoji_list( token )
        emoji_list = emoji_list['emojis']['update']
        remove_all_emojis(emoji_list, token)\
            
    if token['type'] == 'login':
        auth_logout(token)
