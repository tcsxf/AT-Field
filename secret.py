sxf_key=['Saber','Lancer','Archer','Rider','Caster','Assassin','Berserker','Shielder']
encode_bytes=[]


def encrypt(infile,outfile,key,key_if=False,name_if=False):
    with open(outfile,'wb') as outf:
        if key_if:
            outf.write(chr(len(key)).encode())
            key_bytes = bytes(key,encoding='utf8')
            encode_bytes.clear()
            for byte in key_bytes:
                encode_bytes.append(byte^7)
            outf.write(bytes(encode_bytes))
        else:
            outf.write(bytes([0]))

        if name_if:
            outf.write(chr(len(infile)).encode())
            name_bytes = bytes(infile,encoding='utf8')
            encode_bytes.clear()
            for byte in name_bytes:
                encode_bytes.append(byte^7)
            outf.write(bytes(encode_bytes))
        else:
            outf.write(bytes([0]))

def decrypt(infile,outfile=None,key=None):
    with open(infile,'rb') as inf:
        key_len=ord(inf.read(1))
        if key_len:
            key_bytes = inf.read(key_len)
            encode_bytes.clear()
            for byte in key_bytes:
                encode_bytes.append(byte^7)
            print(bytes(encode_bytes).decode('utf8'))

        name_len=ord(inf.read(1))
        if name_len:
            name_bytes = inf.read(name_len)
            encode_bytes.clear()
            for byte in name_bytes:
                encode_bytes.append(byte^7)
            print(bytes(encode_bytes).decode())

encrypt('tmp','outtmp','Saber',True,True)
decrypt('outtmp')