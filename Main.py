# Description: This program will allow to the user to search for stories from the website https://www.wattpad.com/
# and download them in pdf format and html.
# Author: Mia Ruiz (mruiz): miarg49@gmail.com
import os
import tkinter as tk
import re
from wattpad_scraper import Wattpad as wt


# validate if is Mac OS or Windows OS
if os.name == "nt":
    directory = "./booksShelf"
if os.name != "nt":
    directory = "./BookShelf"

terminal_var = None
terminal_log = None
terminal = None


# Create a function to translate the text to spanish, call the function like this: translateTo(line)

# Create a function to add more lines to a string variable and print it in the terminal
def add_line_to_terminal(line):
    global terminal_log, terminal
    terminal_log.set(terminal_log.get() + line + "\n\n")
    terminal.update()


# Create interface for the user to interact with the program
def create_window():
    window = tk.Tk()
    window.title("Web Scrapping Downloader")
    window.geometry("600x600")
    window.resizable(True, True)
    return window


# Create a function to add a label to the window and a input field to get the url from the user
def add_url_label(window):
    url_label = tk.Label(window, text="Enter the books hashtags to look for")
    url_label.pack()
    queryToSearch = tk.Entry(window, width=50)
    queryToSearch.pack()
    queryToSearch.focus()
    button_download = tk.Button(
        window, text="Process books", command=lambda: searchBooks(queryToSearch.get())
    )
    button_download.pack()


# Create a function to add a terminal to the window
def add_terminal_log(window):
    global terminal_var, terminal_log, terminal
    tk.Label(window).pack()
    terminal_var = "Initializing program...\n\n"
    terminal_log = tk.StringVar()
    terminal_log.set(terminal_var)
    terminal = tk.Label(window, width=80, textvariable=terminal_log)
    terminal.pack()


def searchBooks(query: str):
    w = wt()
    w.login(username="", password="")
    # validate if the query starts with https://www.wattpad.com/ if it does, remove it
    books = []
    if query == "n":
        query = "179829885"

    isUrl = query.isalnum()
    if isUrl:
        query = f"https://www.wattpad.com/story/{query}"
        add_line_to_terminal(f"URL: {query}")
        books.append(w.get_book_by_url(url=query))

    if not isUrl:
        booksNonMature = w.search(
            query, mature=False, completed=True, limit=10000, paid=False, free=True
        )
        booksMature = w.search(
            query, mature=True, completed=True, limit=10000, paid=False, free=True
        )
        # merge both lists into one list, not repeating the books.
        books = list(set(booksNonMature + booksMature))
    processBooks(books)


def processBooks(books):
    booksProcessed = 0
    add_line_to_terminal(f"Encontrados: {str(len(books))}")

    for book in books:
        add_line_to_terminal(
            f"Titulo: {book.title}, Autor: {book.author.name}, URL: {book.url}"
        )
        # regex to replace all the special characters in the title
        regex = r"[^\w\s]"
        rtitle = re.sub(regex, "", book.title)

        if not os.path.exists(directory):
            os.makedirs(directory)
        # save the book in html format
        try:
            filePath = directory + "/" + rtitle + ".html"
            add_line_to_terminal(f"Directorio: {filePath}")
            # loop in the book information to organize the data and save it in a file with the name of the title of the book with html format
            with open(filePath, "w", encoding="utf-8") as file:
                print(book)
        # Catch the exception message and print it
        except Exception as e:
            add_line_to_terminal(f"Error del metodo de guardado: {e}")

        booksProcessed += 1
        add_line_to_terminal(
            f"Porcentaje de Libros pendientes de procesar: {(booksProcessed / len(books)) * 100} %"
        )


if __name__ == "__main__":
    window = create_window()
    add_url_label(window)
    add_terminal_log(window)
    window.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
