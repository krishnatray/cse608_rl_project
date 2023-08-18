#
# Wordle.py
#

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import random
import time

dictionary = []
record = []

hide_st_style = """  <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
#header {visibility: hidden;} 
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

with st.sidebar:
    
    credits_text = """

## CSE608 AI wih Reinforcement Learning July 2023
- Project: Wordle Reinforcement Learning
---------------------

## Project Team:
- Alok Gupta https://linkedin.com/in/alok-gupta-innovator 
- Sushil K Sharma https://linkedin.com/in/krishnatray 
- Fang Wang https://www.linkedin.com/in/fangwang12/ 
- Joyce Cheng https://www.linkedin.com/in/joyce-cheng-2872a688/ 
---------------------
## Professor:
Yongchang Feng (yongchang_feng@yahoo.com)

California Science and Technology University
https://www.cstu.edu/
              
"""
    st.markdown(credits_text) 


def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

local_css("wordle.css")

with open('5_letters.csv', 'r') as file:
    reader = csv.reader(file)
    listlist = list(reader)
    
for i in range(len(listlist)-1):
    dictionary.append(''.join(listlist[i+1]))
     
def wordle_feedback(target_word, guess_word):
    green = [(i, g) for i, (t, g) in enumerate(zip(target_word, guess_word)) if t == g]
    remaining = [(i, t, g) for i, (t, g) in enumerate(zip(target_word, guess_word)) if t != g]
    
    remaining_target = [t for i, t, g in remaining]
    yellow = []
    black = []

    for i, t, g in remaining:
        if g in remaining_target:
            yellow.append((i, g))
            remaining_target.remove(g)  # Remove the letter from the target list so it can't be used again
        else:
            black.append((i, g))

    return {"green": green, "yellow": yellow, "black": black}

def colored_text(target_word, guess_word):

    list_target = list(target_word.upper())
    list_guess = list(guess_word.upper())
    green_template = """<span class='highlight green'>
                        <span class='bold'>__letter__
                        </span> 
                        </span> """
    
    yellow_template = """<span class='highlight2 yellow'>
                        <span class='bold'>__letter__
                        </span> 
                        </span> """
   
    black_template = """<span class='highlight2 black'>
                        <span class='bold'>__letter__
                        </span> 
                        </span> """
    colored_str = ""
    for ltr_guess, ltr_target in zip(list_guess, list_target):
        if ltr_guess == ltr_target:
            colored_str = colored_str + green_template.replace("__letter__",ltr_guess)
            # print(colored_str)
        elif ltr_guess in list_target:
            colored_str = colored_str + yellow_template.replace("__letter__",ltr_guess)
        else:
            colored_str = colored_str + black_template.replace("__letter__",ltr_guess)
            
    colored_str = "<div>" + colored_str + "</div>"
    return colored_str

def nextguess(d):
    #find a key with a maximum value.  Choose randomly if there is a tie
    
    import random
    
    max_val = max(d.values())
    keys_with_max_val = [key for key, value in d.items() if value == max_val]
    return random.choice(keys_with_max_val)

def is_consistent(word, feedback):
    # Create list from word and a copy for yellow check
    word_list = list(word)
    remaining_letters = word_list.copy()

    # 'green' checks: correct letter must be at the correct index
    for index, letter in feedback['green']:
        if word_list[index] != letter:
            return False
        remaining_letters.remove(letter)  # Mark as used

    # 'yellow' checks: correct letter can't be at the same index, but must exist elsewhere
    for index, letter in feedback['yellow']:
        if word_list[index] == letter or letter not in remaining_letters:
            return False
        remaining_letters.remove(letter)  # Mark as used

    # 'black' checks: letter must not be in the word at all
    for index, letter in feedback['black']:
        if letter in remaining_letters:
            return False

    return True


def create_Qtable(dictionary):
    
    dict = {key: 0 for key in dictionary} #create dictionary
    
    for key1 in dict: #step through potential target words
        for key2 in dict: #step through each word in dictrionary
            
            feedback = wordle_feedback(key1, key2) #feedback for traget key1 compared with guess key2
            
            for key3 in dict: #computing reduction in length of dictionary by chosing key1 for each key2
                
                inconsistent = 0 #reset counter 
                
                if not is_consistent(key3, feedback):
                    inconsistent += 1 #counting how many words are eliminated from dicationary 
                    
                dict[key2] = dict[key2] + inconsistent #updates key2 for reduction in length of dictionary
                #Updating Qtable
        
    return(dict)

def format_word(guess):
    return " ".join(list(guess.upper())) 

def play_wordle(word, display_output=False):
    """ 
    
    """
    guess = "cares"
    if display_output:

        st.markdown(f"# Target: {format_word(word)}")
        colored_guess = colored_text(word, guess)
        st.markdown(colored_guess, unsafe_allow_html=True)

    feedback = wordle_feedback(word, guess)
    
    remaining_dict = []
    
    for wordtest in dictionary:
        if is_consistent(wordtest, feedback):
            remaining_dict.append(wordtest)
            
   
    for i in range(2,55):
        Qtable = create_Qtable(remaining_dict)
        guess = nextguess(Qtable)
        remaining_dict.remove(guess)
        
        if display_output:
            colored_guess = colored_text(word, guess)
            time.sleep(0.5)
            st.write(" ")
            st.markdown(colored_guess, unsafe_allow_html=True)
        feedback = wordle_feedback(word, guess)
        # st.write("Feedback = ", feedback)
        if len(feedback['green']) == 5:
            record.append(i)
            break
            
        temp = []
            
        for wordtest in remaining_dict:    
            if is_consistent(wordtest, feedback):
                temp.append(wordtest)
                
        remaining_dict = temp 
    return i


st.title("Wordle! - Reinforcement Learning Demo!")

tab1, tab2, tab3 = st.tabs(["Single Game", "Multigame Simulation", "Manual Play"])

with tab1:
    st.header("Single Play Simulation")
    play_button = st.button("Play Game", key="1")

    if play_button:
        word = random.choice(dictionary)
        result = play_wordle(word, True)
        st.markdown(f"# Total Tries [{result}]")
        st.balloons()

with tab2:
    st.header("Mutiple Games Simulation")
    num_games = st.number_input("Number of Games [1-2500]", value = 20, min_value = 1, max_value=2500)
    play_num_button = st.button("Run Simulation", key="2")
    
    if play_num_button:
        results = []
        progress_bar = st.progress(0, "Running simulation..")
        i = 0 
        for game in range(num_games):
            progress_bar.progress((i+1)/num_games, text= "Running simulation..")
            word = random.choice(dictionary)
            result = play_wordle(word, False)
            results.append(result) 
            i += 1

        arr_results = np.array(results)
        avg_tries = np.mean(arr_results)
        st.markdown(f"Mean {avg_tries: 0.2f}")        
        fig, ax = plt.subplots()
        ax.hist(arr_results)
        st.pyplot(fig)

with tab3:
    st.header("Manual Play Simulation")

    word = st.text_input("Please enter a 5 letter word:",max_chars=5)

    play_button_manual = st.button("Play Game", key="3")

    if play_button_manual:
        if len(word) == 5:
            if word not in dictionary:
                dictionary.append(word)

            result = play_wordle(word, True)
            st.markdown(f"# Total Tries [{result}]")
            st.balloons()
        else:
            st.error("Please enter a word of length 5")




