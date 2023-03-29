# python
# -*- coding: UTF-8 -*-
'''
@Project ：tets1 
@File    ：MHE.py
@IDE     ：PyCharm 
@Author  ：jinwenbo
@Date    ：2023/3/4 18:03 
'''

import rsa

def keyGen(keysize=1024):
    '''
    生成keysize比特的公私密钥, 默认keysize=1024
    '''
    (pubkey, privkey) = rsa.newkeys(keysize)
    return (pubkey, privkey)


def save_key(key, filename):
    '''
    key是密钥
    filename是文件名, 默认为pem格式
    '''
    try:
        with open(filename, 'w') as f:#wb以二进制写模式打开 (参见 w )
        #    key = key.save_pkcs1()
            f.write(key)
            return True
    except Exception as e:
        raise ValueError(str(e))


def load_key(filename, mode=0):
    '''
    filename是文件名, 默认为pem格式
    mode取值为0 or 1 分别代表读取的是公钥还是私钥
    '''
    try:
        with open(filename, 'r') as f:
            keydata = f.read(-1)
            if mode == 1:
                key = rsa.PrivateKey.load_pkcs1(keydata)
            else:
                key=1
                print(key)
              #  key = rsa.PublicKey.load_pkcs1(keydata)
            #return key
            #print(key)
    except Exception as e:
        raise ValueError(str(e))

'''自己覆写的加密方法'''
def load_ket_my(filename, mode=0):
    '''
       filename是文件名, 默认为pem格式
       mode取值为0 or 1 分别代表读取的是公钥还是私钥
       '''
    try:
        with open(filename, 'r') as f:
            keydata = f.read(-1)
            if mode == 1:
                key = rsa.PrivateKey.load_pkcs1(keydata)
            else:

                key = rsa.PublicKey.load_pkcs1(keydata)
            # return key
                print(key)
    except Exception as e:
        raise ValueError(str(e))


def Encrypt_int(m, pubkey):
    '''
    m 明文
    pubkey 公钥
    '''
    return rsa.core.encrypt_int(m, pubkey.e, pubkey.n)


def Decrypt_int(c, privkey):
    '''
    c 密文
    privkey 私钥
    '''
    return rsa.core.decrypt_int(c, privkey.d, privkey.n)


def Evaluate_int(c1, c2, pubkey):
    '''
    c1, c2 密文
    pubkey 公钥
    Note: c1 * c2对应明文整数相乘应该小于公钥中的n
    '''
    return c1 * c2 % pubkey.n


if __name__ == "__main__":
    (pubkey, privkey) = keyGen(1024)
    # save_key(pubkey, './key/public_key.pem')
    # save_key(privkey, './key/private_key.pem')

    # pubkey = load_key('./key/public_key.pem', 0)
    # privkey = load_key('./key/private_key.pem', 1)

    num = 1
  #  print(Encrypt_int(1, pubkey))

    # num1 = 2
    # num2 = 3
    # ans = Decrypt_int(Evaluate_int(Encrypt_int(num1, pubkey), Encrypt_int(num2, pubkey), pubkey), privkey)
    # print(ans)
    ''''自己'''
    load_key('F:\\BiShe\\PY_Writer1\\tets1\\key\\private_key.txt',0)