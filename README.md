# 1024-reply

config 配置:

```
config={
    'Forbid':  True,              #True为屏蔽版主发帖,无参数或者False为不屏蔽
    'Input_self':  False,         #设置为True为手动输入验证码,无参数或者False为自动输入
    'like': True,                 #True为每日自动点赞一次，无参数默认为True
}
```

<h4>Secrets 添加下列值</h4>

(必需)

```
USER             用户名

PASSWORD         密码

SECRET           谷歌身份验证器密钥
```

(可选1)([申请地址](https://apitruecaptcha.org/))

```
USERID            api页面中的userid字段
APIKEY            api页面中的apikey字段
```

(可选2)([注册地址](http://ttshitu.com/register.html?inviter=3d92d1b2371f487d9072430a93bb043c) )

```
CODEUSER         注册用户名

CODEPASS         注册密码
```

ps:可选两个是识别验证码用的，任选其一即可，也可以都不选。如果不选碰见需要验证码的则会运行失败。

```
第一个是免费的api接口，每天100次免费的

第二个是自己找的一个平台，1元可以识别500次
```

想要更换验证方式的，修改1024.py 316行，324行为 `GetVerificationCode.`+getver中的函数名

<h4>
2.

(1)先点击Actions,同意使用协议。

(2)点击左侧树形图中的 `1024-AutoReply`,然后点击右边的 `Run workdlow` 即可手动触发执行一次。（后续除非是调试，否则等待自动执行就可以了）

(可选)3.可以通过 `getreply()中的reply`设置回复内容，`sleeptime设置为(1024,2048)之间`，可以根据需要修改。因为Actions一个项目限制6个小时，所以最大值不要超过2048。如果Actions显示运行超过六小时，先自行检查之前是否回复成功，若是，则把2048调整小一点。若不是，请提issues

(可选)4.下面是自己下载py文件运行时的问题

修改以下参数，记得用''括起来

```
user=''                 用户名

password=''             密码

secret=''               谷歌身份验证器密钥
```

验证码部分根据自己选择修改参数类似上面

有能力可以自己登陆修改为使用cookies登录，就不需要验证码部分了
