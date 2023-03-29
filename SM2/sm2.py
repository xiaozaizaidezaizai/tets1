#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @ProjectName: Demo
# @Name: gm_test.py.py
# @Auth: lqn
# @Date: 2022/9/6-14:06
# @Desc: 
# @Ver : 0.0.0.1
from SM2.gmssl import sm2 as SM2
from SM2.gmssl import sm3 as SM3
from SM2.gmssl import func as GMFunc
from random import SystemRandom
from base64 import b64encode, b64decode


class CurveFp:  #曲线

    def __init__(self, A, B, P, N, Gx, Gy, name):
        self.A = A
        self.B = B
        self.P = P
        self.N = N
        self.Gx = Gx
        self.Gy = Gy
        self.name = name


class SM2Key:
    sm2p256v1 = CurveFp(   #曲线初始化
        name="sm2p256v1",
        A=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC,
        B=0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93,
        P=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF,
        N=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123,
        Gx=0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7,
        Gy=0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
    )

    @staticmethod
    def multiply(a, n, N, A, P):#点，私钥，
        return SM2Key.fromJacobian(SM2Key.jacobianMultiply(SM2Key.toJacobian(a), n, N, A, P), P)

    @staticmethod
    def add(a, b, A, P):
        return SM2Key.fromJacobian(SM2Key.jacobianAdd(SM2Key.toJacobian(a), SM2Key.toJacobian(b), A, P), P)

    @staticmethod
    def inv(a, n):
        if a == 0:
            return 0
        lm, hm = 1, 0
        low, high = a % n, n
        while low > 1:
            r = high // low
            nm, new = hm - lm * r, high - low * r
            lm, low, hm, high = nm, new, lm, low
        return lm % n

    @staticmethod
    def toJacobian(Xp_Yp):
        Xp, Yp = Xp_Yp
        return Xp, Yp, 1

    @staticmethod
    def fromJacobian(Xp_Yp_Zp, P):
        Xp, Yp, Zp = Xp_Yp_Zp
        z = SM2Key.inv(Zp, P)
        return (Xp * z ** 2) % P, (Yp * z ** 3) % P

    @staticmethod
    def jacobianDouble(Xp_Yp_Zp, A, P):
        Xp, Yp, Zp = Xp_Yp_Zp
        if not Yp:
            return 0, 0, 0
        ysq = (Yp ** 2) % P
        S = (4 * Xp * ysq) % P
        M = (3 * Xp ** 2 + A * Zp ** 4) % P
        nx = (M ** 2 - 2 * S) % P
        ny = (M * (S - nx) - 8 * ysq ** 2) % P
        nz = (2 * Yp * Zp) % P
        return nx, ny, nz

    @staticmethod
    def jacobianAdd(Xp_Yp_Zp, Xq_Yq_Zq, A, P):
        Xp, Yp, Zp = Xp_Yp_Zp
        Xq, Yq, Zq = Xq_Yq_Zq
        if not Yp:
            return Xq, Yq, Zq
        if not Yq:
            return Xp, Yp, Zp
        U1 = (Xp * Zq ** 2) % P
        U2 = (Xq * Zp ** 2) % P
        S1 = (Yp * Zq ** 3) % P
        S2 = (Yq * Zp ** 3) % P
        if U1 == U2:
            if S1 != S2:
                return 0, 0, 1
            return SM2Key.jacobianDouble((Xp, Yp, Zp), A, P)
        H = U2 - U1
        R = S2 - S1
        H2 = (H * H) % P
        H3 = (H * H2) % P
        U1H2 = (U1 * H2) % P
        nx = (R ** 2 - H3 - 2 * U1H2) % P
        ny = (R * (U1H2 - nx) - S1 * H3) % P
        nz = (H * Zp * Zq) % P
        return nx, ny, nz

    @staticmethod
    def jacobianMultiply(Xp_Yp_Zp, n, N, A, P):
        Xp, Yp, Zp = Xp_Yp_Zp
        if Yp == 0 or n == 0:
            return (0, 0, 1)
        if n == 1:
            return (Xp, Yp, Zp)
        if n < 0 or n >= N:
            return SM2Key.jacobianMultiply((Xp, Yp, Zp), n % N, N, A, P)
        if (n % 2) == 0:
            return SM2Key.jacobianDouble(SM2Key.jacobianMultiply((Xp, Yp, Zp), n // 2, N, A, P), A, P)
        if (n % 2) == 1:
            mv = SM2Key.jacobianMultiply((Xp, Yp, Zp), n // 2, N, A, P)
            return SM2Key.jacobianAdd(SM2Key.jacobianDouble(mv, A, P), (Xp, Yp, Zp), A, P)


class PrivateKey:
    def __init__(self, curve=SM2Key.sm2p256v1, secret=None):#私钥初始化
        self.curve = curve#曲线各参数
        self.secret = secret or SystemRandom().randrange(1, curve.N)#在设的初始值中随机生成 【私钥d】

    def PublicKey(self):
        curve = self.curve#曲线各参数
        xPublicKey, yPublicKey = SM2Key.multiply((curve.Gx, curve.Gy), self.secret, A=curve.A, P=curve.P, N=curve.N)
        return PublicKey(xPublicKey, yPublicKey, curve) # 调用公钥类

    def ToString(self):

        return "{}".format(str(hex(self.secret))[2:].zfill(64))
        # str(hex(self.secret)) 长度为66 需要将前面的【0x】去除
        # hex()函数用于将一个指定数字转换为 16 进制数，以字符串形式表示。
        # zfill()方法用零垫串来填充左边宽度。

class PublicKey:#产生公钥的方法
    def __init__(self, x, y, curve):
        self.x = x
        self.y = y
        self.curve = curve

    def ToString(self, compressed=True):
        return '04' + {
            True: str(hex(self.x))[2:],
            False: "{}{}".format(str(hex(self.x))[2:].zfill(64), str(hex(self.y))[2:].zfill(64))
        }.get(compressed)


class SM2Util:
    def __init__(self, pub_key=None, pri_key=None):
        self.pub_key = pub_key
        self.pri_key = pri_key
        self.sm2 = SM2.CryptSM2(public_key=self.pub_key, private_key=self.pri_key)

    def Encrypt(self, data):
        info = self.sm2.encrypt(data.encode())
        return b64encode(info).decode()

    def Decrypt(self, data):
        info = b64decode(data.encode())
        return self.sm2.decrypt(info).decode()

    def Sign(self, data):
        "self.sm2.para_len=64，产生随机数。"
        random_hex_str = GMFunc.random_hex(self.sm2.para_len)
        print('vs=',data.encode())#bytes类型
        sign = self.sm2.sign(data.encode(), random_hex_str)
        return sign

    def Verify(self, data, sign):
        return self.sm2.verify(sign, data.encode())

    @staticmethod#静态方法
    def GenKeyPair():
        pri = PrivateKey()#私钥【调用初始化方法】
        pub = pri.PublicKey()#公钥
        return pri.ToString(), pub.ToString(compressed=False)#返回私钥和公钥


def SM2_Key():
    return SM2Util.GenKeyPair()

def main():
    """
    主函数
    :return:
    """
    import random

    e = SM2Util.GenKeyPair()#元组数据(分别是私钥和公钥){生成公私钥}
    # e = ('', '')
    print(type(e))
    print('私钥:{} \n公钥:{}'.format(e[0], e[1]))


    vs = '1'#字符
    data =vs 
    print('原数据:{}'.format(data))

    print(e[1][2:])#将添加的‘04’剔除
    sm2 = SM2Util(pri_key=e[0], pub_key=e[1][2:])#此对象变量含有密钥
    sign = sm2.Sign(data)#返回  R, S
    #print (type(sign))
    print('签名:{} 验签:{}'.format(sign, sm2.Verify(data, sign)))#签名值 (r,s）


    cipher = sm2.Encrypt(data)
    print('加密:{}\n解密:{}'.format(cipher, sm2.Decrypt(cipher)))

    #数据和加密后数据为bytes类型[]
    #data = b"222" # bytes类型
    bytes_data=sign.encode()
    y = SM3.sm3_hash(GMFunc.bytes_to_list(bytes_data))
    print('sm3值:')
    print(y)

if __name__ == '__main__':
    main()
