# rocketools - Rocket REST API Tools

## General information

* These are all tools for use with the Rocket Chat Rest API: https://docs.rocket.chat/api/rest-api
* You will need to gene an access token on the given server: https://docs.rocket.chat/api/rest-api/personal-access-tokens
  * Put this info in a file called **token.txt** that looks like so:
  ```
  XAUTHTOKEN,token
  XUSERID,id
  ```
* Currently, thses tools adesigned to be run from the server hosting the rocketchat instance.
* There is a rocketchat python api library: https://github.com/jadolg/rocketchat_API
* Example REST Calls:
```
#/bin/bash
curl -H "X-Auth-Token: " \
     -H "X-User-Id: " \
     http://localhost:3000/api/v1/emoji-custom.list
curl -H "X-Auth-Token: " \
     -H "X-User-Id: " \
     -F "emoji=@7zYM751.png" \
     -F "name=bender" \
     -F "alias=" \
     http://localhost:3000/api/v1/emoji-custom.create
```

## rocketmoji
* Currently has the following features:
  * List all custom emojis
  * Batch add all emojis from a yaml file (examples found here: https://github.com/lambtron/emojipacks)
  * Remove all custom emojis
* Runs as an interactive *python3* script.
* Uses the requests module except for uploading new emojis. That call seems to fail, so instead it creates a `curl` command and runs it via `os.system`.
* Does not use the rocketchat python api because at the moment it does not contain any emoji related fucntions.
