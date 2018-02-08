import times

while True:
    minute = time.strftime('%M',time.localtime(time.time()))
    print(minutes)
    if re.match(r'.*2$|.*3$|.*7$|.*8$',minute):
        time.sleep(3)
        continue
    else:
        print('程序运行！')
        time.sleep(3) 




