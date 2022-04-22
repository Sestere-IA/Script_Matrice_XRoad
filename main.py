"""
run :
- pyinstaller --noconfirm --onefile --windowed  "C:/Users/alexa/PycharmProjects/Script_Matrice_XRoad/main.py"
to create new exe
or use auto-py-to-exe

"""
import os
from datetime import datetime
import shutil
from zipfile import ZipFile
from tkinter import messagebox

dirname = os.path.join(os.path.expanduser('~'), "AppData\Local\XRoad\Saved\Demos")


def remove_replay_less_1min(dirname):
    for i, replayfile in enumerate(os.listdir(dirname)):
        filename, file_extension = os.path.splitext(replayfile)
        if file_extension == ".replay":
            complete_path = os.path.join(dirname, replayfile)
            print(complete_path)
            with open(complete_path, "rb") as file:
                magic_number = (hex(int.from_bytes(file.read(4), "little")))
                version = (hex(int.from_bytes(file.read(4), "little")))
                taille_milli_sec = (int.from_bytes(file.read(4), "little"))
                net_version = (hex(int.from_bytes(file.read(4), "little")))
                change_list = (hex(int.from_bytes(file.read(4), "little")))
                time_min = (taille_milli_sec / (1000 * 60)) % 60
            if time_min < 1:
                print("file to del")
                os.remove(complete_path)
            else:
                print("file to keep")


def create_1dir_per_day(dirname):
    dictonary_file_day_to_dir = {}
    for i, replayfile in enumerate(os.listdir(dirname)):
        filename, file_extension = os.path.splitext(replayfile)
        if file_extension == ".replay":
            complete_path = os.path.join(dirname, replayfile)
            date_of_creation = datetime.strptime(
                datetime.fromtimestamp(os.path.getctime(complete_path)).strftime('%Y-%m-%d'), '%Y-%m-%d')
            key = str(date_of_creation.year) + "-" + str(date_of_creation.month) + "-" + str(date_of_creation.day)
            if key in dictonary_file_day_to_dir:
                dictonary_file_day_to_dir[key].append(complete_path)
            else:
                dictonary_file_day_to_dir[key] = []
                dictonary_file_day_to_dir[key].append(complete_path)

    for different_day, list_files in dictonary_file_day_to_dir.items():
        try:
            os.makedirs(dirname + '\\' + different_day)
        except FileExistsError:
            print("Le dossier existe deja")
            pass
        for file in list_files:
            shutil.move(file, dirname + '\\' + different_day)


def createall_dir_per_month(dirname):
    dictonary_dir_to_month_zipped_dir = {}
    date = ""
    for dir in os.listdir(dirname):
        try:
            complete_path = os.path.join(dirname, dir)
            date = datetime.strptime(dir, '%Y-%m-%d')  # Checking if is a datedir
            key = str(date.year) + "-" + str(date.month)
            if key not in dictonary_dir_to_month_zipped_dir:
                dictonary_dir_to_month_zipped_dir[key] = []
                dictonary_dir_to_month_zipped_dir[key].append(complete_path)
            else:
                dictonary_dir_to_month_zipped_dir[key].append(complete_path)
        except ValueError:
            print("Ce n'est pas le bon type de fichier ")

    for different_month, list_dir in dictonary_dir_to_month_zipped_dir.items():
        try:
            os.makedirs(dirname + '\\' + different_month)
        except FileExistsError:
            print("Le dossier existe deja")
            pass
        for file in list_dir:
            try:
                shutil.move(file, dirname + '\\' + different_month)
            except shutil.Error:
                for file_to_move in os.listdir(file):
                    shutil.move(os.path.join(file, file_to_move),
                                os.path.join(dirname + '\\' + different_month, os.path.basename(file)))
                shutil.rmtree(file)


def zip_all_dir(dirname):
    list_of_zip_to_open = []
    list_of_zip = []
    list_of_dir = []
    for file in os.listdir(dirname):
        if os.path.join(dirname, file).endswith(".zip"):
            list_of_zip.append(file)
        if os.path.isdir(os.path.join(dirname, file)):
            list_of_dir.append(file)
    for folder in list_of_dir:
        for zip_folder in list_of_zip:
            if str(folder) in str(zip_folder):
                list_of_zip_to_open.append(zip_folder)

    if not list_of_zip_to_open:
        for file in os.listdir(dirname):
            if os.path.isdir(os.path.join(dirname, file)):
                shutil.make_archive(os.path.join(dirname, file), "zip", os.path.join(dirname, file))
    else:
        print("Ouvrir le zip")
        zip_manipulation(dirname, list_of_zip_to_open)


def zip_manipulation(dirname, list_of_zip_to_open):
    for file in os.listdir(dirname):
        print(file)
        if os.path.join(dirname, file).endswith(".zip") and file in list_of_zip_to_open:
            with ZipFile(os.path.join(dirname, file)) as current_zip_open:
                current_zip_open.extractall(dirname + "/tochange")
            for file_to_change in os.listdir(dirname + "/tochange"):
                try:
                    shutil.move(dirname + "/tochange/" + file_to_change, dirname + "/" + file[:-4])
                except shutil.Error:
                    # Same day so merge
                    for dir_to_need_to_go_to_futur_folder_zip in os.listdir(dirname + "/tochange"):
                        for file_to_need_to_go_to_futur_folder_zip in os.listdir(
                                dirname + "/tochange/" + dir_to_need_to_go_to_futur_folder_zip):
                            shutil.move(
                                dirname + "/tochange/" + dir_to_need_to_go_to_futur_folder_zip + "/" + file_to_need_to_go_to_futur_folder_zip,
                                dirname + "/" + file[:-4] + "/" + file_to_change)

            os.remove(os.path.join(dirname, file))
            shutil.rmtree(dirname + "/tochange")
            shutil.make_archive(os.path.join(dirname, file[:-4]), "zip", os.path.join(dirname, file[:-4]))
            # FileNotFoundError: [WinError 2] Le fichier spécifié est introuvable: 'C:\\Users\\alexa\\AppData\\Local\\XRoad\\Saved\\Demos\\2022-4.zip'


def remove_old_dir(dirname):
    for file in os.listdir(dirname):
        if os.path.isdir(os.path.join(dirname, file)):
            shutil.rmtree(os.path.join(dirname, file))


def send_to_nass():  # TODO
    pass


if __name__ == '__main__':
    remove_replay_less_1min(dirname)
    create_1dir_per_day(dirname)
    createall_dir_per_month(dirname)
    zip_all_dir(dirname)
    remove_old_dir(dirname)
    send_to_nass()
    messagebox.showinfo("XR_Replay_Sorted", "All .replay file are sorted")
