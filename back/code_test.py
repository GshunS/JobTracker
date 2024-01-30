for i in range(1, 101):
    string = ''
    if i % 3 == 0:
        string += 'Site'
    if i % 5 == 0:
        string += 'Host'
    if string == '':
        print(i)
    else:
        print(string)