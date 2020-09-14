TOKEN_FILE = 'token.txt'


#set tokens from file
def get_tokens(tokenf = TOKEN_FILE):
    f = open(tokenf)
    lines = f.read().split('\n')
    f.close()
    auth = lines[0].split(',')[1]
    uid = lines[1].split(',')[1]
    return (auth, uid)




