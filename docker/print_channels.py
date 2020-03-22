with open("channels.txt", "w", encoding='utf-8') as fout:
    for i in range(1, 61):
        if i < 10:
            fout.write("0" + str(i) + "kanava\t\t\t")
            fout.write("0" + str(i) + "kanava\n\n\n")
        else:
            fout.write(str(i) + "kanava\t\t\t")
            fout.write(str(i) + "kanava\n\n\n")
