# #use eneable1.txt wordlist
# #to crack the password
# #Vigenère Solver

# import sys
# import os
# import time
# import itertools
# import string
# import re
# import hashlib
# import base64
# import binascii
# import argparse
# import threading
# import multiprocessing
# from multiprocessing import Process, Queue
# from threading import Thread
# from queue import Queue
# from itertools import cycle
# from collections import Counter
# from collections import defaultdict
import re
from collections import Counter


def is_english_score(text):
    # Define the set of all lowercase English letters
    letters = 'abcdefghijklmnopqrstuvwxyz'
    
    # Count frequencies of alphabetic characters in lowercase
    freq = Counter(char.lower() for char in text if char.isalpha())
    
    # Normalize frequencies
    total_count = sum(freq.values())
    freq = {char: count / total_count for char, count in freq.items()}
    
    # Expected frequencies of letters in English text (percentage)
    expected_freq = {'e': 0.1202, 't': 0.0910, 'a': 0.0812, 'o': 0.0768, 'i': 0.0731, 'n': 0.0695,
                     's': 0.0628, 'r': 0.0602, 'h': 0.0592, 'd': 0.0432, 'l': 0.0398, 'u': 0.0288,
                     'c': 0.0271, 'm': 0.0261, 'f': 0.0230, 'y': 0.0211, 'w': 0.0209, 'g': 0.0203,
                     'p': 0.0182, 'b': 0.0149, 'v': 0.0111, 'k': 0.0069, 'x': 0.0017, 'q': 0.0011,
                     'j': 0.0010, 'z': 0.0007}
    
    # Calculate chi-squared statistic
    chi_squared = sum((freq.get(char, 0) - expected_freq.get(char, 0))**2 / expected_freq.get(char, 0) for char in letters)
    
    # Determine if text is English based on chi-squared threshold
    if chi_squared == 0:
        return 0
    else:
        return 1/chi_squared


def vigenere(x,key):
    encrypt = False
    lst_final = []
    code = list(x)
    j = 0
	
    for i,char in enumerate(code):
        if char.isalpha():
            code[i] = key[(i+j)%len(key)]
            if encrypt:
                lst_final.append((ord(x[i]) + ord(code[i]) - 65 * 2) % 26)
            else:
                lst_final.append((ord(x[i]) - ord(code[i])) % 26)
        else:
            lst_final.append(ord(char))
            j -=1

    for i,char in enumerate(code):
        if char.isalpha():
            lst_final[i] = chr(lst_final[i] + 65)
        else:
            lst_final[i] = chr(lst_final[i])
			
    return ''.join(lst_final)

# def count_plaintext_words(plaintext):
#     words = plaintext.split()
#     count = 0
#     for word in words:
#         w= word.lower()
#         if w in wordlist:
#             count += 1
#     return count
    
cypher_text="QVRL YGQV P AMDG BWLVV YIH H TIKVRLWJ. VPTYI NCA PSWF C LDUOVA ICK E GQTXJI FHNXJII, DCI MVFO I IVXRNTN KMWHMGLRK OWKPI... XQWS DSIM. GDB HZF I GLEC HQCL AFTS RYETMQCN XYKA GPHUNM. NVY JJWLLH JMQASW ZP XNALFP, VTAAFTSH, VTVTIIPRX UGHAIDU ICK ME VPT ZGZGVRL SW UMRYITA. GDBV IKLSSI ZU LDUI YGZT: KEKC LDA GPDMG KSK QZV KSK KT HSEJJ VTAAFTSH ZPRUP RAJ JNIHO WLEKTZW UQB YWK RNT HTECN TTAXVTA"

def save_good_words():
    with open('good_words.txt', 'w') as f:
        for word in good_words:
            f.write('Key: %s\nPlaintext: %s\n\n' % (word[0], word[2]))
            f.write('grade: %d\n\n' % word[1])
            

# def main():
#     global verbose
#     global debug
#     global wordlistpath
#     global wordlist

#     wordlistpath = 'enable1.txt'

#     # Check if wordlist file exists
#     if not os.path.exists(wordlistpath):
#         print('Error: Wordlist file not found')
#         sys.exit(1)

#     # Read wordlist file
#     with open(wordlistpath, 'r') as f:
#         wordlist = f.read().splitlines()


#     # Decrypt the ciphertext
#     counter = 0
#     for word in wordlist:
#         counter += 1
#         plaintext = vigenere_decrypt(cypher_text, word)
#         count = count_plaintext_words(plaintext)
#         if count > 5:
#             #save it
#             print('Key: %s\nPlaintext: %s' % (word, plaintext))
#             save_plaintext(word, plaintext)
#         print('count: %d' % counter)



# if __name__ == '__main__':
#     main()


import os
import sys
import concurrent.futures

verbose = False
debug = False
wordlistpath = 'enable1.txt'
wordlist = []
good_words = []

def process_word(word,index):
    if index % 1000 == 0:
        print('Processed %d words' % index)

    plaintext = vigenere(cypher_text, word.upper())
    count = is_english_score(plaintext)

    # count = 0
    if count > 2:
        good_words.append((word, count, plaintext))
    return word

def main():
    global verbose
    global debug
    global wordlistpath
    global wordlist

    # Check if wordlist file exists
    if not os.path.exists(wordlistpath):
        print('Error: Wordlist file not found')
        sys.exit(1)

    # Read wordlist file
    with open(wordlistpath, 'r') as f:
        wordlist = f.read().splitlines()
    
    # Decrypt the ciphertext
    # i = 0
    # for word in wordlist:
    #     i += 1
    #     print('Processing word %d: %s' % (i, word))
    #     process_word(word, i)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i, word in enumerate(wordlist, start=1):
            executor.submit(process_word, word, i)
            
                
    
    for word in good_words:
        print('Key: %s\nPlaintext: %s' % (word[0], word[2]))
        print('grade: %d' % word[1])
    save_good_words()
    
    
        
if __name__ == "__main__":
    main()
    # print(is_english('hello world', english_words))
    #check cipher