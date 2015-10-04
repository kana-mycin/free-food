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

batch = {"method":"GET", "relative_url":"search?q=" + "berkeley"+"&type=event"}
output = requests.post(DOMAIN, params={"access_token":ACCESS_TOKEN, "batch":json.dumps(batch)})
print(output.json())