from __future__ import print_function
import sys
import json
import os

import fbchat
from fbchat.models import *

user_file = '.data/current_user.txt'
cookies_file = '.data/cookies.txt'
    
def run(client):
    current_user = client.fetchUserInfo(client.uid)[client.uid]
    print('Welcome to FbTool, {}!\n'.format(current_user.first_name))
    printCommands()

    while(True):
        try:
            print('> ', end='')
            input = sys.stdin.readline().rstrip('\n')
            cmd = input.split(' ', 1)[0]

            if len(cmd) == 0:
                continue
            elif cmd == 'send':
                args = input.split(' ', 2)
                sendMessages(args[1], args[2])
            elif cmd == 'help':
                printCommands()
            elif cmd == 'quit':
                return
            else:
                print('Invalid command: {}. Try again.'.format(cmd))
        except KeyboardInterrupt:
            return
        except:
            print('Unexpected error: {}'.format(sys.exc_info()))

def sendMessages(users_file, message):
    '''
    Send message to all users listed in user_file

    :param users_file: .txt file with one name per line
    :param message: The message to send
    '''
    
    names = [line.rstrip('\n').rstrip('\r') for line in open(users_file)]
    print('Sending \'{}\' to {}'.format(message, names))

    for name in names:
        friend = client.searchForUsers(name)[0]
        print(friend)
        client.sendMessage(message, thread_id=friend.uid, thread_type=ThreadType.USER)

def writeMetadata(client):
    current_user = client.fetchUserInfo(client.uid)[client.uid]
    
    # Save user first name
    print('Writing user name to {}'.format(user_file))
    with open(user_file, 'w') as user_f:
        user_f.write(current_user.first_name)
    
    # Save cookies
    print('Writing cookies to {}'.format(cookies_file))
    with open(cookies_file, 'w') as cookie_f:
        json.dump(client.getSession(), cookie_f)

def printCommands():
    print('Commands:')
    print('\tsend <users_file> <message>')
    print('\t\tusers_file: .txt file with one name per line')
    print('\t\tmessage: The message to send')
    print('\thelp')
    print('\t\tPrint the help menu')
    print('\tquit')
    print('\t\tExit the program')

if __name__ == '__main__':
    print('Welcome to FbTool!')
    
    cookies = None
    if os.path.isfile(user_file) and os.path.isfile(cookies_file):
        with open(user_file, 'r') as user_f:
            name = user_f.read().rstrip('\n').rstrip('\r')
            print('Found login info for {}. Is this you? (y/n): '.format(name), end='')
            try:
                option = sys.stdin.readline()[0]
                if (option == 'y'):
                    with open(cookies_file, 'r') as cookie_f:
                        cookies = json.load(cookie_f)
                        client = fbchat.Client(None, None, max_tries=3, session_cookies=cookies)
            except KeyboardInterrupt:
                exit()
            except:
                print('Unexpected exception: {}'.format(sys.exc_info()))

    # Prompt user for login information if didn't load cookies
    if cookies == None:
        while(True):
            print('Enter your email: ', end='')
            email = sys.stdin.readline().rstrip('\n')
            print('Enter your password: ', end='')
            password = sys.stdin.readline().rstrip('\n')

            try:
                client = fbchat.Client(email, password, max_tries=3)
                # Save user information
                writeMetadata(client)
                break
            except FBchatUserError:
                print('Login error: {}'.format(sys.exc_info()))
    
    run(client)
    print('\nThanks for using FbTool!')