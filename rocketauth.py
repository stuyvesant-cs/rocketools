from requests import get, post
import json
import getpass

#set tokens from file
def get_tokens():
    tokenf = input('token file: ')
    f = open(tokenf)
    lines = f.read().split('\n')
    f.close()
    auth = lines[0].split(',')[1]
    uid = lines[1].split(',')[1]
    return { 'X-User-Id' : uid, 'X-Auth-Token' : auth }

def auth_login():
    name = input("Enter username: ")
    passw = getpass.getpass()
    data = { 'user' : name, 'password': passw }
    r = post('http://localhost:3000/api/v1/login', data = json.dumps(data))
    data = r.json()['data']
    return { 'X-User-Id' : data['userId'], 'X-Auth-Token' : data['authToken'] }

def auth_logout( token ):
    r = post('http://localhost:3000/api/v1/logout', headers = token)
    print(r.text)
    

if __name__ == '__main__':
    choice = """
0: Authenticate with name/password
1: Autheticate with token file
(default 0): 
"""
    if choice == '1':
        token = get_tokens()
    else:
        token = auth_login()
    print(token)
    if choice != '1':
        auth_logout(token) 
