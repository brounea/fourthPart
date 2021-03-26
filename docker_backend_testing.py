import requests

def testdkrbe():
    try:
        res = requests.get('http://localhost:5004/users/1')
        print(res.json())
    except requests.exceptions.ConnectionError as err:
        print('rest_app connection is refused from docker', err)
    finally:
        assert res.ok

if __name__ == "__main__":
    testdkrbe()