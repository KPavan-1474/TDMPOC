import json
import collections
import mysql.connector
import requests

def calling_api():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MySQL$1474",
    database="POCTDM"
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM customer")

    rows = mycursor.fetchall()

    objects_list = []
    d=dict()
    for row in rows:
        d = collections.OrderedDict()
        d['id'] = row[0]
        d['Name'] = row[1]
        d['Age'] = row[2]
        d['SSN'] = row[3]
        d['OrderId'] = row[4]
        objects_list.append(d)

    d={"database-connect": "false", "type": "mask", "rows": 100, "data": objects_list,
    "mask-columns": [
    "ssn",
    
    ]
    }
#"ccn"
    j = json.dumps(d)

    print(j)

    url = "http://127.0.0.1:5000/clone_json"
    headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
    response = requests.post(url, data= j, headers=headers)

    print(response.text)