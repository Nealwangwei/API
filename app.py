import random
a = random.randint(1, 100)
while True:
    guess_num = int(input('请输入您本次猜到数：'))
    if 1 <= guess_num <= 100:
        print('数字符合要求')
        if guess_num > a:
            print('猜大了')
        elif guess_num < a:
            print('猜小了')
        else:
            print('答对了')
else:
    print('不符合要求')


a = random.randint(1, 100)

while True:
    guess_num = int(input('请输入您猜的数字（1~100）：'))

    if not 1 <= guess_num <= 100:
        print('输入不符合要求，请输入1~100之间的数字')
        continue

    if guess_num > a:
        print('猜大了')
    elif guess_num < a:
        print('猜小了')
    else:
        print('答对了！')
        break
