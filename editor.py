from lxml import html
from tkinter import *
from tkinter import ttk

class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

class Garantlxml():
    """docstring for Garantlxml"""
    def __init__(self):
        self.lxmlinit()

    def lxmlinit(self):
        self.file = open("pers.html", "r+", encoding="utf-8")
        text = self.file.read()
        self.tree = html.fromstring(text) # , parser = html.HTMLParser(encoding='utf-8')
        self.file.close()

    def lxmlsave(self):
        self.file = open("pers.html", "w", encoding="utf-8")
        text = html.tostring(self.tree, encoding="utf-8")
        # print(text.decode("utf-8"))
        self.file.write(text.decode("utf-8"))
        self.file.close()

class GarantGui(Garantlxml):
    """docstring for GarantGui"""
    def __init__(self):
        self.root = Tk()
        self.root.title("Garant editor")
        self.root.geometry('600x400+600+300')
        self.root.resizable(False, False)

        self.pframes = list()

        self.lxmlinit()

        sortframe = Frame(self.root, bd = 10)
        persframe = VerticalScrolledFrame(self.root)

        pers = self.tree.xpath('//div[@class = "pers"]')

        for x in pers:
            pid = x.get("id")
            td = x.xpath('.//td[not(@class = "name")]')

            pframe = GarantPers(pid, x, persframe.interior, self.file)
            self.pframes.append(pframe)

        sortframe.pack(side = "left", fill="y", expand=True)
        persframe.pack(side = "right", fill="y")

    def mainloop(self):
        self.root.mainloop()

class GarantPers(Garantlxml):
    """docstring for GarantPers"""
    def __init__(self, id, ld, rootframe, file):
        super().__init__()
        self.frame = Frame(rootframe, bd = 5, relief="groove")

        td = ld.xpath('.//td[not(@class = "name")]')

        self.td = td
        self.ld = ld

        self.serverlist = ("Баалбек", "Югенес")
        self.classlist = ("Призыватель", "Ассасин", "Маг", "Рыцарь", "Рейнджер")
        self.guildlist = ("Нейтрал", "Бигвар")
        self.label = [
                        ["Сервер",  0, 0],
                        ["Уровень", 0, 2],
                        ["Питомец", 0, 4],
                        ["Класс",   1, 0],
                        ["Трофеи",  1, 2],
                        ["Уровень", 1, 4],
                        ["Скилы",   2, 0],
                        ["Гильдия", 3, 0]
                     ]

        self.guilabel(self.frame)
        self.guibox(self.frame, td)

        self.frame.pack()

    def guilabel(self, frame):
        for x in self.label:
            Label(frame, text=x[0]).grid(row=x[1], column=x[2])

    def guibox(self, frame, td):

        self.serverbox = ttk.Combobox(frame, width=20, values=self.serverlist, state="readonly")
        self.serverbox.set(td[0].text)

        self.levelbox = Entry(frame, width=6)
        self.levelbox.insert(0, td[1].text)

        self.petbox = Entry(frame, width=10)
        self.petbox.insert(0, td[2].text)

        self.classbox  = ttk.Combobox(frame, width=20, values=self.classlist, state="readonly")
        self.classbox.set(td[4].text)

        self.trofibox = Entry(frame, width=6)
        self.trofibox.insert(0, td[5].text)

        self.petlevelbox = Entry(frame, width=6)
        self.petlevelbox.insert(0, td[6].text)

        self.skillbox = Entry(frame, width=50)
        self.skillbox.insert(0, td[7].text)

        self.guildbox = ttk.Combobox(frame, width=10, values=self.guildlist, state="readonly")
        self.guildbox.set(td[3].text)
        self.delbtn = ttk.Button(frame, text = "Удалить")
        self.changebtn = ttk.Button(frame, text = "Изменить", command=self.Change)

        self.serverbox.grid(  row=0, column=1)
        self.levelbox.grid(   row=0, column=3)
        self.petbox.grid(     row=0, column=5)
        self.classbox.grid(   row=1, column=1)
        self.trofibox.grid(   row=1, column=3)
        self.petlevelbox.grid(row=1, column=5)
        self.skillbox.grid(   row=2, column=1, columnspan=5)
        self.guildbox.grid(   row=3, column=1)
        self.delbtn.grid(     row=3, column=5)
        self.changebtn.grid(  row=3, column=4)

    def Change(self):
        self.ld.xpath('.//td[not(@class = "name")]')[0].text = self.serverbox.get()
        self.ld.xpath('.//td[not(@class = "name")]')[1].text = self.levelbox.get()
        self.ld.xpath('.//td[not(@class = "name")]')[2].text = self.petbox.get()
        self.ld.xpath('.//td[not(@class = "name")]')[4].text = self.classbox.get()
        self.ld.xpath('.//td[not(@class = "name")]')[5].text = self.trofibox.get()
        self.ld.xpath('.//td[not(@class = "name")]')[6].text = self.petlevelbox.get()
        self.ld.xpath('.//td[not(@class = "name")]')[7].text = self.skillbox.get()
        self.ld.xpath('.//td[not(@class = "name")]')[3].text = self.guildbox.get()
        self.tree = self.ld.getroottree()
        self.lxmlsave()


def main():
    app = GarantGui()
    app.mainloop()

main()