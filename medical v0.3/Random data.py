import random

def GBK2312():# 随机生成汉字
    head = random.randint(0xb0, 0xf7)
    body = random.randint(0xa1, 0xfe)
    val = f'{head:x} {body:x}'
    str = bytes.fromhex(val).decode('gb2312')
    return str

for i in range(100):
    print(GBK2312())