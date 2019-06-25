from secret import *


tp = input('模式:1高级加密 2简单加密 3批量加密\n')
act = input('动作:1加密 2解密\n')
key = input('输入秘钥\n')
if tp == '1':
    infile = input('原文件名:\n')
    outfile = input('输出文件名:\n')
    if act == '1':
        key_if = input('输入任意字符秘钥写入\n')
        name_if = input('输入任意字符文件名写入\n')
        if encrypt(infile, outfile, key, key_if, name_if):
            print('加密成功')
    elif act == '2':
        if decrypt(infile, outfile, key):
            print('解密成功')
elif tp == '2':
    infile = input('原文件名:\n')
    if act == '1':
        if enbiter(infile, key):
            print('加密成功')
    elif act == '2':
        if debiter(infile, key):
            print('解密成功')
elif tp == '3':
    rec = input('输入任意字符递归操作子文件夹\n')
    if act == '1':
        if batch_enbiter(key, rec=rec):
            print('批量加密成功')
    elif act == '2':
        if batch_debiter(key, rec=rec):
            print('批量解密成功')
else:
    print('操作失败')
