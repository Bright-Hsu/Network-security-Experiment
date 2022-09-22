# -*- coding: utf-8 -*-

from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA

# 伪随机数生成器
random_generator = Random.new().read
# rsa算法生成实例
rsa = RSA.generate(1024, random_generator)
 
# master的秘钥对的生成
private_pem = rsa.exportKey()
 
with open('master-private.pem', 'wb') as f:
  f.write(private_pem)
 
public_pem = rsa.publickey().exportKey()
with open('master-public.pem', 'wb') as f:
  f.write(public_pem)


import base64
message = b"hello, this is a plian text"
with open('master-public.pem') as f:
    key = f.read()
    rsakey = RSA.importKey(key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(message))
    print ('加密后:',cipher_text)



with open('master-private.pem') as f:
    key = f.read()
    rsakey = RSA.importKey(key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    text = cipher.decrypt(base64.b64decode(cipher_text), random_generator)
    print ('解密的原文:',text)


n = b'This is a test message'   #要加密的信息
h = SHA.new()   #SHA是安全哈希函数，实例化一个h对象
h.update(n)     #对n进行哈希映射
print('Hash:',h.hexdigest(),'length:',len(h.hexdigest())*4)    #打印16进制的字符串，并输出其长度

sign_txt = 'sign.txt'  #用sign_txt代指TXT文件

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





