from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from pathlib import Path
import wget
import pyzipper
import locale
import json

if locale.getdefaultlocale()[0] == 'ru_RU':
    str_data_loaded = "Данные загружены"
    str_all_countries = "Все страны"
    str_downloading_error = "Ошибка скачивания"
    str_processing = "В процессе..."
    str_str_folder_not_selected = "ПАПКА ДЛЯ СОХРАНЕНИЯ НЕ ВЫБРАНА"
    str_file_not_selected = "ФАЙЛ ДЛЯ СОХРАНЕНИЯ НЕ ВЫБРАН"
    str_done = "Готово!"
    str_app_title = "PCRADIO JSON TO M3U CONVERTER"
    str_file_selection = "ВЫБОР ФАЙЛА"
    str_select_file = "ВЫБРАТЬ ФАЙЛ"
    str_file_downloading = "СКАЧИВАНИЕ ФАЙЛА"
    str_lang_ru = "РУССКИЙ"
    str_lang_en = "АНГЛИЙСКИЙ"
    str_download_file = "СКАЧАТЬ ФАЙЛ"
    str_quality = "КАЧЕСТВО"
    str_country = "СТРАНА"
    str_advanced_settings = "ДОПОЛНИТ. НАСТРОЙКИ"
    str_fix_stream = "ИСПРАВИТЬ ПОТОК"
    str_genre_split = "РАЗБИТЬ ПО ЖАНРАМ"
    str_add_metadata = "ДОБАВИТЬ МЕТАДАННЫЕ"
    str_quality_logo = "КАЧЕСТВЕННЫЕ ЛОГОТИПЫ"
    str_saving = "СОХРАНЕНИЕ"
    str_write_to_m3u = "ЗАПИСАТЬ В ФАЙЛ"
    str_file_not_selected = "ФАЙЛ НЕ ВЫБРАН"
    str_city = "ГОРОД"
    str_all_cities = "Все города"
else:
    str_data_loaded = "Data loaded"
    str_all_countries = "All countries"
    str_downloading_error = "Download error"
    str_processing = "In the process ..."
    str_str_folder_not_selected = "THE FOLDER TO SAVE IS NOT SELECTED"
    str_file_not_selected = "NO FILE TO SAVE SELECTED"
    str_done = "Done!"
    str_app_title = "PCRADIO JSON TO M3U CONVERTER"
    str_file_selection = "FILE SELECTION"
    str_select_file = "SELECT FILE"
    str_file_downloading = "FILE DOWNLOAD"
    str_lang_ru = "RUSSIAN"
    str_lang_en = "ENGLISH"
    str_download_file = "DOWNLOAD FILE"
    str_quality = "QUALITY"
    str_country = "COUNTRY"
    str_advanced_settings = "ADV. SETTINGS"
    str_fix_stream = "FIX THE STREAM"
    str_genre_split = "SPLIT BY GENRE"
    str_add_metadata = "ADD METADATA"
    str_quality_logo = "QUALITY LOGOS"
    str_saving = "SAVING"
    str_write_to_m3u = "WRITE TO FILE"
    str_file_not_selected = "FILE NOT SELECTED"
    str_city = "CITY"
    str_all_cities = "All cities"

def download_ziplist ():
    try:
        ziplist = wget.download(f'http://stream.pcradio.ru/list/list_{lang.get ()}/list_{lang.get ()}.zip')
    except:
        statusbar.configure (text=str_downloading_error, background="#B71C1C", foreground="#EF9A9A")
        return
    
    with pyzipper.AESZipFile(ziplist) as ziplist:
        ziplist.pwd = b'78951233215987'
        with ziplist.open(f'list_{lang.get ()}.json') as json_data:
            load_data (json_data)

def input_file ():
    global json_file
    json_file = filedialog.askopenfilename(filetypes=[('JSON', '*.json')])
    if json_file != '':
        with open (json_file) as json_data:
            load_data (json_data)

def load_data (json_data):
    global data
    data = json.load (json_data)
    country['values'] = [str_all_countries]
    country.current (0)
    for current_country in data['countries']:
        country['values'] += (current_country['name'],)
    
    statusbar.configure (text=str_data_loaded, background="#33691E", foreground="#C5E1A5")
    mk_btn.configure (state="normal")

def search_in_array (wheretolook, inputdata, sourcetype, typeweneed):
    i = 0
    while (data[wheretolook][i][sourcetype] != inputdata):
        i += 1
    return data[wheretolook][i][typeweneed]

def get_city_list (event):
    city['values'] = [str_all_cities]
    city.current (0)
    if country.get () != str_all_countries:
        for current_city in data['countries_cities'][search_in_array ('countries', country.get (), 'name', 'id')]:
            city['values'] += (search_in_array ('cities', current_city, 'id', 'name'),)

def write_file ():
    statusbar.configure (text=str_processing, background='#311B92', foreground="#B39DDB")
    
    if genre_split_state.get ():
        workdir = filedialog.askdirectory()
        if workdir == '':
            statusbar.configure (text=str_folder_not_selected, background='#B71C1C', foreground='#EF9A9A')
            return
    else:
        workfile = filedialog.asksaveasfilename(filetypes=[('M3U', '*.m3u')], defaultextension='.m3u')
        if workfile == '':
            statusbar.configure (text=str_file_not_selected, background='#B71C1C', foreground='#EF9A9A')
            return

    if genre_split_state.get ():
        for current_genre in data['genres']:
            with open(Path (workdir, f'{current_genre["name"]}.m3u'), 'a') as current_file:
                current_file.write ('#EXTM3U\n')
    else:
        with open(workfile, 'a') as current_file:
            current_file.write ('#EXTM3U\n')

    for current_channel in data['stations']:
        current_country = search_in_array ('countries', str(current_channel['country_id']), 'id', 'name')
        
        if country.get () != str_all_countries and current_country != country.get ():
            continue
        
        if city.get () != str_all_cities:
            write_this_station = False
            for current_city_id in current_channel['cities_ids']:
                if city.get () == search_in_array ('cities', str(current_city_id), 'id', 'name'):
                    write_this_station = True
            if write_this_station == False:
                continue
        
        if fix_stream_state.get ():
            current_stream = current_channel['stream'].replace ('http://stream.pcradio.ru:8000/', fix_stream_mode.get())
        else:
            current_stream = current_channel['stream']
        current_channel_genres = current_channel['genres_ids']

        if hq_logo_state.get ():
            current_logo = current_channel['logo'].replace ('thumbnail90', 'thumbnail350').replace ('.jpeg', '-350.jpeg').replace ('.png', '-350.png')
        else:
            current_logo = current_channel['logo']

        for current_genre_id in current_channel_genres:
            current_genre = search_in_array ('genres', str(current_genre_id), 'id', 'name')
            if genre_split_state.get ():
                current_genre_file = Path (workdir, f'{current_genre}.m3u')
            else:
                current_genre_file = workfile
            if add_metadata_state.get ():
                channel_genres = ''
                for current_genre_id in current_channel_genres:
                    current_genre = search_in_array ('genres', str(current_genre_id), 'id', 'name')
                    channel_genres += current_genre + ';'
                channel_genres = channel_genres[:-1]
                metadata = f' tvg-logo=\"{current_logo}\" group-title=\"{channel_genres}\" radio=\"true\"'
            else:
                metadata = ''
            with open(current_genre_file, 'a') as current_file:
                current_file.write (f'#EXTINF:-1{metadata}, {current_channel["name"]}\n')
            with open(current_genre_file, 'a') as current_file:
                current_file.write (f'{current_stream}-{quality.get()}\n')
            if not (genre_split_state.get ()):
                break

    statusbar.configure (text=str_done, background='#BF360C', foreground='#FFAB91')

root = Tk ()
root.title (str_app_title)
root.resizable (width=False, height=False)
root.attributes ('-alpha', 0.9)
root.config (background='#222')

Style().configure ('.', background='#222', foreground='#AAA', anchor='center')
Style().map ('.', background=[('active', '#222')], foreground=[('active', '#CCC')])
Style().configure ('TLabel', background='#006064', foreground='#80DEEA')
Style().configure ('TCombobox', fieldbackground='#222')
Style().map ('TCombobox', fieldbackground=[('active', '#222')])
Style().configure ('TRadiobutton', indicatorcolor='#222')
Style().configure ('TCheckbutton', indicatorcolor='#222')

left_grp = Frame ()
right_grp = Frame ()

input_file_title = Label (left_grp, text=str_file_selection)
input_file_title.pack (fill=X)

choose_btn = Button (left_grp, text=str_select_file, command=input_file)
choose_btn.pack (padx=10, pady=10)

download_file_title = Label (right_grp, text=str_file_downloading)
download_file_title.pack (fill=X)

lang = StringVar ()
lang.set ('ru')
Radiobutton (right_grp, text=str_lang_ru, value='ru', variable=lang).pack ()
Radiobutton (right_grp, text=str_lang_en, value='en', variable=lang).pack ()

dl_btn = Button (right_grp, text=str_download_file, command=download_ziplist)
dl_btn.pack (padx=10, pady=10)

quality_title = Label (left_grp, text=str_quality)
quality_title.pack (fill=X)

quality = StringVar ()
quality.set ('med')
Radiobutton (left_grp, text='ЭКОНОМ (28K, AAC)', value='low', variable=quality).pack ()
Radiobutton (left_grp, text='СТАНДАРТ (42K, AAC)', value='med', variable=quality).pack ()
Radiobutton (left_grp, text='ПРЕМИУМ (64K, AAC)', value='hi', variable=quality).pack ()

country_title = Label (left_grp, text=str_country)
country_title.pack (fill=X)

country = Combobox(left_grp, state='readonly')
country['values'] = [str_all_countries]
country.current (0)
country.pack (padx=10, pady=10)
country.bind ("<<ComboboxSelected>>", get_city_list)

city_title = Label (left_grp, text=str_city)
city_title.pack (fill=X)

city = Combobox(left_grp, state='readonly')
city['values'] = [str_all_cities]
city.current (0)
city.pack (padx=10, pady=10)

advanced_settings_title = Label (right_grp, text=str_advanced_settings)
advanced_settings_title.pack (fill=X)

fix_stream_state = BooleanVar ()
fix_stream_state.set (True)
fix_stream = Checkbutton(right_grp, text=str_fix_stream, var=fix_stream_state)
fix_stream.pack ()

fix_stream_mode = Combobox(right_grp, values=['http://str.pcradio.ru/', 'http://str3.pcradio.ru/'])
fix_stream_mode.current (0)
fix_stream_mode.pack ()

genre_split_state = BooleanVar ()
genre_split_state.set (False)
genre_split = Checkbutton(right_grp, text=str_genre_split, var=genre_split_state)
genre_split.pack ()

add_metadata_state = BooleanVar ()
add_metadata_state.set (True)
add_metadata = Checkbutton(right_grp, text=str_add_metadata, var=add_metadata_state)
add_metadata.pack ()

hq_logo_state = BooleanVar ()
hq_logo_state.set (True)
hq_logo = Checkbutton(right_grp, text=str_quality_logo, var=hq_logo_state)
hq_logo.pack ()

save_as_title = Label (right_grp, text=str_saving)
save_as_title.pack (fill=X)

mk_btn = Button (right_grp, text=str_write_to_m3u, command=write_file, state='disabled')
mk_btn.pack (padx=10, pady=10)

statusbar = Label (text=str_file_not_selected, background='#880E4F', foreground='#F48FB1')
statusbar.pack (side=BOTTOM, fill=X)

left_grp.pack (side=LEFT, ipadx=10)
Label ().pack (side=LEFT, fill=Y)
right_grp.pack (side=RIGHT, ipadx=10)

root.mainloop ()
