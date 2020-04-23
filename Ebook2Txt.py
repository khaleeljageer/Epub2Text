import urllib.request
import json
import os
import pathlib
import subprocess
from tqdm import tqdm


path = str(pathlib.Path().absolute()) + '/books/'


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_url(url, output_path):
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(
            url, filename=output_path, reporthook=t.update_to)
    print('Completed')


def get_books():
    books_json = urllib.request.urlopen(
        "https://raw.githubusercontent.com/KaniyamFoundation/Free-Tamil-Ebooks/master/booksdb.json")
    books_data = json.loads(books_json.read().decode())
    return books_data['books']


def get_title(title):
    try:
        return title+'.epub'
    except UnicodeEncodeError:
        return u''.join(title, '.epub').encode('utf-8')


def download_files(url, title):
    newPath = path+title
    if not os.path.exists(newPath):
        os.makedirs(newPath)
    newTitle = get_title(title)
    bookPath = newPath+'/'+newTitle
    download_url(url, bookPath)


def convert_book(title, file_name):
    newPath = path+title
    bookName = get_title(title)
    ebookPath = newPath+'/'+bookName
    outBook = newPath+'/'+file_name
    subprocess.call(["ebook-convert", ebookPath, outBook+".txt", "--keep-links"])
    subprocess.call(["ebook-convert", ebookPath, outBook+".docx"])


if __name__ == "__main__":
    books = get_books()
    for book in books:
        title = book['title']
        file_name = title + '-' + book['author']
        download_files(book['epub'], title)
        convert_book(title, file_name)

    print('All Done')
