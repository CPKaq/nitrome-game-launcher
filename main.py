import os
import io
import json
import requests
import threading
import webbrowser
from tkinter import *
from tkinter import messagebox
import tkinter.font as tkfont
from PIL import Image, ImageTk

WINDOW_TITLE = "Nitrome Flash Games Launcher: Candytown"
START_BUTTON_TEXT = "▶"
INIT_TEXT = "Click a game tag to start!"
ABOUT_TEXT = """Programmed by CPK\nSpecial thanks to Nitrome Bar"""
THUMBNAIL_LOADING_TEXT = "Loading thumbnail..."
THUMBNAIL_FAIL_TEXT = "Connection failed"

GITHUB_URL = r'https://github.com/CPKaq/nitrome-game-launcher'
THUMBNAIL_PREFIX = r'https://cdn.nitrome.com/images/thumbnails/'

EMPTY_IMAGE = Image.new('RGBA', (0, 0), (255, 255, 255, 0))

# Global variable for game icon
_img_png = None


def thrd(func, *args):
    t = threading.Thread(target=func, args=args)
    t.setDaemon(True)
    t.start()
    # t.join()


class GameInfo:
    def __init__(self):
        self.game = dict()

    def set_game(self, arg: dict):
        self.game = arg

    def get_game(self):
        return self.game

    def get_param(self, key: str):
        return self.game.get(key)

    def is_empty(self):
        return self.game == {}


class GameList:
    def __init__(self):
        self.game_list = []

    def load(self, json_path):
        with open(json_path, 'r') as f:
            self.game_list = json.load(f)

    def list(self):
        return self.game_list

    def get_info(self, game_name):
        for game in self.game_list:
            if game_name == game['name']:
                return GameInfo().set_game(game)
        return None


# Run Flash Player in cmd
def start_game(game: GameInfo):
    if game.is_empty():
        return
    os.system('start /B flash {}'.format(game.get_param('url')))


def get_thumbnail(url: str, label_icon: Label, label_icon_alt: Label):
    global _img_png
    label_icon.config(image=ImageTk.PhotoImage(EMPTY_IMAGE))
    label_icon_alt.config(text=THUMBNAIL_LOADING_TEXT)
    try:
        img_open = requests.get(url).content
        data_stream = io.BytesIO(img_open)
        pil_image = Image.open(data_stream)
        _img_png = ImageTk.PhotoImage(pil_image)
    except Exception as e:
        label_icon.config(image=ImageTk.PhotoImage(EMPTY_IMAGE))
        label_icon_alt.config(text=THUMBNAIL_FAIL_TEXT)
        raise e
    else:
        label_icon.config(image=_img_png)
        label_icon_alt.config(text='')


# Select game
def set_game(clicked_game, game_list, selected_game, label_title, label_icon, lable_icon_alt):
    for game in game_list.list():
        if game['name'] == clicked_game:
            selected_game.set_game(game)
            break
    label_title.config(text=selected_game.get_param('name'))
    # img_open = Image.open('img/ico/{}'.format(selected_game.get_param('img')))
    # global _img_png
    # _img_png = ImageTk.PhotoImage(img_open)
    # img_open = requests.get(THUMBNAIL_PREFIX + selected_game.get_param('img'), verify=False).content
    # get_thumbnail(THUMBNAIL_PREFIX + selected_game.get_param('img'))
    thrd(get_thumbnail, THUMBNAIL_PREFIX + selected_game.get_param('img'), label_icon, lable_icon_alt)
    # label_icon.config(image=_img_png)


def main():
    selected_game = GameInfo()

    game_list = GameList()
    game_list.load('json/games.json')

    # Main Window
    win = Tk()
    win.title(WINDOW_TITLE)
    win.geometry("600x400")
    win.iconphoto(False, PhotoImage(file="img/favicon.gif"))

    font_big = tkfont.Font(size=20)
    font_title = tkfont.Font(size=20, family='Arial', weight='bold')

    # - Menubar
    menubar = Menu(win)
    menu_about = Menu(menubar, tearoff=0)
    menu_about.add_command(label='About...',
                           command=lambda: messagebox.showinfo(title='About', message=ABOUT_TEXT))
    menu_about.add_command(label='View on GitHub...',
                           command=lambda: webbrowser.open(GITHUB_URL))

    menubar.add_cascade(label="About", menu=menu_about)
    win.config(menu=menubar)

    # - Left Column
    frame_games = Frame()
    frame_games.pack(fill=Y, side=LEFT)

    # - - Game listbox
    listbox_game = Listbox(frame_games, width=24)
    listbox_game.bind('<<ListboxSelect>>', lambda event: set_game(
        listbox_game.get(listbox_game.curselection()),
        game_list, selected_game, label_title, label_icon, label_icon_alt))
    listbox_game.pack(fill=BOTH, side=LEFT)

    for item in game_list.list():
        listbox_game.insert("end", item['name'])

    scroll_game = Scrollbar(frame_games)
    scroll_game.pack(side=RIGHT, fill=Y)
    scroll_game.config(command=listbox_game.yview)
    listbox_game.config(yscrollcommand=scroll_game.set)

    # - Right Column
    frame_info = Frame()
    frame_info.pack(fill=BOTH, side=RIGHT, expand=TRUE, padx=20, pady=20)

    # - - Game Title
    label_title = Label(frame_info, text=" ", font=font_title)
    label_title.pack(fill=X, side=TOP)

    # - - Game Icon
    label_icon = Label(frame_info)
    label_icon_alt = Label(frame_info, text=INIT_TEXT)
    label_icon.pack(fill=X, side=TOP)
    label_icon_alt.pack(fill=X, side=TOP)

    # - - Start game button
    btn_start = Button(frame_info, text=START_BUTTON_TEXT, padx=80, pady=10, font=font_big, fg='green',
                       command=lambda: start_game(selected_game))
    btn_start.pack(side=BOTTOM)

    win.mainloop()


if __name__ == '__main__':
    main()
