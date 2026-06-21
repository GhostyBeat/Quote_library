import tkinter as tk
import json
main_background = '#fff0c8'
labels_background = '#c89650'
text_background = '#fff0dc'

quote_theme, quote_author, quote_text, add_theme, add_text, add_author, res_label, history = '','','','','','','',''


def history_window():
    global history
    history_text = ''
    try:
        with open('Quotes history.json', 'r', encoding='utf-8') as file:
            history = json.load(file)
            if history:
                for hi in history: history_text += hi + '\n'
            else: history_text = 'История отсутствует'
    except FileNotFoundError: history_text = 'История отсутствует.'
    except json.decoder.JSONDecodeError: history_text = 'Файл истории поврежден'

    history_window = tk.Tk()
    history_window.geometry('600x300')
    history_window.minsize(600, 240)
    history_window.resizable(False, False)
    history_window.configure(bg=main_background)
    history_window.title('История цитат')
    tk.Label(history_window, bg=labels_background, fg='white', font='Arial 13', text='История').pack(pady=10, fill=tk.X)
    his_text = tk.Text(history_window, bg=text_background, height=6, font='Arial 11', width=70, wrap='word')
    his_text.pack(pady=10)
    his_text.insert('1.0', history_text)



def add_quote():
    quote_theme = add_theme.get()
    quote_text = add_text.get()
    quote_author = add_author.get()
    add_theme.delete(0, tk.END)
    add_text.delete(0, tk.END)
    add_author.delete(0, tk.END)
    if quote_theme and quote_text and quote_author:
        quote = {'author': quote_author, 'text': quote_text, 'theme': quote_theme}
        try:
            with open('Quotes list.json', 'r', encoding='utf-8') as file:
                quotes = json.load(file)
            quotes.append(quote)
            with open('Quotes list.json', 'w', encoding='utf-8') as file:
                json.dump(quotes, file, indent=4, sort_keys=True, ensure_ascii=False)
            res_label['text'] = 'Добавлено'
        except FileNotFoundError: res_label['text'] = 'Уже сказано, что файла с цитатами нет'
        except json.decoder.JSONDecodeError: res_label['text'] = 'Сказал же: файл с цитатами поврежден'
    else: res_label['text'] = 'Не все поля заполнены'


def adding_window():
    global add_theme, add_author, add_text, res_label
    adding_window = tk.Tk()
    adding_window.title('Добавить цитату')
    adding_window.geometry('600x240')
    adding_window.minsize(600, 240)
    adding_window.resizable(False, False)
    adding_window.configure(bg=main_background)
    tk.Label(adding_window, bg=labels_background, fg='white', font='Arial 13', text='Заполните все поля для добавления').pack(pady=10, fill=tk.X)

    tk.Label(adding_window, bg=main_background, fg='black', font='Arial 11', text='Тема:').place(y=50, anchor='w', x=10)
    tk.Label(adding_window, bg=main_background, fg='black', font='Arial 11', text='Цитата:').place(y=80, anchor='w', x=10)
    tk.Label(adding_window, bg=main_background, fg='black', font='Arial 11', text='Автор:').place(y=110, anchor='w', x=10)

    add_theme = tk.Entry(adding_window, bg=text_background, fg='black', font='Arial 11', width=50)
    add_text = tk.Entry(adding_window, bg=text_background, fg='black', font='Arial 11', width=50)
    add_author = tk.Entry(adding_window, bg=text_background, fg='black', font='Arial 11', width=50)

    res_label = tk.Label(adding_window, bg=labels_background, fg='white', font='Arial 13', text='', width=90)
    tk.Button(adding_window, command=add_quote, text='Добавить', relief='flat', bg=labels_background, width=2360, font='Arial 13', fg='white').place(relx=0.5, y=190, anchor='center')

    add_theme.place(x = 70, y = 50, anchor='w')
    add_text.place(x = 70, y = 80, anchor='w')
    add_author.place(x = 70, y = 110, anchor='w')
    res_label.place(relx = 0.5, y = 140, anchor='n')

    adding_window.mainloop()