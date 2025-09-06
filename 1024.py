import requests
import random
import re
import os
import json
import pickle
from time import sleep
from getver import GetVerificationCode
from config import config

class Autoreply:
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/90.0.4430.212 Safari/537.36"
    LOGIN_URL = 'https://t66y.com/login.php'
    THREAD_URL = 'https://t66y.com/thread0806.php?fid=7&search=today'

    def __init__(self, user, password, secret):
        self.user = user
        self.password = password
        self.secret = secret
        self.session = requests.Session()

    def login(self):
        # 用户登录
        data = {'pwuser': self.user, 'pwpwd': self.password, 'step': '2'}
        response = self.session.post(self.LOGIN_URL, data=data)
        content = response.content.decode('utf-8', 'ignore')
        if '尝试次数过多' in content:
            return "需输入验证码"
        elif '验证' in content:
            return self.two_factor_auth()
        return "登录成功"

    def two_factor_auth(self):
        # 两步验证
        response = self.session.post(self.LOGIN_URL, data={'oneCode': "example_totp_code"})
        if '顺利登录' in response.text:
            return "登录完成"

    def fetch_today_threads(self):
        # 获取今日帖子
        response = self.session.get(self.THREAD_URL)
        pattern = r'htm_data/\w+/\w+/\w+.html'
        return re.findall(pattern, response.text)

    def post_reply(self, thread_url, reply_content):
        # 回帖
        data = {'message': reply_content, 'action': 'reply'}
        response = self.session.post(thread_url, data=data)
        if '回复成功' in response.text:
            return "回复成功"
        return "回复失败"

    @staticmethod
    def generate_reply():
        replies = ['感谢分享', '内容精彩', '学习了！', '赞一个', '很有帮助']
        return random.choice(replies)

if __name__ == "__main__":
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")
    secret = os.getenv("SECRET")

    bot = Autoreply(user, password, secret)
    login_status = bot.login()
    if login_status == "需输入验证码":
        GetVerificationCode.apitruecaptcha()  # 自动处理验证码
    elif login_status == "登录成功":
        threads = bot.fetch_today_threads()
        for thread in threads:
            reply = Autoreply.generate_reply()
            print(bot.post_reply(thread, reply))
            sleep(random.randint(5, 15))  # 防止频繁操作触发限制