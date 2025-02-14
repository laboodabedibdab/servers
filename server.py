import os
from flask import Flask, render_template, send_file, jsonify

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users/')
def users():
    return {"Kartofanina":"3003","Fenula":"Fenula","Paket":"Paket","Ponchik":"163459","KurvaJoghik":"2008","Geket":"Geket","ijustseen":"","stopstarter":"IATOWS","NoHit":"komuNyaCum"}#

@app.route('/Sanya/')
def sanya():
    return render_template('sanya.html')

@app.route('/Nika/')
def nika():
    return render_template('nika.html')

@app.route('/Zhenya/')
def zhenya():
    return render_template('zhenya.html')

@app.route('/<path:folder>/')  # <path:> для корректной обработки слешей в URL
def folder(folder):
    # Вариант 1: Относительный путь (скорее всего, то, что вам нужно)
    full_path = os.path.join(app.root_path, folder)  # app.root_path - корень приложения Flask
    try:
        if os.path.isdir(full_path):
            items = os.listdir(full_path)  # Получаем список файлов И папок
            return render_template('files.html', folder=folder, items=items)
        else:
            return send_file(folder)

    except FileNotFoundError:
        return "Папка не найдена", 404
    except PermissionError:
        return "Нет прав доступа", 403
    except Exception as e:  # Обработка других исключений
        return f"Ошибка: {e}", 500
@app.route('/<path:folder>/json/')
def folder_json(folder):
    folders=[]
    files=[]
    for folder,_,file in os.walk(folder):
        folders.append(folder)
        files.append(file)
    dict_folder = {"folders":folders, "files":files}
    return jsonify(dict_folder)

# @app.route('/<folder>/<path>/')
# def download_file(folder, path):
#     folder = folder.replace("-","/")
#     return send_from_directory(folder, path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
