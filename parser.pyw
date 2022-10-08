from tkinter import * 
from tkinter import ttk
from tkinter.ttk import Combobox
from tkinter import filedialog
import json 

def input_file ():
    global json_file
    json_file = filedialog.askopenfilename(filetypes=[('JSON', '*.json')])
    if json_file != "":
        statusbar.configure (text=json_file, bg="#33691E", fg="#C5E1A5")
        with open (json_file) as json_data:
            global data
            data = json.load (json_data)
        for current_country in data["countries"]:
            country['values'] += (current_country["name"],)
        mk_btn.configure (state="normal")

def write_file ():
    statusbar.configure (text="В процессе...", bg="#311B92", fg="#B39DDB")
    
    if genre_split_state.get ():
        workdir = filedialog.askdirectory()
        if workdir == "":
            statusbar.configure (text="ПАПКА ДЛЯ СОХРАНЕНИЯ НЕ ВЫБРАНА", bg="#B71C1C", fg="#EF9A9A")
            return
    else:
        workfile = filedialog.asksaveasfilename(filetypes=[('M3U', '*.m3u')], defaultextension=".m3u")
        if workfile == "":
            statusbar.configure (text="ФАЙЛ ДЛЯ СОХРАНЕНИЯ НЕ ВЫБРАН", bg="#B71C1C", fg="#EF9A9A")
            return

    if genre_split_state.get ():
        for current_genre in data["genres"]:
            with open(workdir + f'\{current_genre["name"]}.m3u', 'a') as current_file:
                current_file.write ('#EXTM3U\n')
    else:
        with open(workfile, 'a') as current_file:
            current_file.write ('#EXTM3U\n')

    for current_channel in data["stations"]:
        
        i = 0
        while (not int(data["countries"][i]["id"]) == current_channel["country_id"]):
            i += 1
        current_country = data["countries"][i]["name"]
        
        if country.get () != "Все страны" and current_country != country.get ():
            continue
        
        if fix_stream_state.get ():
            current_stream = current_channel["stream"].replace ("http://stream.pcradio.ru:8000/", fix_stream_mode.get())
        else:
            current_stream = current_channel["stream"]
        current_channel_genres = current_channel["genres_ids"]

        if hq_logo_state.get ():
            current_logo = current_channel["logo"].replace ("thumbnail90", "thumbnail350").replace (".jpeg", "-350.jpeg").replace (".png", "-350.png")
        else:
            current_logo = current_channel["logo"]

        for current_genre_id in current_channel_genres:
            i = 0
            while (not int(data["genres"][i]["id"]) == current_genre_id):
                i += 1
            current_genre = data["genres"][i]["name"]
            if genre_split_state.get ():
                current_genre_file = f'{workdir}\{current_genre}.m3u'
            else:
                current_genre_file = workfile
            if add_metadata_state.get ():
                metadata = f' tvg-logo=\"{current_logo}\" group-title=\"{current_genre}\" radio=\"true\"'
            else:
                metadata = ''
            with open(current_genre_file, 'a') as current_file:
                current_file.write (f'#EXTINF:-1{metadata}, {current_channel["name"]}\n')
            with open(current_genre_file, 'a') as current_file:
                current_file.write (f'{current_stream}-{quality.get()}\n')
            if not (genre_split_state.get () or add_metadata_state.get ()):
                break

    statusbar.configure (text="Готово!", background="#BF360C", foreground="#FFAB91")

root = Tk ()
root.title ("PCRADIO JSON TO M3U CONVERTER")
root.geometry ('240x400')
root.resizable (width=False, height=False)
root.attributes ('-alpha', 0.9)
root.config (bg="#222")

choose_btn = Button (text='ВЫБРАТЬ ФАЙЛ', bg="#222", fg="#AAA", activebackground="#222", activeforeground="#CCC", command=input_file)
choose_btn.pack (padx=10, pady=10)

settings_title = Label (text="ОСНОВНЫЕ НАСТРОЙКИ", bg="#006064", fg="#80DEEA")
settings_title.pack (fill=X)

quality = StringVar ()
quality.set ('med')
low = Radiobutton (text='ЭКОНОМ (28K, AAC)', bg="#222", fg="#AAA", activebackground="#222", activeforeground="#CCC", selectcolor="#222", value='low', variable=quality)
med = Radiobutton (text='СТАНДАРТ (42K, AAC)', bg="#222", fg="#AAA", activebackground="#222", activeforeground="#CCC", selectcolor="#222", value='med', variable=quality)
hi = Radiobutton (text='ПРЕМИУМ (64K, AAC)', bg="#222", fg="#AAA", activebackground="#222", activeforeground="#CCC", selectcolor="#222", value='hi', variable=quality)
low.pack ()
med.pack ()
hi.pack ()

country = Combobox(values=['Все страны'], state="readonly")
country.current (0)
country.pack ()

Label(bg="#222").pack(pady=1)

advanced_settings_title = Label (text="ДОПОЛНИТ. НАСТРОЙКИ", bg="#006064", fg="#80DEEA")
advanced_settings_title.pack (fill=X)

fix_stream_state = BooleanVar ()
fix_stream_state.set (True)
fix_stream = Checkbutton(text='ИСПРАВИТЬ ПОТОК', bg="#222", fg="#AAA", activebackground="#222", activeforeground="#CCC", selectcolor="#222", var=fix_stream_state)
fix_stream.pack ()

fix_stream_mode = Combobox(values=['http://str.pcradio.ru/', 'http://str3.pcradio.ru/'])
fix_stream_mode.current (0)
fix_stream_mode.pack ()

genre_split_state = BooleanVar ()
genre_split_state.set (False)
genre_split = Checkbutton(text='РАЗБИТЬ ПО ЖАНРАМ', bg="#222", fg="#AAA", activebackground="#222", activeforeground="#CCC", selectcolor="#222", var=genre_split_state)
genre_split.pack ()

add_metadata_state = BooleanVar ()
add_metadata_state.set (True)
add_metadata = Checkbutton(text='ДОБАВИТЬ МЕТАДАННЫЕ', bg="#222", fg="#AAA", activebackground="#222", activeforeground="#CCC", selectcolor="#222", var=add_metadata_state)
add_metadata.pack ()

hq_logo_state = BooleanVar ()
hq_logo_state.set (True)
hq_logo = Checkbutton(text='КАЧЕСТВЕННЫЕ ЛОГОТИПЫ', bg="#222", fg="#AAA", activebackground="#222", activeforeground="#CCC", selectcolor="#222", var=hq_logo_state)
hq_logo.pack ()

mk_btn = Button (text='ЗАПИСАТЬ В ФАЙЛ', bg="#222", fg="#AAA", activebackground="#222", activeforeground="#CCC", command=write_file, state="disabled")
mk_btn.pack (padx=10, pady=10)

statusbar = Label (text="ФАЙЛ НЕ ВЫБРАН", bg="#880E4F", fg="#F48FB1")
statusbar.pack (side=BOTTOM, fill=X)

root.mainloop ()