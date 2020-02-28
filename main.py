from secret import *

tp = input('模式:1高级加密 2简单加密 3批量加密 4获取信息\n')
inf = input('文件\\目录名称:\n')
if tp in ('1', '2', '3'):
    act = input('动作:1加密 2解密\n')
    key = input('输入秘钥\n')
if tp == '1':
    outf = input('输出文件名:\n')
    if act == '1':
        name_if = input('输入任意字符文件名写入\n')
        key_if = input('输入任意字符秘钥写入\n')
        if encrypt(inf, outf, key, name_if, key_if):
            print('加密成功')
    elif act == '2':
        if decrypt(inf, outf, key):
            print('解密成功')
elif tp == '2':
    if act == '1':
        if ezbiter(inf, key):
            print('加密成功')
    elif act == '2':
        if ezbiter(inf, key):
            print('解密成功')
elif tp == '3':
    rec = input('输入任意字符递归操作子文件夹\n')
    if act == '1':
        if batch_biter(inf, key, rec):
            print('批量加密成功')
    elif act == '2':
        if batch_debiter(inf, key, rec):
            print('批量解密成功')
elif tp == '4':
    get_key(inf)
else:
    print('操作失败')
