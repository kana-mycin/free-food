import requests, json
import pandas as pd
from requests_oauthlib import OAuth1
#will need to import/query the database
GRAPH_URL1 = "https://graph.facebook.com/search?q="
GRAPH_URL2 = "&type=event&access_token="
ACCESS_TOKEN = "CAACEdEose0cBAGesEp44klGz3zejNkNWojoczFvjW5OCyDOmIwL0UTZBm24KlFMKHcBodKVDDjZAemmz4OqffbOhQsZBaNq0qZBlR0jemUchem9kSsmCr0BceZArO81Y16nfZBMEmnbGOrpHcX9hWnWXqxaS7ng9puyknS41gleJkwYH5EpWZCGJ6fXYOvCtr2HSlVU6aLMxRrasvPCE8o4"
KEY = "902297456471999"
SECRET = "c399b07485853239b90cd51bf0cdad77"
DOMAIN = "https://graph.facebook.com"
EVENT_URL2 = "?access_token="
auth = OAuth1(KEY, SECRET)
strings = ["free food", "Free food", "FREE FOOD"]
from flask import Flask, request, render_template
app = Flask(__name__)

def contains_query(string):
    for s in strings:
        if string.find(s) > -1:
            return True
    return False

def find_ids(string):
    lst = string.split("\"id\":")
    lst = lst[1:]
    count = 0
    while count < len(lst):
        substr = lst[count]
        lst[count] = int(substr[1:substr.find("\"",1)])
        count+=1
    return lst

def events_from_ids(id_list):
    event_list = list()
    count = 0
    batch = list()
    last = False
    for event_id in id_list:
        last = (event_id==id_list[-1])
        url = str(event_id)
        batch.append({"method":"GET", "relative_url":url})
        count+=1
        if count == 50 or last:
            data = {"access_token":ACCESS_TOKEN, "batch":json.dumps(batch)}
            event_list.extend(requests.post(DOMAIN, params=data).json())
            count = 0
            batch = list()
    return event_list

def parse_field(event_list, field_name):
    field_list = list()
    count = 0
    search_token = "\"" + field_name + "\":"
    for event in event_list:
        first = event.find(search_token) #might need some editing here
        if first == -1:
            field_list[count] = "--"
        else:
            end_token = ",\""
            last = event.find(end_token, first)
            field_list.append(event[first:last])
        count+=1
    return field_list

def grab_events(loc_string):
    url = GRAPH_URL1+loc_string+GRAPH_URL2+ACCESS_TOKEN
    output = requests.get(url, auth=auth).content.decode(encoding = 'UTF-8')
    id_list = find_ids(output)
    minilist = id_list
    event_list = events_from_ids(minilist)
    return event_list

@app.route("/")
def hello():
    return app.send_static_file("index.html")

@app.route("/api/freefood", methods=["POST", "GET"])
def receive_request():
    event_list = grab_events(request.form['area'])
    for i in event_list:
        del i['headers']
    events = list()
    for i in event_list:
        events.append(json.loads(i['body']))
    print(events)
    if len(events)==0:
        return render_template("results.html", events=[])
    events = [x for x in events if 'description' in x and contains_query(x['description'])]
    df = pd.DataFrame(events)
    print(df)
    return render_template("results.html", events=events)

if __name__ == "__main__":
    app.run(debug=True)
