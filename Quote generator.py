import random
import json
import tkinter as tk
import Quote_adder

#Палитра фонов
main_background = '#fff0c8'
labels_background = '#c89650'
text_background = '#fff0dc'
history = []

quotes ,authors, themes, choiced_themes, choiced_authors, author_listbox, themes_listbox = [], [], [], [], [], [], []

lab_text = 'Выберите фильтры для отображения определенных цитат (авторы и тема)'

try:
    with open('Quotes history.json', encoding='utf-8') as file:
        history = json.load(file)
except FileNotFoundError: history = []
except json.decoder.JSONDecodeError: lab_text = 'Файл истории поврежден'

#Функции для работы
def update():
    global quotes, lab_text
    try:
        file = open('Quotes list.json', encoding='utf-8')
        quotes = json.load(file)
        file.close()
        try:
            for author in authors: author_listbox.insert(tk.END, author)
            for theme in themes: themes_listbox.insert(tk.END, theme)
        except NameError: ''
    except FileNotFoundError: main_label['text'] = 'Файла с цитатами нет'
    except json.decoder.JSONDecodeError: main_label['text'] = 'Файл с цитатами поврежден'

def select_authors():
    global choiced_authors
    choiced_authors = []
    for i in reversed(author_listbox.curselection()):
        choiced_authors.append(author_listbox.get(i))
    if choiced_authors: authors_selection_label['text'] = 'Автор(ы) выбраны'
    else: authors_selection_label['text'] = ''

def select_themes():
    global choiced_themes
    choiced_themes = []
    for i in reversed(themes_listbox.curselection()):
        choiced_themes.append(themes_listbox.get(i))
    if choiced_themes: themes_selection_label['text'] = 'Тема(ы) выбраны'
    else: themes_selection_label['text'] = ''

def generate():
    global choiced_authors, choiced_themes
    variants = []
    if choiced_themes and choiced_authors:
        for quote in quotes:
            if (quote['theme'] in choiced_themes) and (quote['author'] in choiced_authors):
                variants.append({'author':quote['author'], 'theme':quote['theme'], 'text':quote['text']})
    elif (choiced_themes) and (not choiced_authors):
        for quote in quotes:
            if quote['theme'] in choiced_themes:
                variants.append({'author': quote['author'], 'theme': quote['theme'], 'text': quote['text']})

    elif (not choiced_themes) and (choiced_authors):
        for quote in quotes:
            if quote['author'] in choiced_authors:
                variants.append({'author': quote['author'], 'theme': quote['theme'], 'text': quote['text']})
    else:
        for quote in quotes:
            variants.append({'author': quote['author'], 'theme': quote['theme'], 'text': quote['text']})

    if variants:
        res_quote = random.choice(variants)
        res = f'"{res_quote["text"]}" \n {res_quote["author"]}'
        res_text.delete('1.0', tk.END)
        res_text.insert('1.0', res)
        history.append(f' "{res_quote["text"]}" - {res_quote["author"]}')
        with open('Quotes history.json', 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=4, ensure_ascii=False)
    else:
        res_text.delete('1.0', tk.END)
        res_text.insert('1.0', 'Цитата не найдена')



def adding_window(): Quote_adder.adding_window()
def history_window(): Quote_adder.history_window()



update()

for quote in quotes:
    authors.append(quote['author'])
    themes.append(quote['theme'])
authors = sorted(list(set(authors)))
themes = sorted(list(set(themes)))


showing_window = tk.Tk()
showing_window.title('Генератор случайных цитат')
showing_window.geometry('600x500')
showing_window.minsize(600, 500)
showing_window.configure(bg = main_background)

main_label = tk.Label(showing_window, bg=labels_background, fg = 'white' , font = 'Arial 13' ,text = lab_text)
main_label.pack(pady = 10, fill = tk.X)
authors_selection_label = tk.Label(showing_window, fg = 'black', text = '', bg = main_background)
themes_selection_label = tk.Label(showing_window, fg = 'black', text= '', bg = main_background)
authors_selection_label.place(relx=0.25, y=50, anchor = 'center')
themes_selection_label.place(relx=0.75, y=50, anchor = 'center')

author_listbox = tk.Listbox(showing_window, width=40, height=10, selectmode='multiple', bg = text_background)
author_listbox.place(relx=0.25, y = 150, anchor = 'center')

themes_listbox = tk.Listbox(showing_window, width=40, height=10, selectmode='multiple', bg = text_background)
themes_listbox.place(relx=0.75, y = 150, anchor = 'center')

for author in authors: author_listbox.insert(tk.END, author)
for theme in themes: themes_listbox.insert(tk.END, theme)

tk.Button(command=select_authors, text='Выбрать авторов', relief='flat', bg= labels_background, fg ='white').place(relx=0.25, y= 250, anchor = 'center')
tk.Button(command=select_themes, text='Выбрать темы', relief='flat', bg= labels_background, fg ='white').place(relx=0.75, y= 250, anchor = 'center')
tk.Button(command=generate, text='Сказать что-нибудь', relief='flat', bg= labels_background, width=2360, font= 'Arial 13', fg = 'white').place(relx=0.5, y= 300, anchor = 'center')
res_text = tk.Text(showing_window, bg = text_background, height= 6, font= 'Arial 11', width= 70, wrap='word')
res_text.place(relx=0.5, y = 330, anchor = 'n')

tk.Button(text = 'Добавить от себя', relief='flat', bg= labels_background, fg ='white', command=adding_window).place(x=290, y= 465, anchor = 'e')
tk.Button(text = 'История', relief='flat', bg= labels_background, fg ='white', command=history_window).place(x=310, y= 465, anchor = 'w')


showing_window.mainloop()