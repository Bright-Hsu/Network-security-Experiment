# SSL/TLS

## **抓包观察ssl协议通信握手过程**

下面我使用wireshark抓包以具体实例来分析ssl握手的具体过程。使用wireshark过滤ssl流量，可以看到有几个明显的ssl会话建立包，例如client hello，server hello等，如下图：

![image-20220330225232681](https://gitee.com/bright_xu/blog-image/raw/master/202203302252821.png)

接下来详细分析每个包的含义：

1. ## Client发送Client Hello

client发起请求，以明文传输请求信息Client Hello，包中包含的信息有Version（版本信息）、random（随机数）、session ID Length（是否有保存会话）、Cipher Suites（加密套件）、compression methods（压缩算法候选列表）、Extension（扩展字段）等信息。相关信息如下：

（1）支持的最高TSL协议版本version，从低到高依次 SSLv2、SSLv3、 TLSv1、TLSv1.1、TLSv1.2。

（2）客户端支持的加密套件 cipher suites 列表， 每个加密套件对应前面 TLS 原理中的四个功能的组合：认证算法 Au (身份验证)、密钥交换算法 Key Exchange(密钥协商)、对称加密算法 Enc (信息加密)和信息摘要 Mac(完整性校验);

（3）支持的压缩算法 compression methods 列表，用于后续的信息压缩传输;

（4）随机数 random，用于后续的密钥的生成;

（5）扩展字段 extensions，支持协议与算法的相关参数以及其它辅助信息等，常见的 SNI 就属于扩展字段。

![image-20220330225320142](https://gitee.com/bright_xu/blog-image/raw/master/202203302253194.png)

2. ## Server发送Server Hello

Server hello是服务端server返回协商的信息结果，包中的信息包括选择使用的协议版本 version，选择的加密套件 cipher suite，选择的压缩算法 compression method、随机数 random 等，其中随机数用于后续的密钥协商。

可以看到这里选用的加密套件是ESA+AES128+SHA256，没有使用压缩算法，因此compression method是null。

![image-20220330225528366](https://gitee.com/bright_xu/blog-image/raw/master/202203302255423.png)