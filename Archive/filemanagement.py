import os
import shutil

def pull_log_from_mprem():
    path = os.path.join(os.getcwd(), 'mprem_files')
    path_to_push = os.path.join(os.getcwd(), 'Logs')
    files = os.listdir(path)
    for file in files:
        if file.endswith(".csv"):
            shutil.move(os.path.join(path,file), path_to_push)
    