# DVWA靶场实验

## 实验目的

1. 搭建安全靶场，熟悉常见的WEB安全漏洞；

2. 了解并掌握相关工具寻找漏洞及注入点；

3. 掌握漏洞的保护方式。

## 实验环境

1. 两个基于VMware的Ubuntu18.04虚拟机；

2. DVWA（Damn Vulnerable Web App）靶场；

## 实验内容

1. DVWA靶场搭建

安装xampp和DVWA文件，并进行环境配置。

2. 爆破登陆

使用burp suite工具拦截包并使用字典暴力破解密码登陆。

3. SQL注入

了解SQL注入原理并利用漏洞进行登录。

## 实验原理

DVWA (Dam Vulnerable Web Application)是用PHP + MySQL编写的一套用于常规WEB漏洞教学和检测的WEB脆弱性测试程序，包含了SQL注入、XSS、盲注等常见的一些安全漏洞。其主要目标是帮助安全专业人员在法律环境中测试他们的技能和工具，帮助Web开发人员更好地了解保护Web应用程序的过程，并帮助学生和教师了解受控类中的Web应用程序安全性房间测试环境。

本次实验我们要实现的是Brute Force（暴力破解）、SQL Injection（SQL注入），还有ARP欺骗。

Brute Force（暴力破解）是指黑客利用密码字典，使用穷举法猜解出用户口令，是现在最为广泛使用的攻击手法之一。一般指穷举法，穷举法的基本思想是根据题目的部分条件确定答案的大致范围，并在此范围内对所有可能的情况逐一验证，直到全部情况验证完毕。若某个情况验证符合题目的全部条件，则为本问题的一个解；若全部情况验证后都不符合题目的全部条件，则本题无解。

SQL Injection（SQL注入）是发生在 Web 程序中数据库层的安全漏洞，是网站存在最多也是最简单的漏洞。主要原因是程序对用户输入数据的合法性没有判断和处理，导致攻击者可以在 Web 应用程序中事先定义好的 SQL 语句中添加额外的 SQL 语句，在管理员不知情的情况下实现非法操作，以此来实现欺骗数据库服务器执行非授权的任意查询，从而进一步获取到数据信息。

## 实验步骤

### 1. Brute Force（暴力破解）

首先，我们修改了浏览器的代理ip，ip为127.0.0.1，端口为8080。同时将No proxy for 中的内容删去。

然后访问127.0.0.1/DVWA/vulnerabilities/brute/index.php,可以看到xampp拦截到了下列包。

![图形用户界面, 文本, 应用程序, 电子邮件  描述已自动生成](C:/Users/DELL/AppData/Local/Temp/msohtmlclip1/01/clip_image002.png)

接下来随便填写一个账号密码，这里输入账号abcd，密码12345，然后提交登录，软件拦截到了包，并且发现账号和密码是明文传输的，可以直接抓取到：

![图形用户界面, 文本, 应用程序, 电子邮件  描述已自动生成](C:/Users/DELL/AppData/Local/Temp/msohtmlclip1/01/clip_image004.png)

  参数列表如下，此时是安全等级是low：

![图形用户界面, 文本, 应用程序, 电子邮件  描述已自动生成](C:/Users/DELL/AppData/Local/Temp/msohtmlclip1/01/clip_image006.png)

然后点击action 选择 send to Intruder ,将包发送到Intruder模块，准备构造爆破包。该模块默认会将所有参数自动标记，我们在low模式下只需要爆破密码。首先看到自动标记的参数如下：

![图形用户界面, 文本, 应用程序, 电子邮件  描述已自动生成](https://gitee.com/bright_xu/blog-image/raw/master/img/clip_image008.png)

点击clear先清除自动标记的参数，然后手动选中密码，按add标记参数，如下图所示。

![图形用户界面, 文本, 应用程序, 电子邮件  描述已自动生成](C:/Users/DELL/AppData/Local/Temp/msohtmlclip1/01/clip_image010.png)

然后点击payload标签，在simple list中添加字典，随便填加几个，添加完成后点击start attack。然后查看结果，发现有一个包返回的长度跟别的都不一样，就是爆破正确的密码。从下图可以看出，密码就是password。

![图形用户界面, 文本, 应用程序  描述已自动生成](C:/Users/DELL/AppData/Local/Temp/msohtmlclip1/01/clip_image012.jpg)

然后将得到的密码输入网页中，可以看到登录成功：

![img](https://gitee.com/bright_xu/blog-image/raw/master/img/clip_image014.png)