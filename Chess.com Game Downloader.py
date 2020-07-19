from codecs import open
from datetime import date
import os.path
import requests

def main():
    user = input("Player's Name:")
    opp_entry = input("Opponent's Name(Optional):")
    
    
    if(opp_entry == ""):
        where = os.path.join(input("Directory(Empty for current):"), "%s's Archive %s" % (user, date.today()))
    else:
        where = os.path.join(input("Directory(Empty for current):"), "%s's vs %s Archive %s" % (user, opp_entry, date.today()))
    
    if not os.path.exists(where + ".pgn"):
        where += ".pgn"
        open(where, 'w').close()
    else:
        print("File already exists. Changing name")
        i=1
        while(os.path.exists(where + "(%s).pgn" % (i))):
            i+=1
        where = where + "(%d).pgn" % (i)
        open(where, 'w').close()
        
    print("Downloading %s's games to %s:" % (user, where))
    for archive in get('https://api.chess.com/pub/player/%s/games/archives' % user)['archives']:
        aa(archive, where, opp_entry)
    

def aa(url, where, opp):
    games = get(url)['games']
    with open(where, 'a+', encoding='utf-8') as output:
        for game in games:
            if (game['rules'] == 'chess'):
                if (opp == ""):
                    try:
                        print(game['pgn'], file=output)
                        print('', file=output)
                    except:
                        pass
                else:
                    if (game['white']['username'] == opp or game['black']['username'] == opp):
                        try:
                            print(game['pgn'], file=output)
                            print('', file=output)
                        except:
                            pass

def get(url):
    return requests.get(url).json()

main()
