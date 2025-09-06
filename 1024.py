import requests
import re
import random
import onetimepass as otp
from time import sleep
import os
from getver import GetVerificationCode
from multiprocessing import Pool
from config import config
import pickle
import json
import sys

class Autoreply:
    result=None
    over=False
    flag=False
    UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    loginurl = 'https://t66y.com/login.php'
    url='https://t66y.com/thread0806.php?fid=7&search=today'
    headers={
        'Host': 't66y.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'https://t66y.com/index.php',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': UserAgent
    }
    headers1={
        'Host': 't66y.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'https://t66y.com/login.php',
        'User-Agent': UserAgent
    }

    def __init__(self,user,password,secret):
        self.user= user
        self.password= password
        self.secret =secret
        self.s=requests.Session()

    def login1(self):
        sleep(2)
        Err=None
        data={
                'pwuser': self.user,
                'pwpwd':  self.password,
                'hideid': '0',
                'cktime': '0',
                'forward': 'https://t66y.com/post.php?',
                'jumpurl': 'https://t66y.com/post.php?',
                'step': '2'
        }
        try:
            login=self.s.post(self.loginurl,headers=self.headers,data=data)
            if login.content.decode('gbk','ignore').find('登录尝试次数过多')!=-1:
                login=login.content.decode('gbk','ignore')
            else:
                login=login.content.decode('utf-8','ignore')
                
            if login.find('登录尝试次数过多')!=-1:
                Err='登录尝试次数过多,需输入验证码'
                return Err
            elif login.find('賬號已開啟兩步驗證')!=-1:
                Err='賬號已開啟兩步驗證'
                return Err
            return None
        except Exception as e:
            print(f"登录请求失败: {e}")
            return "登录请求失败"

    def login2(self):
        sleep(2)
        my_token = otp.get_totp(self.secret)
        data={
        'step': '2',
        'cktime': '0',
        'oneCode': str(my_token)
        }
        try:
            login=self.s.post(self.loginurl,headers=self.headers,data=data)
            with open(f"./{self.user}", 'wb') as f:
                pickle.dump(self.s.cookies, f)
            self.cookies=self.s.cookies
            login=login.content.decode('utf-8','ignore')
            if login.find('您已經順利登錄')!=-1:
                res='已經順利登錄'
                return res
            return "登录失败"
        except Exception as e:
            print(f"两步验证失败: {e}")
            return "两步验证失败"
    
    def updateCookies(self, cookie):
        self.s.cookies.update(cookie)
        self.cookies = self.s.cookies
   
    def verifyLoginSuc(self):
        try:
            index = self.s.get('https://t66y.com/index.php', headers = {
                'Host': 't66y.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': self.UserAgent
            })
            index = index.content.decode('utf-8','ignore')
            if index.find('上次登錄時間')!=-1:
                print('cookie有效登录')
                return True
            print('cookie无效登录, 切换为密码登录')
            return False
        except Exception as e:
            print(f"验证登录状态失败: {e}")
            return False
        
    def getcookies(self):
        return self.cookies

    def getverwebp(self):
        code=random.uniform(0,1)
        code=round(code,16)
        vercodeurl='https://t66y.com/require/codeimg.php?'+str(code)
        try:
            image=self.s.get(vercodeurl,headers=self.headers1)
            with open('image.webp','wb') as f:
                f.write(image.content)
            return True
        except Exception as e:
            print(f"获取验证码失败: {e}")
            return False

    def inputvercode(self,vercode):
        sleep(2)
        vercode=vercode
        data={
            'validate': vercode
        }
        try:
            login=self.s.post(self.loginurl,data=data,headers=self.headers1)
            login=login.content.decode('utf-8','ignore')
            if login.find('驗證碼不正確')!=-1:
                Err='验证码不正确，请重新输入'
                return Err
            return None
        except Exception as e:
            print(f"验证码提交失败: {e}")
            return "验证码提交失败"

    def gettodaylist(self):
        black_list=[]
        pat=('htm_data/\w+/\w+/\w+.html')
        try:
            con=self.s.get(self.url,headers=self.headers)
            con = con.content.decode('utf-8','ignore')
            self.web_page=con
            theme=con.find('普通主題')

            match=re.findall(pat,con[theme:])
            self.match=match
            if  config.get('Forbid',False):
                remove_list=[]
                self.getModerator()
                content=con[theme:]
                pat='class="bl">(.*)?</a>'
                all_user=re.findall(pat,content)
                pat='<h3><a href="([\s\S]*?)"'
                self.match=re.findall(pat,content)
                print('帖子数量为:'+str(len(all_user)))
                if len(all_user)!=len(self.match):
                    print('移除版主列表功能失效，请重试或者联系开发者更新')
                    return []
                for i in range(len(all_user)):
                    if all_user[i] in self.moderator_list:
                        remove_list.append(self.match[i])
                for data in remove_list:
                    print('移除的版主帖子为:'+data)
                    self.match.remove(data)
                print('版主帖子移除完毕')
            return self.match
        except Exception as e:
            print(f"获取今日列表失败: {e}")
            return []

    def getModerator(self):
        try:
            moderator=self.web_page.find('版主')
            moderator=self.web_page[moderator:moderator+800]
            pat='username=(\w+)'
            moderator_list=re.findall(pat,moderator)
            print('版主列表:'+','.join(moderator_list))
            self.moderator_list=moderator_list
        except Exception as e:
            print(f"获取版主列表失败: {e}")
            self.moderator_list = []


    @staticmethod
    def getonelink(todaylist):
        if not todaylist:
            return None, None
        geturl=''
        m=random.randint(0,len(todaylist)-1)
        geturl='https://t66y.com/'+todaylist[m]
        tid=todaylist[m][16:len(todaylist[m])-5]
        todaylist.remove(todaylist[m])
        return geturl,tid

    @staticmethod
    def browse(geturl,cookies):
        headers={
        'Host': 't66y.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'https://t66y.com/index.php',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': Autoreply.UserAgent
        }
        try:
            res=requests.get(url=geturl,headers=headers,cookies=cookies, timeout=10)
            reply_id = re.findall("<a name=#(\d+)><\/a>", res.text)
            if len(reply_id)==0:
                return None
            else:
                return reply_id[random.randint(0,len(reply_id)-1)]
        except Exception as e:
            print(f"浏览帖子失败: {e}")
            return None

    @staticmethod
    def getmatch(geturl,cookies):
        headers={
        'Host': 't66y.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'https://t66y.com/index.php',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': Autoreply.UserAgent
        }
        sleep(2)
        try:
            get=requests.get(geturl,headers=headers,cookies=cookies, timeout=10)
            sleep(2)
            get=get.content.decode('utf-8','ignore')
            pat='<b>本頁主題:</b> .*</td>'
            res=re.search(pat,get)
            if res:
                res=res.group(0).replace('<b>本頁主題:</b> ','').replace('</td>','')
                res='Re:'+res
                return res
            return "Re:分享"
        except Exception as e:
            print(f"获取帖子标题失败: {e}")
            return "Re:分享"

    @staticmethod
    def getreply():
        reply=['感谢分享','感谢你的分享','谢谢分享','多谢分享','感谢作者的分享','谢谢坛友分享','内容精彩','的确如此','感谢分享','涨知识了','很有意思']
        reply_m=random.randint(0,len(reply)-1)
        reply_news=reply[reply_m]
        print('本次回复消息是:'+reply_news)
        return  reply_news

    @staticmethod
    def postreply(cookies,res,reply_news,tid):
        headers={
        'Host': 't66y.com',
        'Origin': 'null',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Proxy-Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': Autoreply.UserAgent
        }
        posturl='https://t66y.com/post.php?'
        data={
            'atc_usesign':'1',
            'atc_convert':'1',
            'atc_autourl': '1',
            'atc_title': res ,
            'atc_content': reply_news ,
            'step': '2',
            'action': 'reply',
            'fid': '7',
            'tid': tid ,
            'atc_attachment': 'none',
            'pid':'',
            'article':'',
            'touid':'',
            'verify':'verify'
        }
        try:
            post=requests.post(posturl,data=data,headers=headers,cookies=cookies, timeout=10)
            post = post.content.decode('utf-8','ignore')
            if post.find('發貼完畢點擊')!=-1:
                status='回复成功'
                return status
            if post.find('所屬的用戶組')!=-1:
                status='今日已达上限'
                return status
            return "回复失败"
        except Exception as e:
            print(f"回复帖子失败: {e}")
            return "回复失败"

    @staticmethod
    def getnumber(cookies):
        indexurl='https://t66y.com/index.php'
        headers={
        'Host': 't66y.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'https://t66y.com/index.php',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': Autoreply.UserAgent
        }
        sleep(2)
        try:
            index=requests.get(indexurl,headers=headers,cookies=cookies, timeout=10)
            index = index.content.decode('utf-8','ignore')
            pat='共發表帖子: \d{1,5}'
            num_match = re.search(pat,index)
            if num_match:
                num=num_match.group(0)
                num=num.replace('共發表帖子: ','')
                return num
            return "0"
        except Exception as e:
            print(f"获取发帖数量失败: {e}")
            return "0"
    
    @staticmethod
    def like(id,url,cookies):
        if not id:
            return False
        likeurl='https://t66y.com/api.php'
        headers={
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Host': 't66y.com',
        'Connection': 'keep-alive',
        'Origin': 'https://t66y.com',
        'User-Agent': Autoreply.UserAgent,
        'X-Requested-With': 'XMLhttpRequest',
        }
        data={
            'action': 'clickLike',
            'id': id,
            'page': 'h',
            'json': '1',
            'url': url
        }    
        try:
            like=requests.post(likeurl,headers=headers,data=data,cookies=cookies, timeout=10)
            if like.status_code == 200:
                like_data = json.loads(like.text)
                if 'myMoney' in like_data and int(like_data['myMoney']) > 0:
                    return True
            return False
        except Exception as e:
            print(f"点赞失败: {e}")
            return False

    @staticmethod
    def main(cookieslist,todaylist,ge):
        n=0
        cookies=cookieslist[ge]
        m=Autoreply.getnumber(cookies)
        like_flag = False
        suc=False
        print('第'+str(ge+1)+'个账号开始时发表帖子:'+m)
        
        # 创建今日列表的副本，避免多进程间干扰
        todaylist_copy = todaylist.copy()
        
        while n<10 and suc is False and todaylist_copy:
            try:
                print('第'+str(ge+1)+'个账号当前在回复第'+str(n+1)+'个。')
                geturl,tid=Autoreply.getonelink(todaylist_copy)
                if not geturl or not tid:
                    print('没有可用的帖子链接')
                    break
                    
                reply_news=Autoreply.getreply()
                res=Autoreply.getmatch(geturl,cookies)
                sleeptime=random.randint(1024,2048)
                au=Autoreply.postreply(cookies,res,reply_news,tid)
                if au=='回复成功':
                    print('第'+str(ge+1)+'个账号回复成功')
                    n=n+1
                    print('第'+str(ge+1)+'个账号休眠'+str(sleeptime)+'s...')
                    id = Autoreply.browse(geturl,cookies)
                    if config.get('like',True) and id:
                        temp = Autoreply.like(id,geturl,cookies)
                        if like_flag != True:
                            like_flag = temp
                    sleep(sleeptime)
                    print('第'+str(ge+1)+'个账号休眠完成')
                elif au=='今日已达上限':
                    print('第'+str(ge+1)+'个账号回复失败，今日次数已达10次')
                    suc=True
                else:
                    print('第'+str(ge+1)+'个账号1024限制或者被禁言！！！')
                    print('第'+str(ge+1)+'个账号休眠'+str(sleeptime)+'s...')
                    sleep(sleeptime)
                    print('第'+str(ge+1)+'个账号休眠完成')
            except Exception as e:
                print('第'+str(ge+1)+'个账号回复失败，重试')
                print(f"错误信息: {e}")
                sleep(60)
        n=Autoreply.getnumber(cookies)
        print('第'+str(ge+1)+'个账号开始时发表帖子:'+m)
        print('第'+str(ge+1)+'个账号结束时发表帖子:'+n)
        if config.get('like',True):
            print(f"第{str(ge+1)}个账号点赞状态为{like_flag}")
        print('第'+str(ge+1)+'个账号回复'+str(int(n)-int(m))+'次')

if __name__ == "__main__":
    cookieslist=[]
    todaylist=[]
    
    user = os.environ.get("USER", "")
    password = os.environ.get("PASSWORD", "")
    secret = os.environ.get("SECRET", "")

    if not user or not password or not secret:
        print('环境变量未设置完整，请检查USER、PASSWORD和SECRET')
        sys.exit(1)

    userlist=user.split()
    passwordlist=password.split()
    secretlist=secret.split()

    if len(userlist)!=len(passwordlist) or len(passwordlist)!=len(secretlist):
        print('参数个数不匹配，请检查环境变量设置是否正确')
        sys.exit(1)
    else:
        print('检测到',len(userlist),'个账号')

    count=0
    while count<len(userlist):
        success=None
        auto=Autoreply(userlist[count],passwordlist[count],secretlist[count])
        while success is None:
            userCookieFile = f"./{userlist[count]}"
            if os.path.isfile(userCookieFile):
                try:
                    with open(userCookieFile, 'rb') as f:   
                        auto.updateCookies(pickle.load(f))
                        print(f"账号{count+1} cookie文件已加载...跳过密码登录")
                    if auto.verifyLoginSuc() == True:
                        success = True
                        break
                except Exception as e:
                    print(f"加载cookie失败: {e}")
                    
            au=auto.login1()
            if au=='登录尝试次数过多,需输入验证码':
                print('登录尝试次数过多,需输入验证码')
                if auto.getverwebp():
                    if config.get('Input_self',False):
                        vercode = input('请手动输入验证码:')
                    else:
                        vercode = GetVerificationCode.apitruecaptcha()
                    print('输入的验证码为:'+vercode)
                    while auto.inputvercode(vercode)=='验证码不正确，请重新输入':
                        print('验证码不正确，请重新输入')
                        if not auto.getverwebp():
                            print("获取验证码失败")
                            break
                        if config.get('Input_self',False):
                            vercode=input('请手动输入验证码:')
                        else:
                            vercode = GetVerificationCode.apitruecaptcha()
                        print('输入的验证码为:'+vercode)
                if auto.login1()=='賬號已開啟兩步驗證':
                    if auto.login2()=='已經順利登錄':
                        print('登录成功')
                        success = True
            elif au=='賬號已開啟兩步驗證':
                if auto.login2()=='已經順利登錄':
                    print('登录成功')
                    success = True
            else:
                print("登录失败，重试中...")
                sleep(10)
                
        cookies=auto.getcookies()
        cookieslist.append(cookies)
        count+=1
        
    print('cookies获取完成')
    
    # 使用最后一个登录的实例获取今日列表
    todaylist=auto.gettodaylist()
    if not todaylist:
        print("获取今日列表失败，程序退出")
        sys.exit(1)
        
    print(f"获取到{len(todaylist)}个帖子")
    
    # 使用进程池处理多个账号
    p=Pool(min(len(userlist), 4))  # 限制最大进程数为4
    results = []
    for i in range(len(userlist)):
        res=p.apply_async(Autoreply.main,args=(cookieslist,todaylist,i))
        results.append(res)
        print('第',str(i+1),'个进程启动...')
    p.close()
    p.join()
    
    # 获取所有进程的结果
    for res in results:
        try:
            res.get()
        except Exception as e:
            print(f"进程执行出错: {e}")
            
    print('完成')