import os
import json


sxf_key = [
    'Saber',
    'Lancer',
    'Archer',
    'Rider',
    'Caster',
    'Assassin',
    'Berserker',
    'Shielder'
]

sxf_value = [
    'Archer',
    'Saber',
    'Lancer',
    'Assassin',
    'Rider',
    'Caster',
    'Shielder',
    'Berserker'
]


def byte_lock(byte, flag=7):
    # 对字节流按flag位进行亦或操作
    byte_lock = map(lambda x: x ^ flag, byte)
    return bytes(byte_lock)


def encrypt(infile, outfile, key='Saber', key_if=False, name_if=False):
    # 对全文件的字节流按key进行加密,并在文件头中写入相关信息
    if key not in sxf_key:
        return False
    with open(outfile, 'wb') as outf:
        if key_if:
            value = sxf_value[sxf_key.index(key)]
            outf.write(chr(len(value)).encode())
            buff = value.encode()
            outf.write(byte_lock(buff))
        else:
            outf.write(bytes([0]))

        if name_if:
            outf.write(chr(len(infile)).encode())
            buff = infile.encode()
            outf.write(byte_lock(buff))
        else:
            outf.write(bytes([0]))

        flag = 1 << sxf_key.index(key)
        with open(infile, 'rb') as inf:
            buff = inf.read(1024)
            while buff:
                outf.write(byte_lock(buff, flag))
                buff = inf.read(1024)
    return True


def decrypt(infile, outfile, key='Archer'):
    # 先读取文件头的相关信息,再根据key对文件进行解密
    with open(infile, 'rb') as inf:
        key_len = ord(inf.read(1))
        buff = inf.read(key_len)
        key_ = byte_lock(buff).decode()
        if not key:
            key = key_
        if key not in sxf_key:
            return False

        name_len = ord(inf.read(1))
        buff = inf.read(name_len)
        outfile_ = byte_lock(buff).decode()
        if not outfile:
            outfile = outfile_
        if not outfile:
            return False

        flag = 1 << sxf_value.index(key)
        with open(outfile, 'wb') as outf:
            buff = inf.read(1024)
            while buff:
                outf.write(byte_lock(buff, flag))
                buff = inf.read(1024)
    return True


def enbiter(infile, key='Saber'):
    # 对原文件的头部信息按key进行加密,适合大文件
    if key not in sxf_key:
        return False
    with open(infile, 'rb+') as inf:
        flag = 1 << sxf_key.index(key)
        buff = inf.read((1 + sxf_key.index(key)) << 20)
        inf.seek(0)
        inf.write(byte_lock(buff, flag))
    return True


def debiter(infile, key='Archer'):
    # 对加密文件头部信息按key进行解密
    if key not in sxf_key:
        return False
    with open(infile, 'rb+') as inf:
        flag = 1 << sxf_value.index(key)
        buff = inf.read((1 + sxf_key.index(key)) << 20)
        inf.seek(0)
        inf.write(byte_lock(buff, flag))
    return True


def batch_enbiter(key='Saber'):
    # 用key批量加密当前文件夹下所有文件,并重命名
    # 把文件对应关系写到0文件中
    names = {}
    ret = False
    for i, n in enumerate(os.listdir()):
        if os.path.isfile(n) and not n.endswith('py'):
            if enbiter(n, key):
                os.rename(n, str(i + 1))
                names[str(i + 1)] = n
                print(n + ' 加密成功')
            else:
                print(n + ' 加密失败')
                break
    else:
        print('批量加密完成')
        ret = True
    if ret:
        with open('0', 'wb') as f:
            buff = byte_lock(json.dumps(names).encode())
            f.write(buff)
    return ret


def batch_debiter(key='Archer'):
    # 读取0文件的文件名对应关系
    # 用key批量解密当前文件家下面所有文件
    with open('0', 'rb') as f:
        buff = byte_lock(f.read())
        names = json.loads(buff)
    for i, n in names.items():
        if debiter(i, key):
            print(i + ' 解密成功')
            os.rename(i, n)
        else:
            print(i + ' 解密失败')
            return False
    else:
        print('批量解密完成')
    return True
