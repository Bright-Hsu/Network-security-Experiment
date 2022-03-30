# SSL/TLS

## **抓包观察ssl协议通信握手过程**

下面我使用wireshark抓包以具体实例来分析ssl握手的具体过程。使用wireshark过滤ssl流量，可以看到有几个明显的ssl会话建立包，例如client hello，server hello等，如下图：