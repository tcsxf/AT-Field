import hashlib
import random
import os
import json


def xor(byte, key, flag=32):
    # byte: 输入字节流
    # key: 加密关键字
    # flag: 取的散列值字节数
    # 函数对key散列到256位，取其中的flag个字节，位数扩充到>=输入的位数，两者进行异或
    sha = hashlib.sha256()
    sha.update(key.encode('utf-8'))
    code = sha.digest()[:flag]
    length = len(byte) // flag + 1
    code = code * length
    ret = map(lambda x: x[0] ^ x[1], zip(byte, code))
    return bytes(ret)


def encrypt(infile, outfile, key='Saber', nm_if=False, key_if=False):
    # 对全文件的字节流按key进行加密,并在文件头中写入相关信息
    with open(outfile, 'wb') as outf:
        if nm_if:
            buff = os.path.basename(infile).encode()
            outf.write(chr(len(buff)).encode())
            outf.write(bytes(map(lambda x: x ^ 255, buff)))
        else:
            outf.write(bytes([0]))
        if key_if:
            buff = key.encode()
            outf.write(chr(len(buff)).encode())
            outf.write(bytes(map(lambda x: x ^ 255, buff)))
        else:
            outf.write(bytes([0]))
        flag = random.randint(17, 32)
        outf.write(chr(flag).encode())
        with open(infile, 'rb') as inf:
            buff = inf.read(1024)
            while buff:
                outf.write(xor(buff, key, flag))
                buff = inf.read(1024)
    return True


def decrypt(infile, outfile, key='Saber'):
    # 先读取文件头的相关信息,再根据key对文件进行解密
    with open(infile, 'rb') as inf:
        nm_len = ord(inf.read(1))
        inf.read(nm_len)
        key_len = ord(inf.read(1))
        inf.read(key_len)

        flag = ord(inf.read(1))
        with open(outfile, 'wb') as outf:
            buff = inf.read(1024)
            while buff:
                outf.write(xor(buff, key, flag))
                buff = inf.read(1024)
    return True


def get_key(infile):
    with open(infile, 'rb') as inf:
        nm_len = ord(inf.read(1))
        nm = inf.read(nm_len)
        if nm:
            nm_ = bytes(map(lambda x: x ^ 255, nm)).decode()
            print(f'原文件名:{nm_}')
        else:
            print('无法获取原文件名')
        key_len = ord(inf.read(1))
        key = inf.read(key_len)
        if key:
            key_ = bytes(map(lambda x: x ^ 255, key)).decode()
            print(f'KEY:{key_}')
        else:
            print('无法获取KEY')


def ezbiter(infile, key='Saber'):
    # 对原文件的头部信息按key进行加密,适合大文件
    with open(infile, 'rb+') as inf:
        buff = inf.read(1 << 20)
        inf.seek(0)
        inf.write(xor(buff, key))
    return True


def batch_biter(key='Saber', path='.', rec=False):
    # 用key批量加密当前文件夹下所有文件,并重命名
    # 把文件对应关系写到0.sxf文件中
    names = {}
    ret = False
    for i, n in enumerate(os.listdir(path)):
        fd = os.path.join(path, n)
        # 判断读写权限
        if not os.access(fd, 6) or fd[-3:] in ('BIN', 'bin', 'sys', '.py', 'pyc', 'dea'):
            continue
        if rec and os.path.isdir(fd):
            batch_biter(key, fd, rec)
            continue
        elif os.path.isfile(fd):
            if ezbiter(fd, key):
                os.rename(fd, os.path.join(path, str(i + 1) + '.sxf'))
                names[str(i + 1) + '.sxf'] = n
            else:
                break
    else:
        ret = True
    if ret:
        with open(os.path.join(path, '0.sxf'), 'wb') as f:
            buff = bytes(map(lambda x: x ^ 255, json.dumps(names).encode()))
            f.write(buff)
    return ret


def batch_debiter(key='Saber', path='.', rec=False):
    # 读取0文件的文件名对应关系
    # 用key批量解密当前文件夹下面所有文件
    for i, n in enumerate(os.listdir(path)):
        fd = os.path.join(path, n)
        if rec and os.path.isdir(fd):
            batch_debiter(key, fd, rec)
            continue
        if n == '0.sxf':
            with open(fd, 'rb') as f:
                buff = bytes(map(lambda x: x ^ 255, f.read()))
                names = json.loads(buff.decode())
            for k, v in names.items():
                if ezbiter(os.path.join(path, k), key):
                    os.rename(os.path.join(path, k), os.path.join(path, v))
                else:
                    return False
            os.remove(fd)
    return True
