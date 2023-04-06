import os


def prepare_to_downloading(file_path):
    if not os.path.exists("media/"):
        os.makedirs("media/")
    if os.path.exists(file_path):
        os.remove(file_path)
