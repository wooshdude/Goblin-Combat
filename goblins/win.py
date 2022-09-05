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

print(logo)

print('//////////////////////////////////')
print('     WELCOME TO GOBLIN COMBAT!')
print('//////////////////////////////////\n')

print('Select an option')
print('[1] Start')
print('[2] Config')
print('[3] Credits')


def gameLoop():
    value = int(input('\nEnter selection: '))

    if value == 1:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Starting")
        os.system('python3 goblin_dev.py')
    elif value == 2:
        print('Please check')

gameLoop()