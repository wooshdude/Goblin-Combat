import time
import os

logo = '''                                                        
              ####              
           %%%%%%&&&&&          
         &&&&&&&&&&@@@@@        
        &@@@@@@@@@@@@@@@@       
     ###  ^^^ ^^^^^ ^^^  ###    
   %&&&&&  ^   ^^^   ^  &&&&@&  
  &&&@@@@@   ^     ^   @@@@@@@@ 
 &@@@@###   ^^^   ^^^   ###@@@@@
          @@^^^@@@^^^@@         
          %@@@@@@@@@@@%         
              &&&&&                                                                                                      
'''
# logo = logo.replace(' ', '^')
# logo = logo.replace('(', ' ')
# logo = logo.replace('*', ' ')
# logo = logo.replace('.', ' ')
# logo = logo.replace(',', ' ')
# logo = logo.replace('/', ' ')


def main():
    print(logo)

    print('//////////////////////////////////')
    print('     WELCOME TO GOBLIN COMBAT!')
    print('//////////////////////////////////\n')

    print('Select an option')
    print('[1] Start')
    print('[2] Config')
    print('[3] Credits')

    value = int(input('\nEnter selection: '))

    if value == 1:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Starting")
        os.system('cd goblins')
        os.system('python goblins/goblin_dev.py')
    elif value == 2:
        os.system('notepad config.json' if os.name == 'nt' else 'nano config.json')
        main()
    elif value == 3:
        credits()


def credits():
    os.system('cls' if os.name == 'nt' else 'clear')
    f = open('credits.txt')
    for line in f.readlines():
        print(line)
        time.sleep(1)
    f.close()
    main()

main()