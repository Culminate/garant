from lxml import html
from tkinter import *
from tkinter import ttk




# pers = tree.xpath('//div[@class = "pers"]')[0]

# td = pers.xpath('.//td[not(@class = "name")]')

# for x in td:
#     print(x.text)


serverlist = ("Баалбек", "Хуньхуянь", "Выньсуньхунь")
classlist = ("Призыватель", "Убиватель", "Охуеватель")
guildlist = ("Нейтрал", "Бигвар")
label = [
["Сервер",  0, 0], 
["Уровень", 0, 2], 
["Питомец", 0, 4], 
["Класс",   1, 0], 
["Трофеи",  1, 2],
["Уровень", 1, 4], 
["Скилы",   2, 0], 
["Гильдия", 3, 0]
]

frames = list()

def guiinit():
    root = Tk()
    root.title("Garant editor")
    root.geometry('600x400+600+300')
    root.resizable(False, False)
    return root

def guilabel(frame):
    for x in label:
        Label(frame, text=x[0]).grid(row=x[1], column=x[2])

def guibox(frame, pers):
    serverbox = ttk.Combobox(frame, width=20, values=serverlist, state="readonly")
    levelbox = Entry(frame, width=6)
    petbox = Entry(frame, width=10)
    classbox  = ttk.Combobox(frame, width=20, values=classlist, state="readonly")
    trofibox = Entry(frame, width=6)
    petlevelbox = Entry(frame, width=6)
    skillbox = Entry(frame, width=50)
    guildbox = ttk.Combobox(frame, width=10, values=guildlist, state="readonly")
    delbtn = Button(frame, text = "Удалить")
    changebtn = Button(frame, text = "Изменить")

    serverbox.grid(row=0, column=1)
    levelbox.grid(row=0, column=3)
    petbox.grid(row=0, column=5)
    classbox.grid(row=1, column=1)
    trofibox.grid(row=1, column=3)
    petlevelbox.grid(row=1, column=5)
    skillbox.grid(row=2, column=1, columnspan=5)
    guildbox.grid(row=3, column=1)
    delbtn.grid(row=3, column=5)
    changebtn.grid(row=3, column=4)

def lxmlinit():
    file = open("pers.html", "r")
    text = file.read()
    tree = html.fromstring(text)
    return tree


def main():
    tree = lxmlinit()
    root = guiinit()

    sortframe = Frame(root, bd = 10)
    persframe = Frame(root, bd = 10)

    sortframe.pack(side="left",  fill="y")
    persframe.pack(side="right", fill="y")

    pers = tree.xpath('//div[@class = "pers"]')

    for x in pers:
        pframe = Frame(persframe, bd = 5)
        frames.append(pframe)
        guilabel(pframe)
        guibox(pframe, pers)
        pframe.pack()
    
    root.mainloop()

main()


# def Quit(ev):
#     global root
#     root.destroy()
    
# root = Tk()

# panelFrame = Frame(root, height = 60, bg = 'gray')
# textFrame = Frame(root, height = 340, width = 600)

# panelFrame.pack(side = 'top', fill = 'x')
# textFrame.pack(side = 'bottom', fill = 'both', expand = 1)

# textbox = Text(textFrame, font='Arial 14', wrap='word')
# scrollbar = Scrollbar(textFrame)

# scrollbar['command'] = textbox.yview
# textbox['yscrollcommand'] = scrollbar.set

# textbox.pack(side = 'left', fill = 'both', expand = 1)
# scrollbar.pack(side = 'right', fill = 'y')

# loadBtn = Button(panelFrame, text = 'Load')
# saveBtn = Button(panelFrame, text = 'Save')
# quitBtn = Button(panelFrame, text = 'Quit')

# quitBtn.bind("<Button-1>", Quit)

# loadBtn.place(x = 10, y = 10, width = 40, height = 40)
# saveBtn.place(x = 60, y = 10, width = 40, height = 40)
# quitBtn.place(x = 110, y = 10, width = 40, height = 40)

# root.mainloop()

# print(html.tostring(pers, encoding="utf-8"))