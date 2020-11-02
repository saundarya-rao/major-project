#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[41]:


import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import *
import tkinter.filedialog

# Structure and Layout
window = Tk()
window.title("Summaryzer GUI")
window.geometry("700x400")
window.config(background='black')

style = ttk.Style(window)
# style.configure('lefttab.TNotebook', tabposition='wn',)


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
tab_control.add(tab3, text=f'{"URL":^20s}')
tab_control.add(tab4, text=f'{"Comparer ":^20s}')
tab_control.add(tab5, text=f'{"About ":^20s}')


label1 = Label(tab1, text= 'Summaryzer',padx=5, pady=5)
label1.grid(column=0, row=0)
 
label2 = Label(tab2, text= 'File Processing',padx=5, pady=5)
label2.grid(column=0, row=0)

label3 = Label(tab3, text= 'URL',padx=5, pady=5)
label3.grid(column=0, row=0)

label3 = Label(tab4, text= 'Compare Summarizers',padx=5, pady=5)
label3.grid(column=0, row=0)

label4 = Label(tab5, text= 'About',padx=5, pady=5)
label4.grid(column=0, row=0)

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
     l1.configure(text="Open File To Summarize")

def clear_text():
	entry.delete('1.0',END)

def clear_display_result():
	tab1_display.delete('1.0',END)


# Clear Text  with position 1.0
def clear_text_file():
	displayed_file.delete('1.0',END)

# Clear Result of Functions
def clear_text_result():
	tab2_display_text.delete('1.0',END)

# Clear For URL
def clear_url_entry():
	url_entry.delete(0,END)

def clear_url_display():
	tab3_display_text.delete('1.0',END)


# Clear entry widget
def clear_compare_text():
	entry1.delete('1.0',END)

def clear_compare_display_result():
	tab1_display.delete('1.0',END)


# Functions for TAB 2 FILE PROCESSER
# Open File to Read and Process
# def openfiles():
# 	file1 = tkinter.filedialog.askopenfilename(filetypes=(("Text Files",".txt"),("All files","*.*")))
# 	read_text = open(file1).read()
# 	displayed_file.insert(tk.END,read_text)

def openfiles():
    filename = filedialog.askopenfilename(initialdir='/', title='Select file', filetypes=(("video files",".mp4"),("all files","*.*")))
    l1.configure(text="File Selected: "+filename)

def get_file_summary():
	raw_text = displayed_file.get('1.0',tk.END)
	final_text = text_summarizer(raw_text)
	result = '\nSummary:{}'.format(final_text)
	tab2_display_text.insert(tk.END,result)

    
#FILE PROCESSING TAB
l1=Label(tab2,text="Open File To Summarize")
l1.grid(row=1,column=1)

# displayed_file = ScrolledText(tab2,height=7)# Initial was Text(tab2)
# displayed_file.grid(row=2,column=0, columnspan=3,padx=5,pady=3)


# BUTTONS FOR SECOND TAB/FILE READING TAB
b0=Button(tab2,text="Open File", width=12,command=openfiles,bg='#c5cae9')
b0.grid(row=3,column=0,padx=10,pady=10)

b1=Button(tab2,text="Reset ", width=12,command=clear_file,bg="#b9f6ca")
b1.grid(row=3,column=1,padx=10,pady=10)

b2=Button(tab2,text="Summarize", width=12,command=get_file_summary,bg='blue',fg='#fff')
b2.grid(row=3,column=2,padx=10,pady=10)

b3=Button(tab2,text="Clear Result", width=12,command=clear_text_result)
b3.grid(row=5,column=1,padx=10,pady=10)

b4=Button(tab2,text="Close", width=12,command=window.destroy)
b4.grid(row=5,column=2,padx=10,pady=10)

# Display Screen
# tab2_display_text = Text(tab2)
tab2_display_text = ScrolledText(tab2,height=10)
tab2_display_text.grid(row=7,column=0, columnspan=3,padx=5,pady=5)

# # Allows you to edit
# tab2_display_text.config(state=NORMAL)

window.mainloop()


# In[ ]:





# In[ ]:





# In[ ]:




