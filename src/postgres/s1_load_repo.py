import os
from ..utils.load_repo import traverse_directory


DIRECTORY_PATH = "/app/repo/postgresql"
FILE_TYPES = {
    '.sgml': 'docs',
    '.c': 'code',
}


def get_document_type(filename):
    ext = os.path.splitext(filename)[1]
    return FILE_TYPES.get(ext)


def get_document_url(document_type, file_path):
    if document_type == 'code':
        return "https://github.com/postgres/postgres/blob/master/" + file_path
    if document_type == 'docs':
        basename = os.path.basename(file_path).split('.')[0]
        if '/ref/' in file_path:
            return f"https://www.postgresql.org/docs/15/sql-{basename.replace('_', '')}.html"
        else:
            return f"https://www.postgresql.org/docs/15/{basename}.html"


if __name__ == "__main__":
    traverse_directory(DIRECTORY_PATH, get_document_type, get_document_url)
