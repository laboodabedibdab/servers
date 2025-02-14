import ast

print("ast")
# from flet import Page, Text, TextField, ElevatedButton, Container, Column, CrossAxisAlignment, app, Colors, ThemeMode, Theme
# print("flet")
import customtkinter as ctk
from tkinter import messagebox

print("tkinter")
import minecraft_launcher_lib

print("minecraft_launcher_lib")
import subprocess

print("subprocess")
import os

print("os")
import nbtlib

print("nbtlib")
import jdk

print("jdk")
import requests

print("requests")


def download_file(url, save_path):
    """
    Скачивает файл по URL и сохраняет его по указанному пути.

    Args:
        url: URL файла для скачивания.
        save_path: Путь для сохранения файла.
    """
    try:
        response = requests.get(url, stream=True)  # stream=True для больших файлов
        response.raise_for_status()  # Проверяем успешность запроса

        # Создаем директорию, если она не существует
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Файл успешно скачан и сохранен по пути: {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при скачивании файла: {e}")
    except OSError as e:
        print(f"Ошибка при сохранении файла: {e}")


def sync_folder(folder_name):
    """
    Синхронизирует указанную папку с сервером.

    Args:
        folder_name (str): Название папки для синхронизации (например, 'mods' или 'config').
    """
    server_url = f"http://kartofanina.zapto.org/"

    try:
        # Получаем список файлов с сервера
        response = requests.get(server_url+"/"+folder_name+"/"+"json/")
        response.raise_for_status()
        server_files = response.json()  # Предполагается, что сервер возвращает JSON список файлов
        server_folders = server_files["folders"]
        server_files = server_files["files"]

        def install_files(directory, list_files):
            if not os.path.exists(os.path.join(minecraft_directory, directory)):
                os.makedirs(os.path.join(minecraft_directory, directory))
            for file in list_files:
                if not os.path.exists(os.path.join(minecraft_directory, directory, file)):
                    download_file(os.path.join(server_url,directory,file), os.path.join(minecraft_directory,directory,file))
                    print(f"Скачиваем {file} в папку {directory}")
                else:
                    print(f"Файл {file} уже существует в папке {folder_name}")

        # Скачиваем недостающие файлы
        for i,folder in enumerate(server_folders):
            folder.replace("\\","/")
            install_files(folder, server_files[i])
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при синхронизации папки {folder_name}: {e}")


def check_java():
    """Проверяет, установлена ли Java, и выводит ее версию."""
    try:
        # Пытаемся выполнить команду java -version и получить вывод
        process = subprocess.run(['java', '-version'], capture_output=True, text=True, check=True)
        output = process.stderr  # Вывод версии Java обычно идет в stderr

        # Извлекаем версию Java из вывода
        version_line = next((line for line in output.splitlines() if "version" in line), None)
        if version_line:
            version = version_line.split()[2].strip('"')
            return version
        else:
            return True

    except subprocess.CalledProcessError:
        return None


def read_dat(minecraft_directory):
    path = minecraft_directory + "/servers.dat"
    nbt_file = nbtlib.load(path)
    print(nbt_file)


def create_serversdat(minecraft_directory):
    path = minecraft_directory + "/servers.dat"
    download_file("https://github.com/laboodabedibdab/servers/raw/refs/heads/main/servers.dat", path)

#
# def get_mods_names():
#     mods = requests.get("http://kartofanina.zapto.org/mods/json").text[4:-3]
#     mods = [f[1:-1] for f in mods.split(",\n  ")]
#     print(mods)
#     return mods

#
# def download_mods(minecraft_directory, mod):
#     path = minecraft_directory + "/mods/"
#     if not os.path.exists(path):
#         os.makedirs(path)
#     mod_path = path + mod
#     print("downloadin mod: " + mod)
#     download_file('http://kartofanina.zapto.org/mods/' + mod, mod_path)


def create_config_file(filepath, content):
    """
    Creates a text file at the specified path with the given content.

    Args:
        filepath: The full path to the file to be created.
        content: The text content to write to the file.
    """
    filepath = filepath + "/options.txt"
    try:
        # Ensure the directory exists
        directory = os.path.dirname(filepath)
        if directory:  # Check if a directory part exists
            os.makedirs(directory, exist_ok=True)  # Create directory if needed

        with open(filepath, 'w') as file:
            file.write(content)
        print(f"File created successfully at: {filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")



file_content = """version:3465
autoJump:false
operatorItemsTab:false
autoSuggestions:true
chatColors:true
chatLinks:true
chatLinksPrompt:true
enableVsync:true
entityShadows:true
forceUnicodeFont:false
discrete_mouse_scroll:false
invertYMouse:false
realmsNotifications:true
reducedDebugInfo:false
showSubtitles:false
directionalAudio:false
touchscreen:false
fullscreen:true
bobView:true
toggleCrouch:false
toggleSprint:false
darkMojangStudiosBackground:false
hideLightningFlashes:false
mouseSensitivity:0.5
fov:0.0
screenEffectScale:1.0
fovEffectScale:1.0
darknessEffectScale:1.0
glintSpeed:0.5
glintStrength:0.75
damageTiltStrength:1.0
highContrast:false
gamma:0.5
renderDistance:12
simulationDistance:12
entityDistanceScaling:1.0
guiScale:0
particles:0
maxFps:120
graphicsMode:1
ao:true
prioritizeChunkUpdates:0
biomeBlendRadius:2
renderClouds:"true"
resourcePacks:[]
incompatibleResourcePacks:[]
lastServer:
lang:en_us
soundDevice:""
chatVisibility:0
chatOpacity:1.0
chatLineSpacing:0.0
textBackgroundOpacity:0.5
backgroundForChatOnly:true
hideServerAddress:false
advancedItemTooltips:false
pauseOnLostFocus:true
overrideWidth:0
overrideHeight:0
chatHeightFocused:1.0
chatDelay:0.0
chatHeightUnfocused:0.4375
chatScale:1.0
chatWidth:1.0
notificationDisplayTime:1.0
mipmapLevels:4
useNativeTransport:true
mainHand:"right"
attackIndicator:1
narrator:0
tutorialStep:movement
mouseWheelSensitivity:1.0
rawMouseInput:true
glDebugVerbosity:1
skipMultiplayerWarning:true
skipRealms32bitWarning:false
hideMatchedNames:true
joinedFirstServer:false
hideBundleTutorial:false
syncChunkWrites:true
showAutosaveIndicator:true
allowServerListing:true
onlyShowSecureChat:false
panoramaScrollSpeed:1.0
telemetryOptInExtra:false
onboardAccessibility:false
key_key.attack:key.mouse.left
key_key.use:key.mouse.right
key_key.forward:key.keyboard.w
key_key.left:key.keyboard.a
key_key.back:key.keyboard.s
key_key.right:key.keyboard.d
key_key.jump:key.keyboard.space
key_key.sneak:key.keyboard.leshift
key_key.sprint:key.keyboard.lecontrol
key_key.drop:key.keyboard.q
key_key.inventory:key.keyboard.e
key_key.chat:key.keyboard.t
key_key.playerlist:key.keyboard.tab
key_key.pickItem:key.mouse.middle
key_key.command:key.keyboard.slash
key_key.socialInteractions:key.keyboard.p
key_key.screenshot:key.keyboard.f2
key_key.togglePerspective:key.keyboard.f5
key_key.smoothCamera:key.keyboard.unknown
key_key.fullscreen:key.keyboard.f11
key_key.spectatorOutlines:key.keyboard.unknown
key_key.swapOffhand:key.keyboard.f
key_key.saveToolbarActivator:key.keyboard.c
key_key.loadToolbarActivator:key.keyboard.x
key_key.advancements:key.keyboard.l
key_key.hotbar.1:key.keyboard.1
key_key.hotbar.2:key.keyboard.2
key_key.hotbar.3:key.keyboard.3
key_key.hotbar.4:key.keyboard.4
key_key.hotbar.5:key.keyboard.5
key_key.hotbar.6:key.keyboard.6
key_key.hotbar.7:key.keyboard.7
key_key.hotbar.8:key.keyboard.8
key_key.hotbar.9:key.keyboard.9
soundCategory_master:1.0
soundCategory_music:1.0
soundCategory_record:1.0
soundCategory_weather:1.0
soundCategory_block:1.0
soundCategory_hostile:1.0
soundCategory_neutral:1.0
soundCategory_player:1.0
soundCategory_ambient:1.0
soundCategory_voice:1.0
modelPart_cape:true
modelPart_jacket:true
modelPart_left_sleeve:true
modelPart_right_sleeve:true
modelPart_left_pants_leg:true
modelPart_right_pants_leg:true
modelPart_hat:true
"""

# username = os.environ.get("USERNAME")
# minecraft_directory = "C:/Users/" + username + "/Desktop/minecraft"
# print(minecraft_directory)
# version = "1.20.1"
# username = "Kartofanina"
# jv = check_java()
# if not str(jv[0:2]) == '23':
#     jdk.install('23')
# else:
#     print("Java already installed")
# if not os.path.exists(minecraft_directory):
#     print("Creating directory")
#     os.makedirs(minecraft_directory)
# else:
#     print("Minecraft directory already exists")
# if 4 > len(os.listdir(minecraft_directory)):
#     print("Installing minecraft version")
#     forge_version = minecraft_launcher_lib.forge.find_forge_version(version)
#     minecraft_launcher_lib.forge.install_forge_version(forge_version, minecraft_directory)
# else:
#     print("Minecraft/forge already installed")
# if not os.path.exists(minecraft_directory + "/options.txt"):
#     print("Creating options.txt")
#     create_config_file(minecraft_directory, file_content)
# else:
#     print("Minecraft options already created")
# if not os.path.exists(minecraft_directory + "/servers.dat"):
#     print("Creating servers.dat")
#     create_serversdat(minecraft_directory)
# else:
#     print("Minecraft servers already created")
# print("Mods work in progress")
# sync_folder("mods")
# print("Mods config folder in progress")
# sync_folder("config")
#
#
# # Define launch options
# def start(username):
#     options = {
#         'username': username
#     }
#     forge_version = minecraft_launcher_lib.forge.find_forge_version(version)
#     # Launch Minecraft
#     process = subprocess.Popen(
#         minecraft_launcher_lib.command.get_minecraft_command(version=forge_version[:7] + "forge-" + forge_version[7:],
#                                                              minecraft_directory=minecraft_directory,
#                                                              options=options))
#
#
# db = ast.literal_eval(requests.get("http://kartofanina.zapto.org/users/").text)
# print(db)
#
#
#
# def start_message(name):
#     messagebox.showinfo("Успех", f"Добро пожаловать, {name}!")
#     start(name)
#
#
# def login():
#     name = txt_name.get()
#     password = txt_password.get()
#     print(f"Имя: {name}, Пароль: {password}")
#
#     if name and password and name in db.keys() and db[name] == password:
#         start(name)
#     else:
#         messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")
#
# ctk.set_appearance_mode("System")
# ctk.set_default_color_theme("blue")
#
# app = ctk.CTk()
# app.geometry("600x400")
# app.title("Minecraft Launcher")
#
# # Центрирование окна (опционально, можно настроить отступы padding)
# window_width = app.winfo_reqwidth()
# window_height = app.winfo_reqheight()
# position_right = int(app.winfo_screenwidth() / 2 - window_width / 2)
# position_down = int(app.winfo_screenheight() / 2 - window_height / 2)
# app.geometry("+{}+{}".format(position_right, position_down))
#
# # Устанавливаем тему (опционально)
# ctk.set_appearance_mode("System")  # "System", "Dark", "Light"
# ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"
#
# # Создаем рамку (контейнер)
# frame = ctk.CTkFrame(app, corner_radius=10)
# frame.pack(pady=20, padx=20)  # Отступы от краёв окна
#
# txt_name = ctk.CTkEntry(frame, placeholder_text="Имя", width=200)
# txt_name.pack(pady=5)
#
# txt_password = ctk.CTkEntry(frame, placeholder_text="Пароль", width=200, show="*")  # show="*" скрывает пароль
# txt_password.pack(pady=5)
#
# btn = ctk.CTkButton(frame, text="Войти", command=login)
# btn.pack(pady=10)
#
# app.mainloop()

username = os.environ.get("USERNAME")
minecraft_directory = "C:/Users/" + username + "/Desktop/minecraft"
print(minecraft_directory)
version = "1.20.1"  # или другая версия
file_content = "" # Здесь должен быть ваш file_content
# username = "Kartofanina"  # Это теперь вводит пользователь
jv = check_java()
if not str(jv[0:2]) == '23':
    jdk.install('23')
else:
    print("Java already installed")

# Установка Minecraft теперь в функции install_minecraft

def install_minecraft(minecraft_directory, version):
    if not os.path.exists(minecraft_directory):
        print("Creating directory")
        os.makedirs(minecraft_directory)
    else:
        print("Minecraft directory already exists")
    progress_bar = ctk.CTkProgressBar(frame)
    progress_bar.pack(pady=5)
    progress_bar.start()

    status_label = ctk.CTkLabel(frame, text="Initializing...", font=ctk.CTkFont(size=12))
    status_label.pack()

    try:
        if 4 > len(os.listdir(minecraft_directory)):
            status_label.configure(text="Finding Forge version...")
            forge_version = minecraft_launcher_lib.forge.find_forge_version(version)

            status_label.configure(text="Installing Forge...")
            minecraft_launcher_lib.forge.install_forge_version(forge_version, minecraft_directory)
        else:
            print("Minecraft/forge already installed")

        if not os.path.exists(minecraft_directory + "/options.txt"):
            status_label.configure(text="Creating options.txt...")
            create_config_file(minecraft_directory, file_content)
        else:
            print("Minecraft options already created")

        if not os.path.exists(minecraft_directory + "/servers.dat"):
            status_label.configure(text="Creating servers.dat...")
            create_serversdat(minecraft_directory)
        else:
            print("Minecraft servers already created")

        status_label.configure(text="Installing mods...")
        print("Mods work in progress")
        sync_folder("mods")

        status_label.configure(text="Configuring mods...")
        print("Mods config folder in progress")
        sync_folder("config")

        status_label.configure(text="Finished!")

        progress_bar.stop()
        progress_bar.pack_forget()
        status_label.pack_forget()
        return True

    except Exception as e:
        print(f"Error during installation: {e}")
        progress_bar.stop()
        progress_bar.pack_forget()
        status_label.configure(text=f"Error: {e}")
        messagebox.showerror("Ошибка", f"Ошибка установки: {e}")
        return False

def start(username):
    options = {
        'username': username
    }
    forge_version = minecraft_launcher_lib.forge.find_forge_version(version)
    # Launch Minecraft
    process = subprocess.Popen(
        minecraft_launcher_lib.command.get_minecraft_command(version=forge_version[:7] + "forge-" + forge_version[7:],
                                                             minecraft_directory=minecraft_directory,
                                                             options=options))

db = ast.literal_eval(requests.get("http://kartofanina.zapto.org/users/").text)
print(db)

def start_message(name):
    messagebox.showinfo("Успех", f"Добро пожаловать, {name}!")
    start(name)

def login():
    name = txt_name.get()
    password = txt_password.get()

    if name and password and name in db.keys() and db[name] == password:
        try:
            get_p=txt_path.get()
            path_get = minecraft_directory if get_p=="" else get_p
            if install_minecraft(path_get, version):
                start_message(name)
        except Exception as e:
            print(e)
            messagebox.showerror("Ошибка", "Неверный путь к папке")

    else:
        messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("600x400")
app.title("Minecraft Launcher")

window_width = app.winfo_reqwidth()
window_height = app.winfo_reqheight()
position_right = int(app.winfo_screenwidth() / 2 - window_width / 2)
position_down = int(app.winfo_screenheight() / 2 - window_height / 2)
app.geometry("+{}+{}".format(position_right, position_down))

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

frame = ctk.CTkFrame(app, corner_radius=10)
frame.pack(pady=20, padx=20)

txt_path = ctk.CTkEntry(frame, placeholder_text="Папка игры", width=200)
txt_path.pack(pady=5)

txt_name = ctk.CTkEntry(frame, placeholder_text="Имя", width=200)
txt_name.pack(pady=5)

txt_password = ctk.CTkEntry(frame, placeholder_text="Пароль", width=200, show="*")
txt_password.pack(pady=5)

btn = ctk.CTkButton(frame, text="Войти", command=login)
btn.pack(pady=10)

app.mainloop()