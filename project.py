#!/usr/bin/env python
# coding: utf-8

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import *
from tkinter import filedialog
from moviepy.editor import *
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import nltk
import os
import re
import math
import operator
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize,word_tokenize
from tkinter.ttk import Progressbar
import shutil
import time
import threading
from tkinter import messagebox


nltk.download('averaged_perceptron_tagger')
Stopwords = set(stopwords.words('english'))
wordlemmatizer = WordNetLemmatizer()

class MyDialog:

    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)
        self.myLabel = tk.Label(top, text='Percentage of information to retain(in percent):')
        self.myLabel.pack()
        self.myEntryBox = tk.Entry(top)
        self.myEntryBox.pack()
        self.mySubmitButton = tk.Button(top, text='OK', command=self.send)
        self.mySubmitButton.pack()

    def send(self):
        self.value = self.myEntryBox.get()
        self.top.destroy()

def onClick():
    inputDialog = MyDialog(window)
    window.wait_window(inputDialog.top)
    print('Value: ', inputDialog.value)
    return inputDialog.value


# Structure and Layout
window = Tk()
window.title("Automatic Lecture Summarizer")
window.geometry("700x400")
window.resizable(0, 0)
window.config(background='white')

style = ttk.Style(window)

# TAB LAYOUT
tab_control = ttk.Notebook(window,style='lefttab.TNotebook')
 
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab4 = ttk.Frame(tab_control)
tab5 = ttk.Frame(tab_control)

# ADD TABS TO NOTEBOOK
tab_control.add(tab1, text=f'{"Home":^20s}')
tab_control.add(tab2, text=f'{"File":^20s}')
tab_control.add(tab3, text=f'{"About ":^20s}')


label1 = Label(tab1, text= 'Summaryzer',padx=5, pady=5)
label1.grid(column=0, row=0)
 
label2 = Label(tab2,padx=5, pady=5)
label2.grid(column=0, row=0)

label3 = Label(tab3, text= 'About',padx=5, pady=5)
label3.grid(column=0, row=0)

tab_control.pack(expand=1, fill='both')

# Functions 
def get_summary():
	raw_text = str(entry.get('1.0',tk.END))
	final_text = text_summarizer(raw_text)
	print(final_text)
	result = '\nSummary:{}'.format(final_text)
	tab1_display.insert(tk.END,result)


# Clear entry widget
def clear_file():
    l1.configure(text="Upload File To Summarize")
    if  os.path.exists("result.txt"):
        os.remove("result.txt")
    
# Clear Result
def clear_text_result():
    tab2_display_text.delete('1.0',END)
    if os.path.exists("summary.txt"):
        os.remove("summary.txt")
    
def VideoToText(input):
    pb.start()
    pb['value'] = 10
    pb.update()  
    mp3_file = "audio.wav"
    videoClip= VideoFileClip(input)
    pb['value'] = 20
    pb.update()  
    audioclip = videoClip.audio
    audioclip.write_audiofile(mp3_file)
    pb['value'] = 30
    pb.update()  
    audioclip.close()
    videoClip.close()  
    pb['value'] = 40
    pb.update() 
    time.sleep(1)
    path="audio.wav"
    pb['value'] = 50
    pb.update()  
    r = sr.Recognizer()
    sound = AudioSegment.from_wav(path)  
    chunks = split_on_silence(sound,
        min_silence_len = 1000,
        silence_thresh = sound.dBFS-14,
        keep_silence=1000,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    pb['value'] = 60
    pb.update()    
    time.sleep(1)
    pb['value'] = 70
    pb.update()      
    with open('result.txt',mode ='w') as file:
        pb['value'] = 80
        pb.update()      
        pb['value'] = 90
        pb.update()      
        file.write(whole_text)
        print("\nText file generated!")  
    pb['value'] = 100
    pb.update() 
    time.sleep(0.5)
    pb.stop()
    messagebox.showinfo('Info',"File uploaded")
    # return the text for all chunks detected
    return whole_text

def openfiles():
    filename = filedialog.askopenfilename(initialdir='/', title='Select file', filetypes=(("video files",".mp4"),("AVI files",".avi"),("all files",".*")))
    if filename:
        l1.configure(text="File Selected: "+filename)
        VideoToText(filename)
    
def lemmatize_words(words):
    lemmatized_words = []
    for word in words:
        lemmatized_words.append(wordlemmatizer.lemmatize(word))
    return lemmatized_words
def stem_words(words):
    stemmed_words = []
    for word in words:
        stemmed_words.append(stemmer.stem(word))
    return stemmed_words

def remove_special_characters(text):
    regex = r'[^a-zA-Z0-9\s]'
    text = re.sub(regex,'',text)
    return text

def freq(words):
    words = [word.lower() for word in words]
    dict_freq = {}
    words_unique = []
    for word in words:
        if word not in words_unique:
            words_unique.append(word)
    for word in words_unique:
        dict_freq[word] = words.count(word)
    return dict_freq

def pos_tagging(text):
    pos_tag = nltk.pos_tag(text.split())
    pos_tagged_noun_verb = []
    for word,tag in pos_tag:
        if tag == "NN" or tag == "NNP" or tag == "NNS" or tag == "VB" or tag == "VBD" or tag == "VBG" or tag == "VBN" or tag == "VBP" or tag == "VBZ":
             pos_tagged_noun_verb.append(word)
    return pos_tagged_noun_verb

def tf_score(word,sentence):
    freq_sum = 0
    word_frequency_in_sentence = 0
    len_sentence = len(sentence)
    for word_in_sentence in sentence.split():
        if word == word_in_sentence:
            word_frequency_in_sentence = word_frequency_in_sentence + 1
    tf =  word_frequency_in_sentence/ len_sentence
    return tf

def idf_score(no_of_sentences,word,sentences):
    no_of_sentence_containing_word = 0
    for sentence in sentences:
        sentence = remove_special_characters(str(sentence))
        sentence = re.sub(r'\d+', '', sentence)
        sentence = sentence.split()
        sentence = [word for word in sentence if word.lower() not in Stopwords and len(word)>1]
        sentence = [word.lower() for word in sentence]
        sentence = [wordlemmatizer.lemmatize(word) for word in sentence]
        if word in sentence:
            no_of_sentence_containing_word = no_of_sentence_containing_word + 1
    idf = math.log10(no_of_sentences/no_of_sentence_containing_word)
    return idf

def tf_idf_score(tf,idf):
    return tf*idf

def word_tfidf(dict_freq,word,sentences,sentence):
    word_tfidf = []
    tf = tf_score(word,sentence)
    idf = idf_score(len(sentences),word,sentences)
    tf_idf = tf_idf_score(tf,idf)
    return tf_idf

def sentence_importance(sentence,dict_freq,sentences):
    sentence_score = 0
    sentence = remove_special_characters(str(sentence)) 
    sentence = re.sub(r'\d+', '', sentence)
    pos_tagged_sentence = [] 
    no_of_sentences = len(sentences)
    pos_tagged_sentence = pos_tagging(sentence)
    for word in pos_tagged_sentence:
        if word.lower() not in Stopwords and word not in Stopwords and len(word)>1: 
            word = word.lower()
            word = wordlemmatizer.lemmatize(word)
            sentence_score = sentence_score + word_tfidf(dict_freq,word,sentences,sentence)
    return sentence_score
        
def get_file_summary():
    file = 'result.txt'
    file = open(file , 'r')
    text = file.read()
    tokenized_sentence = sent_tokenize(text)
    text = remove_special_characters(str(text))
    text = re.sub(r'\d+', '', text)
    tokenized_words_with_stopwords = word_tokenize(text)
    tokenized_words = [word for word in tokenized_words_with_stopwords if word not in Stopwords]
    tokenized_words = [word for word in tokenized_words if len(word) > 1]
    tokenized_words = [word.lower() for word in tokenized_words]
    tokenized_words = lemmatize_words(tokenized_words)
    word_freq = freq(tokenized_words)
    value = int(onClick())
    no_of_sentences = int((value * len(tokenized_sentence))/100)
    print("Total sentences: " + str(no_of_sentences))
    c = 1
    sentence_with_importance = {}
    for sent in tokenized_sentence:
        sentenceimp = sentence_importance(sent,word_freq,tokenized_sentence)
        sentence_with_importance[c] = sentenceimp
        c = c+1
    sentence_with_importance = sorted(sentence_with_importance.items(), key=operator.itemgetter(1),reverse=True)
    cnt = 0
    summary = []
    sentence_no = []
    for word_prob in sentence_with_importance:
        if cnt < no_of_sentences:
            sentence_no.append(word_prob[0])
            cnt = cnt+1
        else:
            break
    sentence_no.sort()
    cnt = 1
    for sentence in tokenized_sentence:
        if cnt in sentence_no:
            summary.append(sentence)
        cnt = cnt+1
    summary = " ".join(summary)
    print("\n")
    print("Summary:")
    print(summary)
    outF = open('summary.txt',"w")
    outF.write(summary)
    tab2_display_text.insert(tk.END,summary)
        
def save(): 
    files = [('Text Document', '*.txt'),
             ('All Files', '.'),  
             ('Python Files', '*.py')
             ]
    f = filedialog.asksaveasfile(mode='w', initialdir='/', title='Save file', filetypes=files, defaultextension = files)
    if f is None: 
        return
    text2save = str(tab2_display_text.get(1.0, END))
    f.write("Summary:")
    f.write("\n")
    f.write(text2save)
    f.close()
    messagebox.showinfo('Info',"Download successfully")
    

def close():
    os.remove("audio.wav")
    shutil.rmtree("audio-chunks")
    os.remove("result.txt")
    os.remove("summary.txt")
    window.destroy()
        
#FILE PROCESSING TAB
l1=Label(tab2,text="Upload File To Summarize")
l1.grid(row=1,column=1)

# BUTTONS FOR SECOND TAB/FILE READING TAB
b0=Button(tab2,text="Upload File", width=12,command=openfiles,bg='#d9b3ff')
b0.grid(row=3,column=0,padx=10,pady=10)

b1=Button(tab2,text="Reset ", width=12,command=clear_file,bg="#ffc299")
b1.grid(row=3,column=1,padx=10,pady=10)

b2=Button(tab2,text="Summarize", width=12,command=get_file_summary,bg='#ffffb3')
b2.grid(row=3,column=2,padx=10,pady=10)

b3=Button(tab2,text="Clear Result", width=12,command=clear_text_result,bg='#b3d9ff')
b3.grid(row=5,column=0,padx=10,pady=10)

b4=Button(tab2,text="Download", width=12,command=save,bg='#ccff99')
b4.grid(row=5,column=1,padx=10,pady=10)

b5=Button(tab2,text="Close", width=12,command=close,bg='#ff6666')
b5.grid(row=5,column=2,padx=10,pady=10)

# Display Screen
tab2_display_text = ScrolledText(tab2,height=10)
tab2_display_text.grid(row=20,column=0, columnspan=5,padx=5,pady=5)

pb = ttk.Progressbar(window, orient=HORIZONTAL, length=700, mode='determinate')
pb.pack()

window.mainloop()
