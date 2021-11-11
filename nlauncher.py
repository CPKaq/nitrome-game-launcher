import os
import json
from tkinter import *
from PIL import Image, ImageTk

WINDOW_TITLE = "Nitrome Flash Games Launcher: Mugen"
START_BUTTON_TEXT = "启动"

def main():
    global selectGame
    global img_png
    selectGame = {}

    # Run flash in cmd
    def startGame():
        os.system('start /B flash {}'.format(selectGame['url']))

    # Select game
    def setGame(event):
        for game in games:
            if game['name'] == listboxGame.get(listboxGame.curselection()):
                global selectGame
                selectGame = game
                break
        labelTitle.config(text=selectGame['name'])
        img_open = Image.open('img/ico/{}'.format(selectGame['img']))
        global img_png
        img_png = ImageTk.PhotoImage(img_open)
        labelIcon.config(image=img_png)

    # Read game list json
    with open('json/games.json', 'r') as f:
        games = json.load(f)

    # Main Window
    win = Tk()
    win.title(WINDOW_TITLE)
    win.geometry("600x400")
    win.iconphoto(False, PhotoImage(file="img/favicon.gif"))

    ## Left Colomn
    frameGames = Frame()
    frameGames.pack(fill=Y, side=LEFT)

    ### Game listbox
    listboxGame = Listbox(frameGames, width=24)
    listboxGame.bind('<<ListboxSelect>>', setGame)
    listboxGame.pack(fill=BOTH, side=LEFT)

    for item in games:
        listboxGame.insert("end", item['name'])

    scrollGame = Scrollbar(frameGames)
    scrollGame.pack(side=RIGHT, fill=Y)
    scrollGame.config(command=listboxGame.yview)
    listboxGame.config(yscrollcommand=scrollGame.set)

    ## Right Colomn
    frameInfo = Frame()
    frameInfo.pack(fill=BOTH, side=RIGHT, expand=TRUE)

    ### Game Title
    labelTitle = Label(frameInfo, text="Launcher")
    labelTitle.pack(fill=X, side=TOP)

    ### Game Icon
    labelIcon = Label(frameInfo)
    labelIcon.pack(fill=X, side=TOP)

    ### Start game button
    btnStart = Button(frameInfo, text=START_BUTTON_TEXT, padx=20, command=startGame)
    btnStart.pack(side=BOTTOM)

    win.mainloop()

if __name__ == '__main__':
    main()