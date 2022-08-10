from backend.settings import CONTENTS_DIR
import random


def get_raw_file_name(file_name):
    # Separate the file name from its extension
    return file_name.split('.')[0]


def content_file_path(content, file_name):
    return f'{CONTENTS_DIR}{content.id}{content.member.id}_{random.randint(1, 999999)}_{file_name}'
