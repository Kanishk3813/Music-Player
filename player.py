import os
from tkinter import *
from tkinter import filedialog
from pygame import mixer
import mysql.connector  


db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="root",
    database="MusicPlayer"
)

cursor = db.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS music_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_path VARCHAR(255) NOT NULL,
    title VARCHAR(255),
    artist VARCHAR(255),
    album VARCHAR(255)
)
"""
cursor.execute(create_table_query)
db.commit()


root = Tk()
root.title("Python Music Player")
root.geometry("485x700+290+10")
root.configure(background='#333333')
root.resizable(False, False)
mixer.init()


def AddMusic():
    file_paths = filedialog.askopenfilenames(
        filetypes=[("MP3 files", "*.mp3")]
    )
    if file_paths:
        for file_path in file_paths:
           
            s=file_path.replace("C:/Users/kanis/OneDrive/Desktop/mp3 player/Music/","")
         
            Playlist.insert(END, file_path)
        
            insert_music_info(file_path, s, "Unknown", "Unknown")


def insert_music_info(file_path, title, artist, album):
    sql = "INSERT INTO music_info (file_path, title, artist, album) VALUES (%s, %s, %s, %s)"
    val = (file_path, title, artist, album)
    cursor.execute(sql, val)
    db.commit()


def get_music_info():
    cursor.execute("SELECT file_path, title, artist, album FROM music_info")
    music_info = cursor.fetchall()
    return music_info

def PlayMusic():
    Music_Name = Playlist.get(ACTIVE)
    print(Music_Name[0:-4])
    mixer.music.load(Playlist.get(ACTIVE))
    mixer.music.play()


def ToggleVolume():
    global volume
    if volume > 0.0:
        volume = 0.0
        volume_icon_label.config(text="🔇")
    else:
        volume = 0.5 
        volume_icon_label.config(text="🔊")
    mixer.music.set_volume(volume)


paused = False
paused_position = 0  

def TogglePause():
    global paused
    global paused_position
    if not paused:
        mixer.music.pause()
        paused_position = mixer.music.get_pos()  
        paused = True
    else:
        mixer.music.unpause()
        mixer.music.set_pos(paused_position / 1000)  
        paused = False


volume = 0.5
mixer.music.set_volume(volume)


lower_frame = Frame(root, bg="#FFFFFF", width=485, height=180)
lower_frame.place(x=0, y=400)

image_icon = PhotoImage(file="logo.png")
root.iconphoto(False, image_icon)

frameCnt = 30
frames = [PhotoImage(file='aa1.gif', format='gif -index %i' % i) for i in range(frameCnt)]

def update(ind):
    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    label.configure(image=frame)
    root.after(40, update, ind)

label = Label(root)
label.place(x=0, y=0)
root.after(0, update, 0)


ButtonPlay = PhotoImage(file="play1.png")
Button(root, image=ButtonPlay, bg="#FFFFFF", bd=0, height=60, width=60,
       command=PlayMusic).place(x=215, y=487)

ButtonStop = PhotoImage(file="stop1.png")
Button(root, image=ButtonStop, bg="#FFFFFF", bd=0, height=60, width=60,
       command=mixer.music.stop).place(x=130, y=487)

Buttonvolume = PhotoImage(file="volume.png")
Button(root, image=Buttonvolume, bg="#FFFFFF", bd=0, height=60, width=60,
       command=ToggleVolume).place(x=20, y=487)

ButtonPause = PhotoImage(file="pause1.png")
Button(root, image=ButtonPause, bg="#FFFFFF", bd=0, height=60, width=60,
       command=TogglePause).place(x=300, y=487)


Menu = PhotoImage(file="menu.png")
Label(root, image=Menu).place(x=0, y=580, width=485, height=120)

Frame_Music = Frame(root, bd=2, relief=RIDGE)
Frame_Music.place(x=0, y=585, width=485, height=100)

Button(root, text="Browse Music", width=59, height=1, font=("calibri",
      12, "bold"), fg="Black", bg="#FFFFFF", command=AddMusic).place(x=0, y=550)

Scroll = Scrollbar(Frame_Music)
Playlist = Listbox(Frame_Music, width=100, font=("Times new roman", 10), bg="#333333", fg="grey", selectbackground="lightblue", cursor="hand2", bd=0, yscrollcommand=Scroll.set)
Scroll.config(command=Playlist.yview)
Scroll.pack(side=RIGHT, fill=Y)
Playlist.pack(side=RIGHT, fill=BOTH)


volume_label = Label(root, text="", font=("calibri", 10), bg="#333333", fg="white")
volume_label.place(x=10, y=560)

volume_icon_label = Label(root, text="🔊", font=("calibri", 20), bg="#333333", fg="white")
volume_icon_label.place(x=405, y=500)

def on_closing():
    db.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
