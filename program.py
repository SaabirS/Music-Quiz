print("== MUSIC QUIZ ==")

import sqlite3

db = sqlite3.connect('users.db')
c = db.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)
''')
c.execute('''
    CREATE TABLE IF NOT EXISTS leaderboard(username TEXT, score INTEGER)
''')
c.execute('''
    CREATE TABLE IF NOT EXISTS songs(listno TEXT, artist TEXT, song TEXT)
''')

import csv
try: f = open('songlist.csv','r')
except FileNotFoundError:
    import urllib.request  #CHANGE LINK ON BELOW LINE
    try: urllib.request.urlretrieve('https://raw.githubusercontent.com/MZakariyya9/SaabirMQ/master/songlist.csv','songlist.csv')
    except:                                 #CHANGE BELOW
        print("\nPlease allow connections to DOMAIN NAME GOES HERE to download files")
        raise SystemExit
    else: f = open('songlist.csv','r')
    
songlist = csv.reader(f)
c.execute("DELETE FROM songs")
for row in songlist:
    c.execute("INSERT INTO songs VALUES (?,?,?)",row)
f.close()
db.commit()

def signin_options():
    signin = ''
    while signin not in ('1','2','3'):
        signin = input("\nWould you like to\n\t1. Login or \n\t2. Register\n\t3. View Leaderboard\n:")
    if signin == '1': login()
    elif signin == '2': register()
    else: leaderboard()

def login():
    global username
    username = input("\nUsername: ").strip().lower()
    password = input("Password: ").strip()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?",
                       (username,password))
    if c.fetchone():
        game()
    else:
        print("INCORRECT DETAILS")
        login()

def register():
    global username
    username = input("\nCreate a username: ").strip().lower()
    c.execute("SELECT * FROM users WHERE username = ?",(username,))
    if c.fetchone():
        print("Username exists! Try again")
        register()
    password = input("Create a strong password: ").strip()
    c.execute("INSERT INTO users VALUES (?,?)",(username,password))
    db.commit()

def leaderboard():
    c.execute("SELECT * FROM leaderboard ORDER BY score DESC")
    try: leaderboard = c.fetchall()
    except IndexError: print("\nNO SCORES FOUND")
    print("\n== LEADERBOARD ==")
    for i in range(0,5):
        username = leaderboard[i][0]
        score = leaderboard[i][1]
        print("Username: ",username,"\tScore: ",score)
    signin_options()

import random
import string
playedsongs = []
score = 0
def game():
    global score
    if len(playedsongs) == 200:
        print("\nAll songs played")
        raise SystemExit

    songno = random.randint(1,200)
    while songno in playedsongs:
        songno = random.randint(1,200)
        playedsongs.append(songno)
        
    c.execute("SELECT artist,song FROM songs WHERE listno=?",(str(songno),))
    artist,song = c.fetchone()
    
    songname = song.split()
    song_clue = []
    
    for words in songname:
        letters = list(words)
        word_clue = []
        counter = 0
        for l in letters:
            if counter == 0: counter += 1
            elif l is string.punctuation: pass
            else: l = "_"
            word_clue.append(l)   
        song_clue.append(word_clue)
        
    clue = []
    for words in song_clue:
        for l in words:
            clue.append(l)
        clue.append("\t")
    clue = " ".join(clue)
    
    print("\n\tArtist: ",artist)
    print("\tSong Clue: ",clue)

    lives = 2
    while lives != 0:
        entry = input("\n\tName the Song: ")
        if entry.upper() == song.upper():
            print("\tCORRECT")
            if lives == 2:
                score += 3
                game()
            else:
                score += 1
                game()
        else:
            print("\tINCORRECT")
            lives -= 1
    gameover()

def gameover():
    global username
    c.execute("SELECT * FROM leaderboard WHERE username = ?",(username,))

    try: tempname,tempscore = c.fetchone()
    except TypeError: insert = True
    else:
        if tempscore<score: insert=True
        else: insert=False
                                
    if insert==True:
        c.execute("REPLACE INTO leaderboard (username,score) VALUES (?,?)",(username,score))
        db.commit()
    print("\n\tCongrats, your score was:",score)
    raise SystemExit

signin_options()
db.close()
    
                             
