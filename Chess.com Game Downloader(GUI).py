import tkinter as tk
from tkinter import ttk
from codecs import open
from datetime import date
import os.path
import requests

dictn = {'All Games': 'All Games', 'Bullet': 'bullet', 'Blitz': 'blitz', 'Rapid': 'rapid', 'Daily Chess': 'daily'}

def download_games():
    user=name_entry.get()
    where = os.path.join(loc_entry.get(), "%s's %s Archive %s" % (user, event.get(),date.today()))
    
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
    

def aa(url, where):
    games = get(url)['games']
    with open(where, 'a+', encoding='utf-8') as output:
        for game in games:
            try:
                if (game['rules'] == 'chess'):
                    if (event.get() == "All Games"):
                        print(game['pgn'], file=output)
                        print('', file=output)
                    else:
                        if(dictn[event.get()] == game['time_class']):
                            print(game['pgn'], file=output)
                            print('', file=output)
                    
            except:
                pass

def get(url):
    return requests.get(url).json()



window = tk.Tk()
window.title("Chess.com Game Downloader")
frame_a = tk.Frame(padx=20, pady=10)

name = tk.Label(master=frame_a, text="Account Name")
name_entry = tk.Entry(master=frame_a)

name.pack(side=tk.LEFT)
name_entry.pack(side=tk.LEFT)




frame_b = tk.Frame(padx=20, pady=10)

location = tk.Label(master=frame_b, text="File Destination")
loc_entry = tk.Entry(master=frame_b)

location.pack(side=tk.LEFT)
loc_entry.pack(side=tk.LEFT)


frame_c = tk.Frame(padx=20, pady=10)

event = ttk.Combobox(master=frame_c, state="readonly", values = ['All Games', 'Bullet', 'Blitz', 'Rapid', 'Daily Chess'])
event.current(0)
event.pack(side=tk.LEFT)




frame_end = tk.Frame(padx=20, pady=10)

button = tk.Button(master=frame_end, text="Download Games", command=download_games)
button.pack()


frame_a.pack()
frame_b.pack()
frame_c.pack()
frame_end.pack()

window.mainloop()
