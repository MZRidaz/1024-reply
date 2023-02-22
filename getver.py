from PIL import Image
import requests
import base64
import os
import json

class GetVerificationCode:
    @staticmethod
    def apitruecaptcha():
        im=Image.open("image.webp")
        im.save('image.png')
        f=open('image.png','rb')
        
        userid = os.environ["USERID"]
        apikey = os.environ["APIKEY"]
        image=base64.b64encode(f.read())
        url='https://api.apitruecaptcha.org/one/gettext'
        data={
            'data':str(image,'utf-8'),
            'userid':userid,
            'apikey':apikey
        }
        result = requests.post(url, json.dumps(data))
        res=result.json()
        code = res['result']
        return code

    @staticmethod
    def ttshitu():
        im=Image.open('image.webp')
        im.save('image.png')
        f=open('image.png','rb')
        image=base64.b64encode(f.read())
        host='http://api.ttshitu.com/base64'
        headers={
            'Content-Type':'application/json;charset=UTF-8'
        }
        data={
            'username': os.environ["CODEUSER"] ,
            'password': os.environ["CODEPASS"] ,
            'image':image.decode('utf-8')
        }
        res=requests.post(url=host,data=json.dumps(data))
        res=res.text
        res=json.loads(res)
        res=res['data']['result']
        return res