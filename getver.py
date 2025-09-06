from PIL import Image
import requests
import base64
import os
import json

class GetVerificationCode:
    @staticmethod
    def apitruecaptcha():
        # TrueCaptcha 验证码服务
        im = Image.open("image.webp").convert("RGB")
        im.save('image.png')
        with open('image.png', 'rb') as f:
            userid = os.getenv("USERID")
            apikey = os.getenv("APIKEY")
            image = base64.b64encode(f.read())
        url = 'https://api.apitruecaptcha.org/one/gettext'
        data = {'data': str(image, 'utf-8'), 'userid': userid, 'apikey': apikey}
        response = requests.post(url, json=data).json()
        return response['result']

    @staticmethod
    def ttshitu():
        # TTSHITU 验证码服务
        im = Image.open('image.webp').convert("RGB")
        im.save('image.png')
        with open('image.png', 'rb') as f:
            image = base64.b64encode(f.read())
        url = 'http://api.ttshitu.com/base64'
        data = {
            'username': os.getenv("CODEUSER"),
            'password': os.getenv("CODEPASS"),
            'image': image.decode('utf-8')
        }
        response = requests.post(url, json=data).json()
        return response['data']['result']