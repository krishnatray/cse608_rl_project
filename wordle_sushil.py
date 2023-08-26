#!/usr/bin/env python
# coding: utf-8



import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from colorama import Fore, Back, Style

def feedback_plus(guess, target):
    # Green = Correct Place  = score = 3
    # Yellow = Wrong place    = score = 1 
    # Black = letter does not exist in target score = 0
    
    score = 0
    txt = ""
    for i in range(5):
        if guess[i] == target[i]:
            txt += Fore.GREEN+ Back.BLACK + guess[i] + " "
            score += 1
        elif guess[i] in target:
            txt += Fore.YELLOW+ Back.BLACK + guess[i] + " "
        else:
            txt += Fore.WHITE + Back.BLACK + guess[i] + " "
        
    return (txt, score)

words_df = pd.read_csv("5_letters.csv")
words_df['word'] = words_df['1'] + words_df['2'] + words_df['3'] + words_df['4'] +  words_df['5']
words_list = words_df['word'].to_list()


def play_game():
    target =  random.choice(words_list).upper()
    for i in range(6):
        guess = input("Guess:").upper()
        txt, score = feedback_plus(guess, target)
        print(txt)
        if score == 5:
            print("Correct Guess!!")
            break

    print("Correct Word:", target) 


if __name__ == "__main__":
    play_game()




