# DNS cache poisoning

## 实验目的

1. 了解 hosts 文件和 DNS 系统的关系。

2. 使用 DNS 攻击工具进行 DNS 投毒，观察攻击情况，了解 DNS 攻击原理。

## 实验环境

Server：ubuntu虚拟机，安装DNS服务器bind9

Attacker：ubuntu虚拟机，与server处于同一网段（局域网）

## 实验原理

目前DNS采用UDP协议传输查询和应答数据包，采用简单信任机制，对首先收到的DNS应答数据包仅进行原查询包发送IP地址、端口和ID的确认，而不会对数据包的合法性做任何分析，若匹配，则接受其为正确应答数据包，继续DNS解析过程，并且丢弃后续到达的所有应答数据包。这就使得攻击者可以仿冒权威DNS服务器向缓存DNS服务器发送伪造应答包，力争抢先完成应答以污染DNS缓存。若攻击者发送的伪造应答包在权威名字服务器发送的正确应答包之前到达缓存DNS服务器，并与原查询包IP地址、端口、ID相匹配，就能够成功污染DNS缓存。

DNS缓存投毒是指一些刻意制造（投毒）或无意中制造（污染）出来的DNS数据包，让DNS缓存服务器缓存了错误的域名解析记录。

  DNS缓存投毒工作方式是：由于通常的DNS查询没有任何认证机制，而且DNS查询通常基于的UDP是无连接不可靠的协议，因此DNS的查询非常容易被篡改，通过对UDP端口上的DNS查询进行监听，一经发现与关键词相匹配的请求则立即伪装成目标域名的解析服务器（NS，Name Server）给查询者返回错误结果。为了减少网络上的流量，一般的DNS缓存服务器都会把域名数据缓存起来，待下次有其他DNS客户端要求解析同样的域名时，可以立即提供服务。当缓存服务器缓存了错误的域名数据时，DNS客户端在请求这些域名时就会得到错误的结果。

## 实验步骤

### 配置DNS服务端

首先使用命令安装bind9： `apt-get install bind9`

安装bind9后, `/etc/bind/`文件夹中会生成很多基础的配置文件，可以用

`ls /etc/bind/ -l`进行查看，如下图所示：

![image-20220304224041018](https://gitee.com/bright_xu/blog-image/raw/master/img/image-20220304224041018.png)

使用命令编辑该文件：`sudo gedit named.conf.options`

在文件中修改DNS查询端口，关闭dnssec-validation服务，这是设置用来防止DNS缓存投毒攻击的。注释掉named.conf.options文件中的对应条目，并且加入关闭dnssec服务的语句：

![image-20220304224106820](https://gitee.com/bright_xu/blog-image/raw/master/img/image-20220304224106820.png)

刷新DNS缓存，然后重启DNS服务器，将DNS数据导出并查看初始状态：

![image-20220304224122972](https://gitee.com/bright_xu/blog-image/raw/master/img/image-20220304224122972.png)

dump.db文件初始状态如下：

![image-20220304224148377](https://gitee.com/bright_xu/blog-image/raw/master/img/image-20220304224148377.png)                           

### 配置客户端

使用命令`sudo gedit /etc/resolv.conf `，将nameserver修改为server的ip地址192.168.43.126。

![image-20220304224215551](https://gitee.com/bright_xu/blog-image/raw/master/img/image-20220304224215551.png)

在客户端访问www.baidu.com之后，我们可以看到server的解析记录

![image-20220304224232399](https://gitee.com/bright_xu/blog-image/raw/master/img/image-20220304224232399.png)

### 进行DNS投毒

接下来，我们进行DNS投毒攻击。在进行DNS缓存投毒时，使用server运行wireshark，可以看到抓取了大量的DNS数据包，发现每个查询请求报文后跟着大量应答。

![image-20220304224247048](https://gitee.com/bright_xu/blog-image/raw/master/img/image-20220304224247048.png)

由于DNS污染概率较小，清理缓存比较麻烦，所以这次实验的目标是污染不存在的域名，即随机的一个域名。攻击成功之后，程序结束，截图如下：

![image-20220304224301359](https://gitee.com/bright_xu/blog-image/raw/master/img/image-20220304224301359.png)

### 结果分析

投毒成功后我们打开wireshark查看，发现DNS server成功返回了域名4519890.example.com的IP地址为1.1.1.1，表明攻击成功。

![image-20220304224407815](https://gitee.com/bright_xu/blog-image/raw/master/img/image-20220304224407815.png)

投毒成功后，输入rndc dumpdb –cache，然后查看server端的cache，发现已经被污染。攻击成功，缓存信息中4519890.example.com对应的A记录被设置成1.1.1.1。

![image-20220304224418329](https://gitee.com/bright_xu/blog-image/raw/master/img/image-20220304224418329.png)

再在客户端进行dig，确实域名解析到了1.1.1.1。

![image-20220304224429589](https://gitee.com/bright_xu/blog-image/raw/master/img/image-20220304224429589.png)