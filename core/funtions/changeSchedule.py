import os
import shutil
PARENT = os.getcwd()
CURRENT_SCH = f"{PARENT}\\core\\source\\"
NEW_SCH = f"{PARENT}\\core\\new_schedule"
ARCHIVE = f"{PARENT}\\core\\archive"

def get_file_path(folder):
    res=''
    for file in os.listdir(folder):
        res = os.path.join(folder,file)   
    return res


def empty_folder(folder):
    for file in os.listdir(folder):
        path = os.path.join(folder,file)
        os.remove(path)

def swap_schedules(CURRENT_SCH=CURRENT_SCH,NEW_SCH=NEW_SCH, ARCHIVE=ARCHIVE):
    CURRENT_SCH = get_file_path(CURRENT_SCH)
    NEW_SCH = get_file_path(NEW_SCH)
    empty_folder(ARCHIVE)
    shutil.move(CURRENT_SCH,ARCHIVE)
    shutil.move(NEW_SCH,CURRENT_SCH)

