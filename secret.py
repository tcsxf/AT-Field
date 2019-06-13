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


def decrypt(infile, outfile=None, key=None):
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
