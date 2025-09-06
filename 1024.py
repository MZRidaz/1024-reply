import traceback
import random
import requests

# from typing import Optional
from bs4 import BeautifulSoup
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
from datetime import datetime, timedelta
from time import sleep
from sel_def_logger import MyLog

class postreply1024:
    _UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0"
    _mylogg = MyLog().logger
    def __init__(self, host,cookies: str,app_id,app_secret,user_id,template_id,target_url):
        self._host=host
        self._cookies: str = cookies
        self._app_id =app_id
        self._app_secret=app_secret
        self._user_id=user_id
        self._template_id=template_id
        self._target_url=target_url

    def _get_random_color(self):
        return "#%06x" % random.randint(0, 0xFFFFFF)
    def _send_to_mp(self,msg:str):
        tday = datetime.now()+timedelta(hours = 8)
        tday=tday.strftime("%Y-%m-%d %H:%M:%S")
        client = WeChatClient(self._app_id, self._app_secret)
        wm = WeChatMessage(client)
        data = {
            "date": {"value": format(tday), "color": self._get_random_color()},
            "re": {"value": msg, "color": self._get_random_color()},
        }
        res = wm.send_template(self._user_id, self._template_id, data)

    def _report_signin_failed(self,msg:str):
        tday = datetime.now()+timedelta(hours = 8)
        tday=tday.strftime("%Y-%m-%d %H:%M:%S")
        client = WeChatClient(self._app_id, self._app_secret)
        wm = WeChatMessage(client)
        data = {
            "date": {"value": format(tday), "color": self._get_random_color()},
            "re": {"value": msg, "color": self._get_random_color()},
        }
        res = wm.send_template(self._user_id, '1gUyGk6YJWp3vkdsIVbf571M-O5SK2mPCq28QG2xKrA', data)

    #获取回复内容
    def _getword(self,wordlist, num):
        wordlist_new = random.sample(wordlist, len(wordlist))
        if num > len(wordlist):
            for _ in range(int(num / len(wordlist)) - 1):
                wordlist_sam = random.sample(wordlist, len(wordlist))
                if wordlist_new[-1] == wordlist_sam[0]:
                    wordlist_sam[0], wordlist_sam[-1] = wordlist_sam[-1], wordlist_sam[0]
                wordlist_new.extend(wordlist_sam)
            if num % len(wordlist):
                wordlist_sam = random.sample(wordlist, num % len(wordlist))
                if wordlist_new[-1] == wordlist_sam[0]:
                    wordlist_sam[0] = wordlist_new[-2]
                wordlist_new.extend(wordlist_sam)
        else:
            wordlist_new = random.sample(wordlist, num)
        return wordlist_new

    #获取列表
    def _getlist(self):
        list_url = f"{self._host}/thread0806.php?fid=7"

        with requests.session().get(
            list_url,
            headers={'cookie': self._cookies,
                     'user-agent': self._UA,
                     'content-type': 'application/json;charset=UTF-8',
                     'Upgrade-Insecure-Requests': '1',
                     },
        ) as r:
            # return  r.text.encode('utf-8').decode('latin1')
            return  BeautifulSoup(r.content, 'html.parser')

    def _visitthread(self,url):
        pageurl = f"{self._host}{url}"

        with requests.session().get(
            pageurl,
            headers={'cookie': self._cookies,
                     'user-agent': self._UA,
                     'content-type': 'application/json;charset=UTF-8',
                     'Upgrade-Insecure-Requests': '1',
                     },
        ) as r:
            return  BeautifulSoup(r.content, 'html.parser')

    #回复帖子
    def _postreply(self,atc_title,atc_content,tidurl,tid):
        posturl=f"{self._host}/post.php?"
        referer=f"{self._host}{tidurl}"
        payload={
            'atc_usesign':'1',
            'atc_convert':'1',
            'atc_autourl':'1',
            'atc_title':atc_title,
            'atc_content':atc_content,
            'step':'2',
            'action':'reply',
            'fid':'7',
            'tid':tid,
            'page':'h',
            'pid':'',
            'article':'',
            'touid':'',
            'verify':'verify',
            'Submit':'正在提交回覆..'
        }

        with requests.session().post(
            posturl,
            headers={'cookie': self._cookies,
                     'referer': referer,
                     'origin': self._host,
                     'user-agent': self._UA,
                     'content-type': 'application/x-www-form-urlencoded',
                     'Upgrade-Insecure-Requests': '1',
                     },
            data=payload
        ) as r:
            return  BeautifulSoup(r.content, 'html.parser')


    def _reply(self):
        n1 = 3
        while n1 > 0:
            n1 = n1 - 1
            sleep(3)
            res3 = self._visitthread(self._target_url)
            if res3.text.find("快速回帖")!=-1:
                break
        else:
            # self._send_to_mp("签到帖子访问失败！")
            print("签到帖子访问失败！")

        # atc_title = res3.select('title')[0].text
        atc_title = res3.select('input[name="atc_title"]')[0].attrs['value']
        atc_content = "今日签到"

        tid = self._target_url.split('/')[-1].replace(".html", "")
        # wait = int(random.uniform(1, 3) * 1000) / 1000
        # sleep(wait)
        time1 = datetime.now() + timedelta(hours=8)
        time2 = datetime(time1.year, time1.month, time1.day+1, 0, 0, 0, 0)
        wait = (time2 - time1).seconds+1
        sleep(wait)
        n2 = 3
        while n2 > 0:
            n2 = n2-1
            replyres2 = self._postreply(atc_title, atc_content, self._target_url, tid)
            if replyres2.text.find("發貼完畢點擊進入主題列表") != -1:
                sign_res = "签到成功"
                # self._send_to_mp("签到回帖成功！")
                break
        else:
            sign_res = "签到失败"
            # self._report_signin_failed("签到回帖失败！")
            return

        wait = int(random.uniform(1, 3) * 1000) / 1000
        sleep(wait)
        res1 = self._getlist()
        if res1.text.find("普通主題")==-1:
            self._send_to_mp("获取列表失败")
            return

        res1 = res1.select('#tbody tr.tr3.t_one.tac td.tal h3 a')
        randn = random.randint(1, 10)
        tidurl = res1[randn].get("href")
        tid = res1[randn].get("id")[1:]
        atc_title = res1[randn].text

        while randn<20:
            if res1[randn].find('font',color="orange") != None or ('求片求助貼' in atc_title) or ('统计' in atc_title) or atc_title == "":
                randn = randn + 1
                tidurl = res1[randn].get("href")
                tid = res1[randn].get("id")[1:]
                atc_title = "Re:" + res1[randn].text
            else:
                break
            # if ('求片求助貼' in atc_title) or ('[活动]' in atc_title) or ('[领奖帖]' in atc_title) or atc_title == "":
            #     randn=randn+1
            #     tidurl = res1[randn].get("href")
            #     tid = res1[randn].get("id")[1:]
            #     atc_title = res1[randn].text
            # else:
            #     break
        else:
            raise RuntimeError('尝试次数过多')

        wait=int(random.uniform(1,3)*1000)/1000
        sleep(wait)
        res2=self._visitthread(tidurl)
        if res2.text.find("快速回帖")==-1:
            self._send_to_mp("前置帖子访问失败！")


        wordlist = ['忽忘提肛，感谢分享',
                    '感谢楼主辛苦分享',
                    '不管怎么说先冲为敬',
                    '感谢分享',
                    '大佬辛苦，感谢分享',
                    '看看大佬的分享',
                    '精彩帖子，感谢楼主']
        atc_content=random.choice(wordlist)

        wait=int(random.uniform(10,20)*1000)/1000
        sleep(wait)
        replyres1 = self._postreply(atc_title, atc_content,tidurl, tid)
        if replyres1.text.find("發貼完畢點擊進入主題列表")!=-1:
            reply_res="更新回帖成功"
            # self._send_to_mp("更新回帖成功！")
        else:
            reply_res = "更新回帖失败"
            # self._send_to_mp("更新回帖失败！")
            return
        self._send_to_mp(sign_res+","+reply_res)

    def run(self):
        try:
            self._reply()
        except BaseException:
            self._mylogg.error('program error!')
            self._report_signin_failed(traceback.format_exc())


