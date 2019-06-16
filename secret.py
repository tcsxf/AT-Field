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

sxf_value =[
    'Archer',
    'Saber',
    'Lancer',
    'Assassin',
    'Rider',
    'Caster',
    'Shielder',
    'Berserker'
]


def biter(infile,key='Saber'):
    if key not in sxf_key:
        return False
    with open(infile,'rb+') as inf:
        flag = 1<<sxf_key.index(key)
        buff = inf.read(1024*flag)
        buff = map(lambda x: x ^ flag, buff)
        inf.seek(0)
        inf.write(bytes(buff))

def unbiter(infile,key='Archer'):
    if key not in sxf_key:
        return False
    with open(infile,'rb+') as inf:
        flag = 1<<sxf_value.index(key)
        buff = inf.read(1024*flag)
        buff = map(lambda x: x ^ flag, buff)
        inf.seek(0)
        inf.write(bytes(buff))


def encrypt(infile, outfile, key, key_if=False, name_if=False):
    if key not in sxf_key:
        return False
    with open(outfile, 'wb') as outf:
        if key_if:
            outf.write(chr(len(key)).encode())
            buff = bytes(sxf_value[sxf_key.index(key)], encoding='utf8')
            buff = map(lambda x: x ^ 7, buff)
            outf.write(bytes(buff))
        else:
            outf.write(bytes([0]))

        if name_if:
            outf.write(chr(len(infile)).encode())
            buff = bytes(infile, encoding='utf8')
            buff = map(lambda x: x ^ 7, buff)
            outf.write(bytes(buff))
        else:
            outf.write(bytes([0]))

        flag = 1<<sxf_key.index(key)
        with open(infile, 'rb') as inf:
            buff = inf.read(1024)
            while buff:
                buff = map(lambda x: x ^ flag, buff)
                outf.write(bytes(buff))
                buff = inf.read(1024)
    return True


def decrypt(infile, outfile='', key=''):
    with open(infile, 'rb') as inf:
        key_len = ord(inf.read(1))
        buff = inf.read(key_len)
        key_ = bytes(map(lambda x: x ^ 7, buff)).decode('utf8')
        if not key:
            key = key_
        if key not in sxf_key:
            return False

        name_len = ord(inf.read(1))
        buff = inf.read(name_len)
        outfile_ = bytes(map(lambda x: x ^ 7, buff)).decode('utf8')
        if not outfile:
            outfile = outfile_
        if not outfile:
            return False

        flag = 1<<sxf_value.index(key)
        with open(outfile, 'wb') as outf:
            buff = inf.read(1024)
            while buff:
                buff = map(lambda x: x ^ flag, buff)
                outf.write(bytes(buff))
                buff = inf.read(1024)
    return True


if __name__ == '__main__':
    slt = input('请选择:1.加密\t2.解密')
    if slt == '1':
        infile = input('原文件')
        outfile = input('输出文件')
        key = input('秘钥')
        keyif = input('秘钥写入输入任意字符')
        nameif = input('文件名写入输入任意字符')
        if encrypt(infile, outfile, key, bool(key), bool(nameif)):
            print('文件加密成功')
        else:
            print('文件加密失败')
    elif slt == '2':
        infile = input('加密文件')
        outfile = input('输出文件')
        key = input('秘钥')
        if decrypt(infile, outfile, key):
            print('文件解密成功')
        else:
            print('文件解密失败')
    else:
        print('输入不正确')