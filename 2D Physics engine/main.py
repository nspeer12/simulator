import calculate
import time

def main():
    print('Physics simulator')
    print('type your number equation(1-4) or ')
    print('type ball to simulate a ball drop')
    inp = input(':>')
    if inp == '1':
        calculate.eq1()
    if inp == '2':
        calculate.eq2()
    if inp == '3':
        calculate.eq3()
    if inp == '4':
        calculate.eq4()
    if inp == 'ball':
        import simulate
        simulate.main()
    else:
        time.sleep(1)
        main()
    
main()
