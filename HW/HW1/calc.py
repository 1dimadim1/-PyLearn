while True:
    print("please insert two variables and sign (example: '2 2 *')")
    x, y, sign = input().split()
    x = int(x)
    y = int(y)
    if sign == '+':
        print(x+y)
    elif sign == '-':
        print(x-y)        
    elif sign == '*':
        print(x*y)      
    elif sign == '/':
        print(x/y)        
    else:
        print("wrong sign")