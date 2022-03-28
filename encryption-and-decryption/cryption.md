# Encryption and Decryption

## 实验目的

1. 加深对非对称，对称加解密算法、散列函数的理解。

2. 了解常用加密工具包以及相关库函数的使用。

3. 了解ssl协议

## 实验环境

ubuntu虚拟机，python3

## 实验原理

1. 对称加密 采用单钥密码系统的加密方法，同一个密钥可以同时用作信息的加密和解密，这种 加密方法称为对称加密，也称为单密钥加密。在对称加密算法中常用的算法有：DES、 3DES、TDEA、Blowfish、RC2、RC4、RC5、IDEA、SKIPJACK 等。 对称加密算法的缺点是在数据传送前，发送方和接收方必须商定好秘钥，然后使双 方都能保存好秘钥。其次如果一方的秘钥被泄露，那么加密信息也就不安全了。另外， 每对用户每次使用对称加密算法时，都需要使用其他人不知道的唯一秘钥，这会使得收、 发双方所拥有的钥匙数量巨大，密钥管理成为双方的负担。 

2. 非对称加密 非对称加密算法需要两个密钥：公开密钥（publickey）和私有密钥（privatekey）。公 开密钥与私有密钥是一对，如果用公开密钥对数据进行加密，只有用对应的私有密钥才 能解密；如果用私有密钥对数据进行加密，那么只有用对应的公开密钥才能解密。因为 加密和解密使用的是两个不同的密钥，所以这种算法叫作非对称加密算法。 非对称加 密算法实现机密信息交换的基本过程是：甲方生成一对密钥并将其中的一把作为公用密 钥向其它方公开；得到该公用密钥的乙方使用该密钥对机密信息进行加密后再发送给甲 方；甲方再用自己保存的另一把专用密钥对加密后的信息进行解密。

3. 散列函数 Hash，一般翻译做"散列"，也有直接音译为"哈希"的，就是把任意长度的输入（又 叫做预映射， pre-image），通过散列算法，变换成固定长度的输出，该输出就是散列值。 这种转换是一种压缩映射，也就是，散列值的空间通常远小于输入的空间，不同的输入 可能会散列成相同的输出，而不可能从散列值来唯一的确定输入值。简单的说就是一种 将任意长度的消息压缩到某一固定长度的消息摘要的函数。

## 实验步骤

### **1.** **使用AES对称加密算法加解密**

对称加密算法采用单钥密码系统的加密方法，同一个密钥可以同时用作信息的加密和解密。本次实验我们采用AES算法对字符串进行加密。

首先在Python中安装加解密相关的库是Crypto，此前已经安装过pip，因此只需输入命令：`pip3 install pycrypto`

AES 加密算法就是众多对称加密算法中的一种，它的英文全称是 Advanced Encryption Standard，翻译过来是高级加密标准，它是用来替代之前的 DES 加密算法的。AES 加密算法采用分组密码体制，每个分组数据的长度为128位16个字节，密钥长度可以是128位16个字节、192位或256位，一共有四种加密模式，我们通常采用需要初始向量 IV 的 CBC 模式，初始向量的长度也是128位16个字节。

下面运行aes.py文件，可以看到加密过程如下：

![image-20220327231532567](https://gitee.com/bright_xu/blog-image/raw/master/202203272315628.png)

### 2.**使用RSA算法进行加解密**

RSA公开密钥密码体制的原理是：根据数论，寻求两个大素数比较简单，而将它们的乘积进行因式分解却极其困难，因此可以将乘积公开作为加密密钥。

RSA公开密钥密码体制是一种使用不同的加密密钥与解密密钥，“由已知加密密钥推导出解密密钥在计算上是不可行的”密码体制。在公开密钥密码体制中，加密密钥（即公开密钥）PK是公开信息，而解密密钥（即秘密密钥）SK是需要保密的。加密算法E和解密算法D也都是公开的。虽然解密密钥SK是由公开密钥PK决定的，但却不能根据PK计算出SK。

下面运行rsa.py文件，可以看到加密解密的过程。另外，在运行前目录中还没有公钥和私钥文件，但在运行之后目录中生成了两个秘钥文件，分别是公钥和私钥。

![image-20220327231638201](https://gitee.com/bright_xu/blog-image/raw/master/202203272316260.png)

### 3. 数字签名

RSA数字签名算法，包括签名算法和验证签名算法。首先用MD5算法对信息作散列计算。签名的过程需用户的私钥，验证过程需用户的公钥。A用签名算法将字符串形式的消息处理成签名；B用验证签名算法验证签名是否是A对消息的签名，确认是A发送的消息；消息没有被攥改过；A一定发送过消息。

运行程序，发现生成了sign.txt文件，且输出正确的数字签名。

![image-20220327231735359](https://gitee.com/bright_xu/blog-image/raw/master/202203272317406.png)

## 思考题

### **1. AES加密中iv变量的作用？**

答：iv变量其实是AES-CBC模式加密时的一个初始化向量(Initialization Vector, IV)，长度是16个字节，在每次加密之前或者解密之后，使用初始化向量与明文或密文进行异或操作。

本实验中的AES加密是CBC模式，即加密块链模式(Cipher Block Chaining) 。CBC 模式的加密首先将明文分成固定长度的块，然后将前面一个加密块输出的密文与下一个要加密的明文块进行异或操作，将计算结果再用密钥进行加密得到密文。第一明文块加密的时候，因为前面没有加密的密文，所以需要一个初始化向量。跟 ECB 方式不一样，通过连接关系，使得密文跟明文不再是一一对应的关系，破解起来更困难，而且克服了只要简单调换密文块可能达到目的的攻击。

encrypt函数在加密的过程中会修改iv的内容，因此iv参数不能是一个常量，而且不能在传递给加密函数后再立马传递给解密函数，必须重新赋值之后再传递给解密函数。

加密时，明文首先与iv异或，然后将结果进行块加密，得到的输出就是密文，同时本次的输出密文作为下一个块加密的iv，如下图：

![image-20220328211555464](https://gitee.com/bright_xu/blog-image/raw/master/202203282116562.png)

解密时，先将密文的第一个块进行块解密，然后将结果与iv异或，就能得到明文，同时，本次解密的输入密文作为下一个块解密的iv，如下图：

![image-20220328211633292](https://gitee.com/bright_xu/blog-image/raw/master/202203282116356.png)

### **2.** **RSA【公钥加密，私钥解密】和【私钥加密，公钥解密】算法一样吗？为什么？**

答：不一样。【公钥加密，私钥解密】被用于RSA加密算法，公钥用于对数据进行加密，私钥用于对数据进行解密。而【私钥加密，公钥解密】被用于RSA数字签名，私钥用于对数据进行签名，公钥用于对签名进行验证。下面是二者算法的不同：

  首先我们用密钥生成算法生成公钥和私钥：![img](https://gitee.com/bright_xu/blog-image/raw/master/202203282117703.png)。以安全常数![img](https://gitee.com/bright_xu/blog-image/raw/master/202203282117712.png)作为输入，输出一个公钥PK，和一个私钥SK。安全常数![img](file:///C:/Users/DELL/AppData/Local/Temp/msohtmlclip1/01/clip_image004.png)用于确定这个加密算法的安全性有多高，一般以加密算法使用的质数p的大小有关。越大，质数p一般越大，保证体制有更高的安全性。在RSA中，密钥生成算法如下：算法首先随机产生两个不同大质数p和q，计算N=pq。随后，算法计算欧拉函数 ![img](C:/Users/DELL/AppData/Local/Temp/msohtmlclip1/01/clip_image006.png)，接下来，算法随机选择一个小于![img](C:/Users/DELL/AppData/Local/Temp/msohtmlclip1/01/clip_image008.png)的整数e，并计算e关于![img](file:///C:/Users/DELL/AppData/Local/Temp/msohtmlclip1/01/clip_image008.png)的模反元素。最后得到公钥为PK=(N,e)，私钥为SK=(N,d)。

在RSA加密算法中，加密算法以公钥PK和待加密的消息M作为输入，输出密文CT，密文![img](C:/Users/DELL/AppData/Local/Temp/msohtmlclip1/01/clip_image010.png)。解密算法以私钥SK和密文CT作为输入，输出消息M。在RSA中，解密算法如下：算法直接输出明文为![img](C:/Users/DELL/AppData/Local/Temp/msohtmlclip1/01/clip_image012.png)。可以看出【公钥加密，私钥解密】是为了让别人用公钥加密数据，然后只有我知道私钥，能把数据解开，私钥起到解密效果，解开被加密的数据。

  在RSA数字签名中，签名算法以私钥SK和待签名的消息M作为输入，输出签名![img](https://gitee.com/bright_xu/blog-image/raw/master/202203282117173.png)，签名![img](https://gitee.com/bright_xu/blog-image/raw/master/202203282117175.png)。验证算法以公钥PK，签名![img](file:///C:/Users/DELL/AppData/Local/Temp/msohtmlclip1/01/clip_image014.png)以及消息M作为输入，输出一个比特值b。b=1意味着验证通过，b=0意味着验证不通过。在数字签名中，验证算法首先计算![img](C:/Users/DELL/AppData/Local/Temp/msohtmlclip1/01/clip_image018.png)，随后对比M'与M，如果相等，则输出b=1，否则输出b=0。可以看出【私钥加密，公钥解密】是为了用私钥加密数据作为签名，然后将数据附带着签名一同发布出去。当别人用公钥解开数据时，就说明签名是我发的，私钥起到认证效果，证明我的身份。

### 3. 书写数字签名的注释，每行都干了些什么？并任意举一个例子使得result=False。

```python
n = b'This is a test message'   #要加密的信息
h = SHA.new()   #SHA是安全哈希函数，实例化一个h对象
h.update(n)     #对n进行哈希映射
print('Hash:',h.hexdigest(),'length:',len(h.hexdigest())*4)    #打印16进制的字符串，并输出其长度

sign_txt = 'sign.txt'  #用sign_txt表示签名文件

with open('master-private.pem') as f:   #打开私钥文件
    key = f.read()   #读取私钥
    private_key = RSA.importKey(key)  #导入RSA私钥
    hash_obj = SHA.new(n)   #实例化哈希对象
    signer = Signature_pkcs1_v1_5.new(private_key)  #用私钥实例化一个signer签名者对象
    d = base64.b64encode(signer.sign(hash_obj))  #使sign函数返回签名字符串，然后用Base64编码赋值给d

f = open(sign_txt,'wb')   #打开sign.txt文件
f.write(d)   #将d写入到文件中
f.close()    #关闭文件

with open('master-private.pem') as f:  #打开私钥文件
    key = f.read()  #读取私钥
    public_key = RSA.importKey(key) #导入RSA公钥
    sign_file = open(sign_txt,'r')   #用sign_file 表示签名文件
    sign = base64.b64decode(sign_file.read())   #用Base64解码签名字符串，赋值给sign
    h = SHA.new(n)   #实例化哈希对象
    verifier = Signature_pkcs1_v1_5.new(public_key)  #用公钥实例化一个verifier验证者对象
    print('result:', verifier.verify(h,sign))  #将哈希对象和签名字符串作为参数，验证者验证签名是否为真

```

