import os
import json
import datetime
import sys
from flask import Flask, request, redirect
from flask import make_response
from flask import jsonify
from flask_cors import CORS
import requests
import io
import hashlib


app = Flask(__name__)
CORS(app)


@app.route("/classifyGCP", methods=['POST'])
def classify_serve2():
    """Respond to incoming calls with a brief message."""

    ##resp = "Ok"

    os.system ('$env:GOOGLE_APPLICATION_CREDENTIALS="F:\data\hackprinceton\gc.json"')

    req_data = request.get_json()

    text = req_data["text"]
    author = req_data["author"]

    print (" i received " + text)
    print (" from " + author)

    combotext = author + "|" + text
    signature = hashlib.md5(combotext.encode('utf-8')).hexdigest()

    print (signature)

    ##shortcode = signature[:10]

    commandline = 'python predictMLv3.py "' + text +'" aiot-fit-xlab TCN3380722269616129492 '

    print (commandline)

    os.system(commandline)

    with open("class.txt") as fp:  
       line = fp.readline()
    cls = line.strip()

    with open("confidence.txt") as fp:  
       line = fp.readline()
    con = line.strip()


    

    url = "http://10.24.148.214:3000"

    payload = '{"name": "' + signature +'"}'
    headers = {
        'Content-Type': "application/json"
        }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)

    injson = json.loads(response.text)
   
    out_r = {}
    out_r["status"] = "ok"
    out_r["class"] = cls
    out_r["confidence"] = con
    out_r["transid"] = injson["data"]["id"]
    out_r["blockid"] = injson["data"]["blockId"]

    response = make_response(json.dumps(out_r))
    response.headers['content-type'] = 'application/json'

    return response





if __name__ == "__main__":
    app.run(debug=True, port = 8002)
    ##app.run(debug=True, host = '169.62.204.155', port = 8001)



