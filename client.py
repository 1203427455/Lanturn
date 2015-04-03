import requests

r = requests.post('http://192.168.1.10:8080/')
print dir(r)
print r.headers
print r.content