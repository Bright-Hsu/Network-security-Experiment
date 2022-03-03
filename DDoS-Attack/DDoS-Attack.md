# DDos-Attack

## 实验目的

1. 熟悉 Linux 系统,Wireshark 软件基本操作。

2. SYN 洪泛攻击的实现与观察。

## 实验平台

Server：ubuntu虚拟机，安装Apache24

Attacker：ubuntu虚拟机，与server处于同一网段（局域网）

## 实验原理

分布式拒绝服务攻击原理分布式拒绝服务攻击DDoS是一种基于DoS的特殊形式的拒绝服务攻击，是一种分布的、协同的大规模攻击方式。单一的DoS攻击一般是采用一对一方式的，它利用网络协议和操作系统的一些缺陷，采用欺骗和伪装的策略来进行网络攻击，使网站服务器充斥大量要求回复的信息，消耗网络带宽或系统资源，导致网络或系统不胜负荷以至于瘫痪而停止提供正常的网络服务。与DoS攻击由单台主机发起攻击相比较，分布式拒绝服务攻击DDoS是借助数百、甚至数千台被入侵后安装了攻击进程的主机同时发起的集团行为。

SYN泛洪攻击是一种比较常用的 Dos 方式之一。通过发送大量伪造的 TCP 连接请求，使被攻击主机资源耗尽（通常是 CPU 满负荷或内存不足）的攻击方式。

我们都知道建立 TCP 连接需要三次握手。正常情况下客户端首先向服务器端发送 SYN报文，随后服务端返回以 SYN+ACK 报文，最后客户端向服务端发送 ACK 报文完成三次握手。而 SYN泛洪攻击则是客户端向服务器发送 SYN报文之后就不再响应服务器回应的报文。由于服务器在处理 TCP 请求时，会在协议栈留一块缓冲区来存储握手的过程，当然如果超过一定时间内没有接收到客户端的报文，本次连接在协议栈中存储的数据将会被丢弃。攻击者如果利用这段时间发送大量的连接请求，全部挂起在半连接状态。这样将不断消耗服务器资源，直到拒绝服务。

## 实验步骤

### 1. 配置环境

首先安装两个ubuntu虚拟机，一个作为被攻击者，另一个作为攻击者，它们需要处于同一局域网。因此将两个虚拟机都调整为桥接模式。

### 2. 在server上安装Apache服务器

在浏览器中输入127.0.0.1访问，出现以下界面，因此说明Apache安装成功：

![image-20220303215548163](https://gitee.com/bright_xu/blog-image/raw/master/img/image-20220303215548163.png)

### 3. 检查连台虚拟机是否在同一局域网

通过ifconfig命令，我们获取apache2服务器的ip地址，可知server的IP是192.168.1.103。

![image-20220303215647988](https://gitee.com/bright_xu/blog-image/raw/master/img/image-20220303215647988.png)

在Attacker的浏览器上，输入192.168.1.103，也能访问，说明配置成功。

![image-20220303215726568](https://gitee.com/bright_xu/blog-image/raw/master/img/image-20220303215726568.png)

### 4. 进行SYN-FLOOD攻击

在攻击机上下载函数库，然后编写代码进行攻击，SYN_flood.py文件内容及注释如下。

![image-20220303215802455](https://gitee.com/bright_xu/blog-image/raw/master/img/image-20220303215802455.png)

运行py脚本，开始攻击：

![image-20220303215829654](https://gitee.com/bright_xu/blog-image/raw/master/img/image-20220303215829654.png)

在server上用wireshark进行观察，可以看到，客户端和服务器端 TCP 连接只握手了两次，都处于半开连接状态：

![image-20220303215840118](https://gitee.com/bright_xu/blog-image/raw/master/img/image-20220303215840118.png)

Server运行netstat –atn可以看到，出现了很多的SYN请求。

![image-20220303215859106](https://gitee.com/bright_xu/blog-image/raw/master/img/image-20220303215859106.png)

## 遇到的问题及其解决

在两个虚拟机都使用NAT模式时，SYN攻击失败，客户端会在两次握手后，发送 TCP RST 断开 TCP 连接。在查阅资料后，发现改为桥接模式之后，问题便解决了，SYN攻击成功，但是其中原理还是尚未清楚。

