import tkinter as tk
from tkinter import ttk
from codecs import open
from datetime import date
import os.path
import requests
import os
import sys, time

dictn = {'All Games': 'All Games', 'Bullet': 'bullet', 'Blitz': 'blitz', 'Rapid': 'rapid', 'Daily Chess': 'daily'}
dictb = {'Small, Only Wins': 0, 'Small, All Games': 1, 'Large, Only Wins': 2,'Large, All Games': 3}

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

exedir = os.getcwd()
updir = resource_path("")


def download_games():
    user=name_entry.get()
    if(opp_entry.get() == ""):
        where = os.path.join(loc_entry.get(), "%s's %s Archive %s" % (user, event.get(), date.today()))
    else:
        where = os.path.join(loc_entry.get(), "%s's vs %s %s Archive %s" % (user, opp_entry.get(), event.get(), date.today()))
    
    if not os.path.exists(where + ".pgn"):
        where += ".pgn"
        open(where, 'w').close()
    else:
        i=1
        while(os.path.exists(where + "(%s).pgn" % (i))):
            i+=1
        where = where + "(%d).pgn" % (i)
        open(where, 'w').close()
        
    for archive in get('https://api.chess.com/pub/player/%s/games/archives' % user)['archives']:
        aa(archive, where)

def mob():
    user=name_entry.get()
    obwp = os.path.join(updir, "White%s" % (user))
    obbp = os.path.join(updir, "Black%s" % (user))
    if (loc_entry.get() == ""):
        finalfile = os.path.join(exedir, "%s" % (user))
    else:
        finalfile = os.path.join(loc_entry.get(), "%s" % (user))
        
    if not os.path.exists(obwp + ".pgn"):
        obwp += ".pgn"
        open(obwp, 'w').close()
    else:
        i=1
        while(os.path.exists(obwp + "(%s).pgn" % (i))):
            i+=1
        obwp = obwp + "(%d).pgn" % (i)
        open(obwp, 'w').close()

    if not os.path.exists(obbp + ".pgn"):
        obbp += ".pgn"
        open(obbp, 'w').close()
    else:
        i=1
        while(os.path.exists(obwp + "(%s).pgn" % (i))):
            i+=1
        obbp = obbp + "(%d).pgn" % (i)
        open(obbp, 'w').close()
        
        
    for archive in get('https://api.chess.com/pub/player/%s/games/archives' % user)['archives']:
        obw(archive, obwp)
        obb(archive, obbp)
    try:
        
        os.chdir(updir)
        
        
        os.system("pgn-extract -s -C -N -V -tstartpos.txt -owclean.pgn %s" % (obwp))
        os.system("pgn-extract -s -C -N -V -tstartpos.txt -obclean.pgn %s" % (obbp))

        if (dictb[bo.get()] == 0 or dictb[bo.get()] == 1):
            os.system("polyglot make-book -only-white -pgn wclean.pgn -bin w1.bin -max-ply 32 -min-game 25")
            os.system("polyglot make-book -only-white -pgn wclean.pgn -bin w2.bin -max-ply 60 -min-game 5")
            os.system("polyglot make-book -only-black -pgn bclean.pgn -bin b1.bin -max-ply 32 -min-game 25")
            os.system("polyglot make-book -only-black -pgn bclean.pgn -bin b2.bin -max-ply 60 -min-game 5")
        else:
            os.system("polyglot make-book -only-white -pgn wclean.pgn -bin w1.bin")
            os.system("polyglot make-book -only-white -pgn wclean.pgn -bin w2.bin")
            os.system("polyglot make-book -only-black -pgn bclean.pgn -bin b1.bin")
            os.system("polyglot make-book -only-black -pgn bclean.pgn -bin b2.bin")
            
            
        os.system("polyglot merge-book -in1 w1.bin -in2 w2.bin -out w12.bin")
        os.system("polyglot merge-book -in1 b1.bin -in2 b2.bin -out b12.bin")
        
        os.system("polyglot merge-book -in1 w12.bin -in2 b12.bin -out %s.bin" % (finalfile))

        os.remove(obwp)
        os.remove("wclean.pgn")
        os.remove("w1.bin")
        os.remove("w2.bin")
        os.remove("w12.bin")

        os.remove(obbp)
        os.remove("bclean.pgn")
        os.remove("b1.bin")
        os.remove("b2.bin")
        os.remove("b12.bin")
        os.chdir(exedir)
    except:
        pass

def aa(url, where):
    games = get(url)['games']
    with open(where, 'a+', encoding='utf-8') as output:
        for game in games:
            try:
                if (game['rules'] == 'chess'):
                    if (opp_entry.get() == ""):
                        if (event.get() == "All Games"):
                            print(game['pgn'], file=output)
                            print('', file=output)
                        else:
                            if(dictn[event.get()] == game['time_class']):
                                print(game['pgn'], file=output)
                                print('', file=output)
                    else:
                        if (game['white']['username'] == opp_entry.get() or game['black']['username'] == opp_entry.get()):
                            if (event.get() == "All Games"):
                                print(game['pgn'], file=output)
                                print('', file=output)
                            else:
                                if(dictn[event.get()] == game['time_class']):
                                    print(game['pgn'], file=output)
                                    print('', file=output)
                    
                    
            except:
                pass

def obw(url, where):
    user = name_entry.get()
    games = get(url)['games']
    with open(where, 'a+', encoding='utf-8') as output:
        for game in games:
            try:
                if (game['rules'] == 'chess'):
                    if (game['white']['username'] == user):
                        if (dictb[bo.get()] == 0 or dictb[bo.get()] == 2):
                            if (game['white']['result'] == 'win'):
                                print(game['pgn'], file=output)
                                print('', file=output)
                        else:
                            print(game['pgn'], file=output)
                            print('', file=output)
            except:
                pass
def obb(url, where):
    user = name_entry.get()
    games = get(url)['games']
    with open(where, 'a+', encoding='utf-8') as output:
        for game in games:
            try:
                if (game['rules'] == 'chess'):
                    if (game['black']['username'] == user):
                        if (dictb[bo.get()] == 0 or dictb[bo.get()] == 2):
                            if (game['black']['result'] == 'win'):
                                print(game['pgn'], file=output)
                                print('', file=output)
                        else:
                            print(game['pgn'], file=output)
                            print('', file=output)
            except:
                pass


def get(url):
    return requests.get(url).json()



window = tk.Tk()
window.title("Chess.com Game Downloader")
frame_a = tk.Frame(padx=20, pady=10)

name = tk.Label(master=frame_a, text="Account Name", padx=10)
name_entry = tk.Entry(master=frame_a)

name.pack(side=tk.LEFT)
name_entry.pack(side=tk.LEFT)

frame_b = tk.Frame(padx=20, pady=10)

opp = tk.Label(master=frame_b, text="Opponent's Name", padx=10)
opp_entry = tk.Entry(master=frame_b)

opp.pack(side=tk.LEFT)
opp_entry.pack(side=tk.LEFT)


frame_c = tk.Frame(padx=20, pady=10)

location = tk.Label(master=frame_c, text="File Destination", padx=10)
loc_entry = tk.Entry(master=frame_c)

location.pack(side=tk.LEFT)
loc_entry.pack(side=tk.LEFT)


frame_d = tk.Frame(padx=20, pady=10)

tr = tk.Label(master=frame_d, text="Time Rules :", padx=10)
event = ttk.Combobox(master=frame_d, state="readonly", values = ['All Games', 'Bullet', 'Blitz', 'Rapid', 'Daily Chess'])
event.current(0)

tr.pack(side=tk.LEFT)
event.pack(side=tk.LEFT)

frame_e = tk.Frame(padx=20, pady=10)

bot = tk.Label(master=frame_e, text="Book Options :", padx=10)
bo = ttk.Combobox(master=frame_e, state="readonly", values = ['Small, Only Wins', 'Small, All Games', 'Large, Only Wins','Large, All Games'])
bo.current(0)

bot.pack(side=tk.LEFT)
bo.pack(side=tk.LEFT)

frame_ob = tk.Frame(padx=20, pady=10)
ob = tk.Button(master=frame_ob, text="Make Opening Book", command=mob)
ob.pack()

frame_end = tk.Frame(padx=20, pady=10)

button = tk.Button(master=frame_end, text="Download Games", command=download_games)
button.pack()



frame_a.pack()
frame_b.pack()
frame_c.pack()
frame_d.pack()
frame_e.pack()
frame_ob.pack()
frame_end.pack()

window.mainloop()
