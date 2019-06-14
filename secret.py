sxf_key = {
    'Saber': [1, 5],
    'Lancer': [2, 4],
    'Archer': [3, 6],
    'Rider': [4, 2],
    'Caster': [5, 1],
    'Assassin': [6, 3],
    'Berserker': [7, 0],
    'Shielder': [0, 7]
}


def encrypt(infile, outfile, key, key_if=False, name_if=False):
    if key not in sxf_key:
        return False
    with open(outfile, 'wb') as outf:
        if key_if:
            outf.write(chr(len(key)).encode())
            buff = bytes(key, encoding='utf8')
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

        flag = sxf_key[key][0] ^ 7
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

        flag = (7 - sxf_key[key][1]) ^ 7
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
