from PIL import Image
import requests
import base64
import os
import json

class GetVerificationCode:
    @staticmethod
    def apitruecaptcha():
        try:
            # 尝试将webp转换为png
            try:
                im=Image.open("image.webp")
                im.save('image.png')
            except:
                print("图片转换失败")
                return "0000"  # 默认返回一个验证码
            
            with open('image.png','rb') as f:
                userid = os.environ.get("USERID", "")
                apikey = os.environ.get("APIKEY", "")
                
                if not userid or not apikey:
                    print("USERID或APIKEY环境变量未设置")
                    return "0000"
                    
                image=base64.b64encode(f.read())
                url='https://api.apitruecaptcha.org/one/gettext'
                data={
                    'data':str(image,'utf-8'),
                    'userid':userid,
                    'apikey':apikey
                }
                result = requests.post(url, json=data, timeout=30)
                res=result.json()
                if 'result' in res:
                    code = res['result']
                    return code
                else:
                    print(f"验证码识别API返回异常: {res}")
                    return "0000"
        except Exception as e:
            print(f"验证码识别失败: {e}")
            return "0000"

    @staticmethod
    def ttshitu():
        try:
            # 尝试将webp转换为png
            try:
                im=Image.open('image.webp')
                im.save('image.png')
            except:
                print("图片转换失败")
                return "0000"
                
            with open('image.png','rb') as f:
                image=base64.b64encode(f.read())
                host='http://api.ttshitu.com/base64'
                headers={
                    'Content-Type':'application/json;charset=UTF-8'
                }
                codeuser = os.environ.get("CODEUSER", "")
                codepass = os.environ.get("CODEPASS", "")
                
                if not codeuser or not codepass:
                    print("CODEUSER或CODEPASS环境变量未设置")
                    return "0000"
                    
                data={
                    'username': codeuser,
                    'password': codepass,
                    'image':image.decode('utf-8')
                }
                res=requests.post(url=host,data=json.dumps(data), headers=headers, timeout=30)
                res=res.json()
                if 'data' in res and 'result' in res['data']:
                    return res['data']['result']
                else:
                    print(f"验证码识别API返回异常: {res}")
                    return "0000"
        except Exception as e:
            print(f"验证码识别失败: {e}")
            return "0000"