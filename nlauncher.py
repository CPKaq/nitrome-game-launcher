import os
import json
from tkinter import *
from PIL import Image, ImageTk

def main():
    global selectGame
    global img_png
    selectGame = {}

    #通过cmd启动游戏
    def startGame():
        os.system('start /B flash {}'.format(selectGame['url']))

    #选择游戏
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

    #读取游戏列表
    with open('json/games.json', 'r') as f:
        games = json.load(f)

    #主窗口
    win = Tk()
    win.title("Nitrome Flash Games Launcher: Mugen")
    win.geometry("600x400")
    win.iconphoto(False, PhotoImage(file="img/favicon.gif"))

    #左栏
    frameGames = Frame()
    frameGames.pack(fill=Y, side=LEFT)

    #游戏列表
    listboxGame = Listbox(frameGames, width=24)
    listboxGame.bind('<<ListboxSelect>>', setGame)
    listboxGame.pack(fill=BOTH, side=LEFT)

    for item in games:
        listboxGame.insert("end", item['name'])

    scrollGame = Scrollbar(frameGames)
    scrollGame.pack(side=RIGHT, fill=Y)
    scrollGame.config(command=listboxGame.yview)
    listboxGame.config(yscrollcommand=scrollGame.set)

    #右栏
    frameInfo = Frame()
    frameInfo.pack(fill=BOTH, side=RIGHT, expand=TRUE)

    #页面标题
    labelTitle = Label(frameInfo, text="Launcher")
    labelTitle.pack(fill=X, side=TOP)

    #游戏图标
    labelIcon = Label(frameInfo)
    labelIcon.pack(fill=X, side=TOP)

    #开始按钮
    btnStart = Button(frameInfo, text="启动", padx=20, command=startGame)
    btnStart.pack(side=BOTTOM)

    win.mainloop()

if __name__ == '__main__':
    main()