import os
import shutil
import datetime
import secrets

import tkinter as tk
from tkinter import filedialog

save_path = ""
current_character = ""

def generate_random_string():
    random_hex = ''.join(secrets.choice('0123456789abcdef') for _ in range(16))
    return random_hex

def get_file_timestamp(filename):
    global current_character
    file_path = "Characters/" + current_character + "/" + filename
    return os.path.getmtime(file_path)

def promptEnter():
    print("\n\t[ -- Press Enter to continue -- ]")
    input("")

def validate_save_path():
    global save_path

    if (len(os.listdir(save_path))) == 0:
        return()

    if (len(os.listdir(save_path))) != 3:
        print("\n\tWARNING: Error validating save directory. Unexpected file structure for save folder.\n\t\t Please ensure that you have selected the correct directory. File removal is permanent and unrecoverable.")
        quit()

    remote_folder = False
    remote_vdf = False
    for item in os.listdir(save_path):
        if (item == "remote"):
            remote_folder = True
        elif (item == "remotecache.vdf"):
            remote_vdf = True
    
    if (remote_folder == False):
        print("\n\tWARNING: Error validating save directory. Could not find remote folder.\n\t\t  Please ensure that you have selected the correct directory. File removal is permanent and unrecoverable.")
        quit()

    if (remote_vdf == False):
        print("\n\tWARNING: Error validating save directory. Could not find remotecache.vdf.\n\t\t  Please ensure that you have selected the correct directory. File removal is permanent and unrecoverable.")
        quit()

def clear_save_directory():
    global save_path
    
    #clearing save directory
    print("\n\tClearing save directory...")

    #validate save path
    validate_save_path()

    count = 0
    for filename in os.listdir(save_path+"/remote/win64_save"):
        if (count > 3):
            error_path = save_path+"/remote/win64_save"
            print(f"WARNING: Abnormal file structure dectected while deleting from {error_path}. Aborting now.")
            quit()
        file_path = os.path.join(save_path+"/remote/win64_save", filename)
        os.remove(file_path)
        print(f"\tDeleted: {file_path}")
        count += 1

def stage_save_directory(source_path):
    global save_path

    win_save_path = save_path+"/remote/win64_save"

    print("")
    for filename in os.listdir(source_path):
        source_file = os.path.join(source_path, filename)
        destination_file = os.path.join(win_save_path, filename)
        shutil.copyfile(source_file, destination_file)
        print(f"\tDeployed file: {source_file}")

def remove_character_file():
    for item in os.listdir(os.getcwd()):
        s = item.split(".")
        if (len(s) == 1): continue
        if (s[1] == "character"):
            os.remove(os.path.join(os.getcwd(), item))

def create_file(file_path):
    with open(file_path, 'w'):
        pass

def initialize():

    global save_path

    os.system("cls")
    print("\t\t\t+ +\t\t\t\t\t\t\t\t+ +")
    print("\t\t\t+ \t\t\t\t\t\t\t\t  +")
    print("\t\t\t\t\t\t\tSave Manager\n\n")
    print("\t\t\t\t WARNING: This program is still in development and may\n\t\t\t\t\t  cause issues with your game. Additionally,\n\t\t\t\t\t  please be sure to CLOSE your game before using\n\t\t\t\t\t  this program.\n\n\n\t\t\t\t\t  Use at your own risk.")
    print("\n")
    print("\t\t\t\t\t  [ -- Press enter to continue -- ]")
    print("\t\t\t+ \t\t\t\t\t\t\t\t  +")
    print("\t\t\t+ +\t\t\t\t\t\t\t\t+ +")
    input("")

    os.system("cls")

    print("\n\tInitializing Save Manager...")
    
    current_directory = os.getcwd()
    character_folder = os.path.join(current_directory, "Characters")
    
    if (os.path.exists(character_folder) == False):
        os.mkdir("Characters")

    print("\n\tPlease select your save folder. This folder usually has a path similar\n\tto Steam/userdata/{some number}/{game id}")

    print("\n\t [ -- Press Enter to continue to folder selection -- ]")
    input("")

    # Create a tkinter window (this will not be displayed)
    root = tk.Tk()
    root.withdraw()

    # Open a file dialog and store the selected file path
    file_path = filedialog.askdirectory()
    global save_path
    global current_character
    save_path = file_path
    # Print the selected file path
    print("\tSelected folder:", save_path)


    validate_save_path()

    character_list = os.listdir(os.path.join(os.getcwd(), "Characters"))
    if (len(character_list) == 0):
        print("\n\tNo saved characters detected. Importing current character...")
        folder_name = input("\tPlease name the folder for the imported character: ")

        os.mkdir("Characters/"+folder_name)
        print(f"\n\tCharacter {folder_name} successfully created.\n")
        
        os.mkdir("Characters/"+folder_name+"/main_save")

        if (len(os.listdir(save_path+"/remote/win64_save")) == 0):
            print("WARNING: Error importing current character. No save data found. Please start the game to generate save data.")
            quit()

        for filename in os.listdir(save_path+"/remote/win64_save"):
            source_file = os.path.join(save_path+"/remote/win64_save", filename)
            destination_file = os.path.join("Characters/"+folder_name+"/main_save", filename)
            shutil.copy(source_file, destination_file)
            print(f"\tImported {source_file}")

        current_character = folder_name
        create_file(current_character + ".character")

        print("\n\tImported current character successfully.")
        promptEnter()
    
    if (current_character == ""):
        #look for .character file
        for filename in os.listdir(os.getcwd()):
            s = filename.split(".")
            if (len(s) == 1): continue
            if (s[1] == "character"):
                current_character = s[0]
        
        if (current_character == ""):
            print("\n\tNo .character file found. Please indicate your current character.\n")
            character_count = 0
            for character in character_list:
                character_count += 1
                print(f"\t{character_count}. {character}")
                
            user_input = input("\n\tChoose an option: ")

            user_input = int(user_input)
            if (user_input <= 0 or user_input > character_count):
                print("\n\tInvalid character selected.")
                quit()
            
            current_character = character_list[user_input-1]
            create_file(current_character + ".character")

    run()

def new_character():

    global current_character

    os.system("cls")

    print("\n\tWARNING: Creating a new character will remove your current save game.\n\t\t Please back up your current save game before proceeding.\n")

    user_input = input("\n\tDo you still wish to proceed? [Y/N]: ")

    if (user_input != "Y" and user_input != "y"):
        return

    auto_save()

    while (True):
        os.system("cls")

        print("================================")
        print("Create a New Character")

        folder_name = input("\tChoose a name: ")
        new_folder_directory = os.path.join(os.getcwd(), "Characters/"+folder_name)
        if (os.path.exists(new_folder_directory) == False):
            
            clear_save_directory()

            print("\n\tCreating new character folder...")

            os.mkdir("Characters/"+folder_name)
            print(f"\n\tCharacter {folder_name} successfully created.\n")
            
            os.mkdir("Characters/"+folder_name+"/main_save")

            current_character = folder_name

            remove_character_file()
            create_file(current_character+".character")

            promptEnter()

            break
        else:
            print("\n\t Character folder name already exists. Please choose a new name.")
            print("\n\t[ -- Press Enter to continue -- ]")
            input("")

def auto_save():

    print("")
    save_list = os.listdir("Characters/"+current_character)
    num_saves = len(save_list)
    num_saves = str(num_saves)
    save_name = "BackupSave"+num_saves
    random_string = "_"+generate_random_string()
    save_name = save_name + random_string
    os.mkdir("Characters/"+current_character+"/"+save_name)

    user_input= input("\n\tDo you want to back up your current save? [Y/N]: ")

    if (user_input != "Y" and user_input != "y"):
        return

    for filename in os.listdir(save_path+"/remote/win64_save"):
            source_file = os.path.join(save_path+"/remote/win64_save", filename)
            destination_file = os.path.join("Characters/"+current_character+"/"+save_name, filename)
            shutil.copy(source_file, destination_file)

def save_game():

    os.system("cls")

    print("Note: Saving the game will always overwrite the 'main_save' as well as creating an additional backup save")
    print("================================")
    print("Save Game")
    print("\t\t1. Confirm Save")
    print("\t\t2. Cancel")
    print("================================")
    
    user_input = input("Choose an option: ")

    if (user_input != "1"):
        return
    
    user_input = input("\n\t Would you like to name your save? [Y/N]: ")

    save_list = os.listdir("Characters/"+current_character)
    num_saves = len(save_list)
    num_saves = str(num_saves)
    save_name = "Save"+num_saves
    random_string = "_"+generate_random_string()
    save_name = save_name + random_string
    if (user_input == "Y" or user_input == "y"):
        while (True):
            user_input = input("\n\tEnter a name for your save: ")

            if (os.path.exists("Characters/"+current_character+"/"+user_input+random_string) == False):
                save_name = user_input + random_string
                break
            else:
                print("\tSave name already taken, please choose another.")
    
    os.mkdir("Characters/"+current_character+"/"+save_name)

    for filename in os.listdir(save_path+"/remote/win64_save"):
            source_file = os.path.join(save_path+"/remote/win64_save", filename)
            destination_file = os.path.join("Characters/"+current_character+"/"+save_name, filename)
            shutil.copy(source_file, destination_file)

    for filename in os.listdir(save_path+"/remote/win64_save"):
            source_file = os.path.join(save_path+"/remote/win64_save", filename)
            destination_file = os.path.join("Characters/"+current_character+"/main_save", filename)
            shutil.copy(source_file, destination_file)
            print(f"\tSaved {source_file}")

    promptEnter()
    

def load_game():

    os.system("cls")

    print("================================")
    print("Load Game")
    print("\t(m). Main Save")
    save_count = 0
    save_list = os.listdir("Characters/"+current_character)
    sorted_save_list = sorted(save_list, key=get_file_timestamp, reverse=True)
    for save in sorted_save_list:
        save_count += 1
        save_file_path = os.path.join(os.getcwd(), "Characters/"+current_character+"/"+save)
        timestamp = os.path.getmtime(save_file_path)
        timestamp_dt_obj = datetime.datetime.fromtimestamp(timestamp)
        print(f"\t{save_count}. {save}\t\t\t\t |\t{timestamp_dt_obj}")
    print(f"\t{save_count+1}. Cancel")
    print("================================")
    
    while (True):
        user_input = input("Choose an option: ")

        if (user_input == "m"):
            # main save
            auto_save()
            clear_save_directory()
            stage_save_directory("Characters/"+current_character+"/main_save")
            promptEnter()
            return
        
        user_input = int(user_input)

        if (user_input <= 0 or user_input > save_count):
            return
        
        save_folder = sorted_save_list[user_input-1]
        
        auto_save()
        clear_save_directory()
        stage_save_directory("Characters/"+current_character+"/"+save_folder)
        break

    promptEnter()

def change_character():

    global current_character

    os.system("cls")
    print("\n\tWARNING: Changing your character will permanently remove your current save game.\n\t\t Please back up your current save game before proceeding.\n")

    user_input = input("\n\tDo you still wish to proceed? [Y/N]: ")

    if (user_input != "Y" and user_input != "y"):
        return

    auto_save()

    os.system("cls")

    print("================================")
    print("Select a Character")

    character_count = 0
    character_list =  os.listdir(os.path.join(os.getcwd(), "Characters"))
    for item in character_list:
        character_count += 1
        print(f"{character_count}. {item}")
    
    print(f"{character_count+1}. Exit")

    print("================================")
    user_input = input("Choose an option: ")

    user_input = int(user_input)

    if (user_input <= 0):
        return
    if (user_input > character_count):
        return
    
    current_character = character_list[user_input-1]
    remove_character_file()
    create_file(current_character+".character")

    character_dir = os.path.join(os.path.join(os.getcwd(), "Characters"), current_character)

    print("Selected character at: ", character_dir)

    clear_save_directory()
    
    stage_save_directory(character_dir+"\main_save")

    promptEnter()

def view_saves():
    os.system("cls")

    save_list = os.listdir("Characters/"+current_character)
    sorted_save_list = sorted(save_list, key=get_file_timestamp, reverse=True)

    print("================================")
    print("Save List:")
    save_count = 0
    for save in sorted_save_list:
        save_count += 1
        save_file_path = os.path.join(os.getcwd(), "Characters/"+current_character+"/"+save)
        timestamp = os.path.getmtime(save_file_path)
        timestamp_dt_obj = datetime.datetime.fromtimestamp(timestamp)
        print(f"\t{save_count}. {save}\t\t\t\t |\t{timestamp_dt_obj}")
    print("================================")

    promptEnter()

def run():

    while (True):

        os.system("cls")

        print("================================")
        print("Main Menu")
        print(f"\tActive Character: {current_character}")
        print("\t1. New Character")
        print("\t2. Save Game")
        print("\t3. Load Game")
        print("\t4. Change Character")
        print("\t5. View Saves")
        print("\t9. Quit")
        print("================================")

        user_input = input("Choose option: ")
        if (user_input == "9"):
            break
        elif (user_input == "1"):
            new_character()
        elif (user_input == "2"):
            save_game()
        elif (user_input == "3"):
            load_game()
        elif (user_input == "4"):
            change_character()
        elif (user_input == "5"):
            view_saves()
    
    terminate()

def terminate():
    quit()
    
if __name__ == "__main__":
    initialize()