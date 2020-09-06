#!/usr/bin/env python
import tkinter as tk
import shelve
import pdb

class Item:
    numItems = 0

    def __init__(self,  name, onHover, toClipboard):
        self.name = name
        self.onHoverMessage = onHover
        self.toClipboard = toClipboard
        self.num = Item.numItems
        Item.numItems += 1
        self.button = tk.Button(display, text=name,width="15",height="2",\
            command=self.onClick,  activebackground="#4444ff")
        self.button.grid(column=self.num//20,row=self.num%20 + 1)

    def onClick(self):
        display.clipboard_clear()
        display.clipboard_append(self.toClipboard)

    def changeValue(self, message, change):
        if if_found(message, "name"):
            self.name = change
            self.button.configure(text=change)
            return 0
        if if_found(message, "message"):
            self.onHover = change
            return 1
        if if_found(message, "value"):
            self.toClipboard = change
            return 2
        raise Exception

def custom_input(message):
    value = input(message)
    if if_found(value, "stop"):
        db.close()
        exit()
    return value

def if_found(command, search):
    return command.lower().find(search) > -1


display = tk.Tk()
display.grid()
io_dict = {}

db = shelve.open("clikboard_pickle", writeback=True)
for key in db.keys():
    args = db[key]
    io_dict[key] = Item(args[0], args[1], args[2])

while True:
    command = custom_input("That is the command? ")
    if if_found(command, "name"):
        name = custom_input("Please specify name: ")
        message = custom_input("Hover Message: ")
        clipboardValue = custom_input("Clipboard value: ")
        io_dict[name] = Item(name, message, clipboardValue)
        db[name] = [name, message, clipboardValue]
    if if_found(command, "delete"):
        try:
            name = custom_input("What name of the item you want to delete? ")
            del db[name]
            io_dict[name].button.destroy()
            del io_dict[name]
        except:
            print("There is no such key!")
    if if_found(command, "change"):
        try:
            item = custom_input("What is the item you want to change? ")
            attr = custom_input("What attribute do you want to change? ")
            change = custom_input("What do you want to change to? ")
            index = io_dict[item].changeValue(attr, change)
            db[item][index] = change
        except:
            print("Wrong index or item name")
    if if_found(command, "list"):
        print(io_dict.keys())
    if if_found(command, "help"):
        print("name, list, delete, change are the commands.")

display.mainloop()
