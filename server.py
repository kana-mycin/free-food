import requests
from requests_oauthlib import OAuth1
from flask import Flask, request
app = Flask(__name__)
#will need to import/query the database
GRAPH_URL = "https://graph.facebook.com/search?q=berkeley&type=event&access_token="
ACCESS_TOKEN = "CAACEdEose0cBAEFpiuPsAP7gK0TdPgYl8Eyan8pqYWZAs3ePBAf34gvUwhUcxhtSvCsSkwVgT76IBdx2Ie5Ply8b6UJZCyu6ZCVoTHn6hFUNl6MZCr5cUOHojpP1Bk5nfRaRi7GW354dNin3GHfBXLoKSNwb8TI7OTPkqoBDJ0IkpOwUp9CQrMDtG6SrzwlPFCb0KzZCcZBWkSEnZA2po6G"
KEY = "902297456471999"
SECRET = "c399b07485853239b90cd51bf0cdad77"
EVENT_URL1 = "https://graph.facebook.com/"
EVENT_URL2 = "?access_token="
auth = OAuth1(KEY, SECRET)

@app.route("/")
def hello():
    return app.send_static_file("index.html")

@app.route("/api/freefood", methods=["POST"])
def receive_request():
    #make a request to server, save as string
    url = GRAPH_URL+ACCESS_TOKEN
    output = requests.get(url, auth=auth).content.decode(encoding = 'UTF-8')
    id_list = find_ids(output)
    print(events_from_ids(id_list))

if __name__ == "__main__":
    app.run()

def find_ids(string):
    lst = string.split("\"id\":")
    lst = lst[1:]
    count = 0
    while count < len(lst):
        substr = lst[count]
        lst[count] = substr[1:substr.find("\"",1)]
        count+=1
    return lst

def events_from_ids(id_list):
    for event_id in id_list:
        url = EVENT_URL1+event_id+EVENT_URL2+ACCESS_TOKEN
        print(requests.get(url, auth=auth).content.decode(encoding = 'UTF-8'))
