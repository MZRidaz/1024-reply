import requests
import re
import random
import os
import pickle
import json
import onetimepass as otp
from time import sleep
from config import config
from getver import GetVerificationCode


class AutoReply:
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    LOGIN_URL = 'https://t66y.com/login.php'
    THREAD_URL = 'https://t66y.com/thread0806.php?fid=7&search=today'

    HEADERS = {
        'Host': 't66y.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'https://t66y.com/index.php',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': USER_AGENT
    }
    LOGIN_HEADERS = {
        'Host': 't66y.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'https://t66y.com/login.php',
        'User-Agent': USER_AGENT
    }

    def __init__(self, user, password, secret):
        self.user = user
        self.password = password
        self.secret = secret
        self.session = requests.Session()
        self.cookies = None

    def login(self):
        """用户登录，包括验证码和两步验证流程"""

        # 第一步登录动作
        login_data = {
            'pwuser': self.user,
            'pwpwd': self.password,
            'step': '2'
        }

        login_response = self.session.post(self.LOGIN_URL, data=login_data, headers=self.LOGIN_HEADERS)
        response_content = login_response.content.decode('utf-8', 'ignore')

        if '登录尝试次数过多' in response_content:
            return "登录错误：次数过多，需要验证码"
        elif '賬號已開啟兩步驗證' in response_content:
            print("帐户启用了两步验证，正在请求验证码")
            return self.two_factor_authentication()

    def two_factor_authentication(self):
        """完成两步验证"""
        sleep(2)
        token = otp.get_totp(self.secret)
        auth_data = {'step': '2', 'cktime': '0', 'oneCode': str(token)}

        login_response = self.session.post(self.LOGIN_URL, data=auth_data, headers=self.LOGIN_HEADERS)

        with open(f"./{self.user}_cookies.pkl", 'wb') as cookie_file:
            pickle.dump(login_response.cookies, cookie_file)

        if '您已經順利登錄' in login_response.text:
            self.cookies = login_response.cookies
            return "登录成功"

    def fetch_today_threads(self):
        """获取今天的帖子列表"""
        response = self.session.get(self.THREAD_URL, headers=self.HEADERS)
        content = response.content.decode('utf-8', 'ignore')

        # 使用正则表达式匹配帖子链接
        thread_pattern = r'htm_data/\w+/\w+/\w+.html'
        threads = re.findall(thread_pattern, content)
        return threads

    def reply_to_thread(self, thread_url, message):
        """自动回复帖子"""
        reply_data = {
            'message': message
        }
        reply_response = self.session.post(thread_url, data=reply_data, headers=self.HEADERS)
        return reply_response.content.decode('utf-8', 'ignore')

    @staticmethod
    def generate_random_message():
        """生成随机回复内容"""
        return f"感谢分享！支持！ -- {random.randint(1, 1000)}"


if __name__ == "__main__":
    # 环境变量读取
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")
    secret = os.getenv("SECRET")

    bot = AutoReply(user, password, secret)

    login_status = bot.login()
    print("登录状态:", login_status)

    # 获取今日帖子
    today_threads = bot.fetch_today_threads()
    for thread in today_threads[:5]:  # 限制操作帖子的数量
        print(f"回复帖子: {thread}")
        message = AutoReply.generate_random_message()
        bot.reply_to_thread(f'https://t66y.com/{thread}', message)
        sleep(random.randint(10, 30))