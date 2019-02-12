#User interface 
print("== MUSIC QUIZ ==")
#Importing libraries
import sqlite3#SQL
#Creating databases
db = sqlite3.connect('users.db')
c = db.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)''')#Users database
c.execute('''CREATE TABLE IF NOT EXISTS leaderboard(username TEXT, score INTEGER)''')#Leaderboard
c.execute('''CREATE TABLE IF NOT EXISTS songs(listno TEXT, artist TEXT, song TEXT)''')#Songs database
import urllib.request
import csv
#Opening song file
try: f = open('songlist.csv','r')
except FileNotFoundError:#If file is not found import from github 
    import urllib.request
    try:
        urllib.request.urlretrieve('https://raw.githubusercontent.com/SaabirS/Music-Quiz/master/songlist.csv','songlist.csv')
    except:                                 
        print("\nPlease allow connections to https://github.com/SaabirS/Music-Quiz/blob/master/songlist.csv to download files")
        raise SystemExit
    else: f = open('songlist.csv','r')#Opening and reading the song file
    
songlist = csv.reader(f)
c.execute("DELETE FROM songs")
for row in songlist:
    c.execute("INSERT INTO songs VALUES (?,?,?)",row)
f.close()#Close file
db.commit()
#Functions-----------------------------------------------------------------------------------------------
#Creating a function for the main menu

def signin_options():
    signin = ''
    while signin not in ('1','2','3'):
        signin = input("\nWould you like to\n\t1. Login or \n\t2. Register\n\t3. View Leaderboard\n:")#putting signin options on next lines, more user-friendly.
    if signin == '1': login()#calling login function
    elif signin == '2': register()#calling registration function
    else: leaderboard()
#Creating a function for the login system
def login():
    global username
    username = input("\nUsername: ").strip().lower()#Input sanitisation
    password = input("Password: ").strip()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?",(username,password))
    if c.fetchone():
        game()
    else:
        print("INCORRECT DETAILS")
        login()
#Creating a function for the user to register
def register():
    global username
    username = input("\nCreate a username: ").strip().lower()#Sanitising input
    c.execute("SELECT * FROM users WHERE username = ?",(username,))
    if c.fetchone():
        print("Username exists! Try again")#Calling function again if there is an inavlid username
        register()
    password = input("Create a strong password: ").strip()
    c.execute("INSERT INTO users VALUES (?,?)",(username,password))
    db.commit()
#Creating a function for the leaderboard
def leaderboard():
    c.execute("SELECT * FROM leaderboard ORDER BY score DESC")
    leaderboard = c.fetchall()
    print("\n== LEADERBOARD ==")
    try: leaderboard[0][0]
    except IndexError: print("\nNO SCORES FOUND")
    else:
        for i in range(len(leaderboard)):
            username = leaderboard[i][0]
            score = leaderboard[i][1]
            print("Username: ",username,"\tScore: ",score)
    signin_options()
#Importing libraries
import random
import string
playedsongs = []
score = 0
#Creating a function for the game
def game():
    global score
    if len(playedsongs) == 200:
        print("\nAll songs played")
        raise SystemExit

    songno = random.randint(1,200)#Extracting a random song from the song file
    while songno in playedsongs:
        songno = random.randint(1,200)
        playedsongs.append(songno)
        
    c.execute("SELECT artist,song FROM songs WHERE listno=?",(str(songno),))#Fetching song and artist from songs database
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
#Creating a function to end the game
def gameover():
    global username
    c.execute("SELECT * FROM leaderboard WHERE username = ?",(username,))

    try: tempname,tempscore = c.fetchone()
    except TypeError: insert = True
    else:
        if tempscore<score: insert=True
        else: insert=False
                                
    if insert==True:
        c.execute("REPLACE INTO leaderboard (username,score) VALUES (?,?)",(username,score))#Placing scores into leaderboard
        db.commit()
    if score>0:
        print("\n\tCongrats, your score was:",score)
    else:
        print("\n\tUnlucky, your score was:",score)
    raise SystemExit

signin_options()#Calling function for the main menu
db.close()
    
                             
