# SSL/TLS

## **抓包观察ssl协议通信握手过程**

下面我使用wireshark抓包以具体实例来分析ssl握手的具体过程。使用wireshark过滤ssl流量，可以看到有几个明显的ssl会话建立包，例如client hello，server hello等，如下图：

![image-20220330225232681](https://gitee.com/bright_xu/blog-image/raw/master/202203302252821.png)

接下来详细分析每个包的含义：

### 1. Client发送Client Hello

client发起请求，以明文传输请求信息Client Hello，包中包含的信息有Version（版本信息）、random（随机数）、session ID Length（是否有保存会话）、Cipher Suites（加密套件）、compression methods（压缩算法候选列表）、Extension（扩展字段）等信息。相关信息如下：

（1）支持的最高TSL协议版本version，从低到高依次 SSLv2、SSLv3、 TLSv1、TLSv1.1、TLSv1.2。

（2）客户端支持的加密套件 cipher suites 列表， 每个加密套件对应前面 TLS 原理中的四个功能的组合：认证算法 Au (身份验证)、密钥交换算法 Key Exchange(密钥协商)、对称加密算法 Enc (信息加密)和信息摘要 Mac(完整性校验);

（3）支持的压缩算法 compression methods 列表，用于后续的信息压缩传输;

（4）随机数 random，用于后续的密钥的生成;

（5）扩展字段 extensions，支持协议与算法的相关参数以及其它辅助信息等，常见的 SNI 就属于扩展字段。

![image-20220330225320142](https://gitee.com/bright_xu/blog-image/raw/master/202203302253194.png)

### 2. Server发送Server Hello

Server hello是服务端server返回协商的信息结果，包中的信息包括选择使用的协议版本 version，选择的加密套件 cipher suite，选择的压缩算法 compression method、随机数 random 等，其中随机数用于后续的密钥协商。

可以看到这里选用的加密套件是ESA+AES128+SHA256，没有使用压缩算法，因此compression method是null。

![image-20220330225528366](https://gitee.com/bright_xu/blog-image/raw/master/202203302255423.png)

### 3. Server发送Certificate

Certificate是服务器端配置对应的证书链，用于身份验证与密钥交换。server的证书信息，只包含public key，server将该public key对应的private key保存好，用于证明server是该证书的实际拥有者。

![image-20220330230342411](https://gitee.com/bright_xu/blog-image/raw/master/202203302303453.png)

### 4. Server发送Server Key Exchange

表明这里用的是DH协议来交换对称加密的密钥。

![image-20220330230411366](https://gitee.com/bright_xu/blog-image/raw/master/202203302304404.png)

### 5. Server发送Server Hello Done

通知客户端 server hello 信息发送结束。

![image-20220330230555129](https://gitee.com/bright_xu/blog-image/raw/master/202203302305185.png)

### 6. Client发送Client Key Exchange

这里也是表明用DH协议来交换对称加密的密钥。

![image-20220402224724711](https://gitee.com/bright_xu/blog-image/raw/master/202204022247853.png)

### 7. Client发送Change Cipher Spec









## 概述

SSL：（Secure Socket Layer，安全套接字层），位于可靠的面向连接的网络层协议和应用层协议之间的一种协议层。SSL通过互相认证、使用数字签名确保完整性、使用加密确保私密性，以实现客户端和服务器之间的安全通讯。该协议由两层组成：SSL记录协议和SSL握手协议。其中SSL握手协议层又分为SSL握手协议、SSL密钥更改协议和SSL警告协议。

握手协议是客户机和服务器用SSL连接通信时使用的第一个子协议，握手协议包括客户机与服务器之间的一系列消息。该协议允许服务器和客户机相互验证，协商加密和MAC算法以及保密密钥，用来保护在SSL记录中发送的数据。握手协议是在应用程序的数据传输之前使用的。SSL协议通信握手过程主要可以分为以下四个阶段：

（1）初始化阶段。客户端创建随机数，发送Client Hello 将随机数连同自己支持的协议版本、加密算法和压缩算法发送给服务器。服务器回复Server Hello将自己生成的随机数连同选择的协议版本、加密算法和压缩算法给客户端。

（2）认证阶段。服务器发送Server Hello的同时可能将包含自己公钥的证书发送给客户端（Certificate），并请求客户端的证书（Certificate Request）。

（3）密钥协商阶段。客户端验证证书，如果收到Certificate Request则发送包含自己公钥的证书，同时对此前所有握手消息进行散列运算，并使用加密算法进行加密发送给服务器。同时，创建随机数pre-master-secret并使用服务器公钥进行加密发送。服务器收到这个Client Key Exchange之后解密得到pre-master-secret。服务器和客户端利用1阶段的随机数，能够计算得出master-secret。

（4）握手终止。服务器和客户端分别通过Change Cipher Spec消息告知伺候使用master-secret对连接进行加密和解密，并向对方发送终止消息（Finished）。

 

  在前面实验步骤中，抓包观察ssl协议通信握手过程的分析已经讲过了，因此这里不再赘述，下面我再对握手过程进行简单的总结：

（1）client发送Client Hello，包含Version（版本信息），session ID Length（是否有保存会话），随机数(Random)，所有支持的密码套件(Cipher Suites)等信息；

（2）server回应Server Hello，指定版本，随机数（Random），选择Cipher Suites，会话ID(Session ID)；

（3）server发送Certificate，发送包含公钥的证书；

（4）server发送Server Key Exchange，用于与client交换session key；

（5）Server发送Server Hello Done；

（6）Client发送Client Key Exchange，用于与server交换session key；

（7）Client发送Change Cipher Spec，指示Server从现在开始发送的消息都是加密过的；

（8）Client发送Finished，包含了前面所有握手消息的hash，可以让server验证握手过程是否被第三方篡改；

（9）Server发送Change Cipher Spec，指示Client从现在开始发送的消息都是加密过的；

（10）Server发送Finished，包含了前面所有握手消息的hash，可以让client验证握手过程是否被第三方篡改，并且证明自己是Certificate密钥的拥有者，即证明自己的身份；

（11） 双方互相发送Application Data。
