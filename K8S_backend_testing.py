import requests
import re

def getaddrs():
    addrs = ''
    try:
        with open('k8s_url.txt', 'r', encoding='utf-8') as file:
            text = file.read()
            url = re.search("(?P<url>https?://[^\s]+)", text).group("url")
            print(addrs)
    except IOError as e:
        print("File can not be found:", e)
    finally:
        file.close()
        return addrs


def testk8s():
    res = requests.get( getaddrs() + '/users/1')
    if res.ok:
        print(res.json())
    else:
        print(res.status_code)
        print(res.json())

testk8s()