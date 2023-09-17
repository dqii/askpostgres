import os
from ..utils.load_repo import traverse_directory


DIRECTORY_PATH = "/app/repo/llama_index"
FILE_TYPES = {
    '.md': 'docs',
    '.py': 'code',
}


def get_document_type(filename):
    ext = os.path.splitext(filename)[1]
    return FILE_TYPES.get(ext)


def get_document_url(document_type, file_path):
    return "https://github.com/jerryjliu/llama_index/blob/main/" + file_path


if __name__ == "__main__":
    traverse_directory(DIRECTORY_PATH, get_document_type, get_document_url)
