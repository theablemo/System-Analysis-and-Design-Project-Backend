from backend.settings import CONTENTS_DIR


def get_raw_file_name(file_name):
    # Separate the file name from its extension
    return file_name.split('.')[0]


def content_file_path(content, file_name):
    return f'{CONTENTS_DIR}{content.member.id}_{content.library.name}_{get_raw_file_name(file_name)}_{file_name}'