import requests, json
import pandas as pd
from requests_oauthlib import OAuth1
#will need to import/query the database
GRAPH_URL = "https://graph.facebook.com/search?q=berkeley&type=event&access_token="
ACCESS_TOKEN = "CAACEdEose0cBAJq8OQlrFp9pY9b9WEEvCzQrMfZA30coxqZCqoOJ5eYMc7hgprgiuUPkmjSLlYIC7lulhIZB3uLTriOHhWhj1ZA60XMmYUePcvmAQVtrefwxUZCfzK3dDx46ErCcbCiarE2oTpchBfZBGu8qFZBp59RPf9a1tsUmLfzmuImEMatBSsNwrGnFx7nkKQGd6PQHYLpdRmPA4we"
KEY = "902297456471999"
SECRET = "c399b07485853239b90cd51bf0cdad77"
DOMAIN = "https://graph.facebook.com"
EVENT_URL2 = "?access_token="
auth = OAuth1(KEY, SECRET)
strings = ["free", "Free", "FREE"]

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

url = GRAPH_URL+ACCESS_TOKEN
output = requests.get(url, auth=auth).content.decode(encoding = 'UTF-8')
id_list = find_ids(output)
minilist = id_list[:10]
event_list = events_from_ids(minilist)
for i in event_list:
    del i['headers']
events = list()
for i in event_list:
    events.append(json.loads(i['body']))
df = pd.DataFrame(events)
print(df)



#event_split = event_string.split("\"id\":")
#print(event_split)
#name_list = parse_field(event_list, "name")
#owner_list = parse_field(eventlist, "owner")
#venue_list = parse_field(event_list, "venue")
#start_list = parse_field(event_list, "start_time")
#print(owner_list)


#want name, owner, venue, and start time
