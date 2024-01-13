import os

from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError


def prepare_to_downloading(file_path):
    if not os.path.exists("media/"):
        os.makedirs("media/")
    if os.path.exists(file_path):
        os.remove(file_path)


def get_number_of_pages(file_path) -> int:
    """Возвращает количесвто страниц, если файл валиден. В противном случае
    возвращает 0"""
    try:
        file = PdfReader(file_path)
        number_of_pages = len(file.pages)
        for i in range(number_of_pages):
            paper_size = list(file.pages[i]["/MediaBox"])
            if not (
                paper_size[0] == 0
                and paper_size[1] == 0
                and (
                    (595 <= paper_size[2] <= 597 and 841 <= paper_size[3] <= 843)
                    or (595 <= paper_size[3] <= 597 and 841 <= paper_size[2] <= 843)
                )
            ):
                return 0

    except PdfReadError:
        return 0
    return number_of_pages
