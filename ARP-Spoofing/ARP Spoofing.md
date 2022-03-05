# ARP Spoofing

## 实验目的

1. 增强对ARP协议工作方式的理解
2. 掌握ARP欺骗的原理

## 实验环境

两个基于VMware的Ubuntu18.04虚拟机；

嗅探工具Ettercap

## 实验内容

使用Ettercap + driftnet软件建立中间人攻击并监听图片。

## 实验原理

ARP欺骗（ARP spoofing），又称ARP毒化（ARP poisoning），是针对以太网地址解析协议（ARP）的一种攻击技术，通过欺骗局域网内访问者PC的网关MAC地址，使访问者PC错以为攻击者更改后的MAC地址是网关的MAC，导致网络不通。此种攻击可让攻击者获取局域网上的数据包甚至可篡改数据包，且可让网络上特定计算机或所有计算机无法正常连线。ARP欺骗的运作原理是由攻击者发送假的ARP数据包到网上，尤其是送到网关上。其目的是要让送至特定的IP地址的流量被错误送到攻击者所取代的地方。因此攻击者可将这些流量另行转送到真正的网关（被动式数据包嗅探，passive sniffing）或是篡改后再转送（中间人攻击，man-in-the-middle attack）。

## 实验过程

ARP欺骗需要两台在同一网段的虚拟机，因此首先确认一下能否ping通。我的两台虚拟机IP地址分别是192.168.1.105和192.168.1.106。用105主机ping通106主机的截图如下：

![image-20220304225350712](https://gitee.com/bright_xu/blog-image/raw/master/img/image-20220304225350712.png)

输入 sudo ettercap –G 打开软件，选择sniff标签下的unified sniffing。选择host 下的scan for hosts 扫描主机，完成后选择hosts list打开。然后点击网关，选择add target1 ,再点击受害者的主机，选择add target2，截图如下：

![image-20220304225358992](https://gitee.com/bright_xu/blog-image/raw/master/img/image-20220304225358992.png)

 在受害者主机上查看ARP缓存表，可以看到接口的地址是攻击者主机说明攻击成功，我的攻击者主机即为192.168.1.105，如下图：

![image-20220304225414451](https://gitee.com/bright_xu/blog-image/raw/master/img/image-20220304225414451.png)

在攻击者主机上打开wireshark进行抓包，可以看到许多ARP协议包：

![image-20220304225421943](https://gitee.com/bright_xu/blog-image/raw/master/img/image-20220304225421943.png)

打开下载的driftnet工具，我主机的网卡名是ens33,因此输入：sudo driftnet -i ens33。如下图：

![image-20220304225436480](https://gitee.com/bright_xu/blog-image/raw/master/img/image-20220304225436480.png)

然后在受害者主机上随便打开一个未加密的http网页，这里我以西安交通大学教务处的网站dean.xjtu.edu.cn为例，然后观察driftnet的嗅探情况，可以发现driftnet已经有嗅探到了图片，说明中间人攻击生效。

![image-20220304225447317](https://gitee.com/bright_xu/blog-image/raw/master/img/image-20220304225447317.png)

## 防御办法

（1）MAC地址绑定。由于ARP欺骗攻击是通过虚构IP地址和MAC地址欺骗目标主机, 从而更改ARP缓存中的路由表进行攻击的, 因此, 只要将局域网中每一台计算机的IP地址与MAC地址绑定, 就能有效地防御ARP欺骗攻击。

（2）设置静态的ARP缓存。使用静态ARP缓存来绑定关系, 如果需要更新ARP缓存表, 使用手工进行更新, 以保障黑客无法进行ARP欺骗攻击。在计算机上使用arp -s命令添加静态ARP缓存记录。若攻击者向主机发送ARP应答报文，目标机接收报文后并不会刷新ARP缓存表。

（3）使用ARP服务器。在ARP服务器中保存局域网服务器中各主机的IP地址和MAC地址的映射信息，同时禁用各主机的ARP应答，保留服务器对ARP请求的应答。它的致命缺点就是一定要保证ARP服务器的安全，不然ARP服务器一旦被攻陷，后果不堪设想。

（4）采用ARP防火墙。现在很多杀毒软件制造商都设计出了个人ARP防火墙模块，该模块也是通过绑定主机和网关等其他方式，来避免遭受攻击者所冒充的家网关攻击。在一定程度上可以防御ARP欺骗攻击。

（5）划分虚拟局域网VLAN和端口绑定。在使用三层交换机的网络中，可以通过划分VLAN的方法减小ARP攻击的影响范围。VLAN可以不考虑网络的实际地理位置，用户可以根据不同客户端的功能、应用等将其从逻辑上划分在一个相对独立的组中，每个客户端的主机都连接在支持VLAN的交换机端口上，同一个VLAN内的主机形成一个广播域，不同VLAN之间的广播报文能够得到有效的隔离。由于ARP攻击不能跨网段完成。因此，这种方法能够有效地将ARP攻击限制在一定范围内。但其缺点是增加了网络管理的复杂度, 而且无法适应网络的动态变化。

