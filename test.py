import requests
from requests_oauthlib import OAuth1
#will need to import/query the database
GRAPH_URL = "https://graph.facebook.com/search?q=berkeley&type=event&access_token="
ACCESS_TOKEN = "CAACEdEose0cBAJC7Nx33jKgP5aUeEsr3jvNj4rosC1EVyAddsRBxgCmwDvVN3gYXqS37KuZCX22ZCTUoXavU2QZA5zVenT9mSEg3ZCJoNyW5UIWmkwja60ZBpFY67YrleA1EBeRl9cEmRtsNpeOSaHzZAZA3wFTgJ9pJEsznTMqazdit9wX7iAeDU0Sa9B6D1aqI2XxFQHytIZATWcs67usy"
KEY = "902297456471999"
SECRET = "c399b07485853239b90cd51bf0cdad77"
EVENT_URL1 = "https://graph.facebook.com/"
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
    for event_id in id_list:
        url = EVENT_URL1+str(event_id)+EVENT_URL2+ACCESS_TOKEN
        event_list.append(requests.get(url, auth=auth).content.decode(encoding = 'UTF-8'))
        count+=1
    print("done")
    return [x for x in event_list if contains_query(x)]

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
minilist = id_list[:500]
eventlist = events_from_ids(minilist)
print(eventlist)
#name_list = parse_field(event_list, "name")
#owner_list = parse_field(eventlist, "owner")
#venue_list = parse_field(event_list, "venue")
#start_list = parse_field(event_list, "start_time")
#print(owner_list)


#want name, owner, venue, and start time
