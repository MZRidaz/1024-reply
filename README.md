# 1024-reply

config 配置:

```
config={
    'Forbid':  True,              #True为屏蔽版主发帖,无参数或者False为不屏蔽
    'Input_self':  False,         #设置为True为手动输入验证码,无参数或者False为自动输入
    'like': True,                 #True为每日自动点赞一次，无参数默认为True
}
```

Secrets 添加下列值

```
USER             用户名

PASSWORD         密码

SECRET           谷歌身份验证器密钥
```

`Run workdlow` 即可手动触发执行一次，后续除非是调试，都可以自动执行。

 `getreply()中的reply`设置回复内容,`sleeptime` 设置为(1024,2048)之间，Actions一个项目限制6个小时，所以最大值不要超过2048。
