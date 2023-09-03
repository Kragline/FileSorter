import os
import shutil
from tkinter import *
from tkinter import ttk
from tkinter import filedialog


class FileSorter:

    def __init__(self, master: Tk):
        self.files_by_type = {
            'audio': ('mp3', 'aac', 'wav', 'ogg', 'flac'),
            'video': ('mp4', 'avi', 'mkv', 'mov', 'wmv'),
            'photo': ('jpeg', 'jpg', 'png', 'gif', 'svg'),
            'text': ('docx', 'txt'),
            'pdf': ('pdf',)
        }

        self.window = master

        self.label = ttk.Label(self.window, text='Sort files by type', font='15')
        self.label.place(relx=0.5, rely=0.3, anchor=CENTER)

        self.button = ttk.Button(self.window, text='Choose directory', command=self.sort_files)
        self.button.place(relx=0.5, rely=0.6, anchor=CENTER)

    def get_file_type(self, file_extension: str):
        for file_type, extensions in self.files_by_type.items():
            if file_extension.lower() in extensions:
                return file_type

        return 'other'

    def move_file(self, src_path, target_dir):
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        shutil.move(src_path, os.path.join(target_dir, os.path.basename(src_path)))

    def sort_files(self):
        directory = filedialog.askdirectory()

        if directory:
            for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path):
                    f_extension = os.path.splitext(file_path)[1][1:]
                    file_type = self.get_file_type(f_extension)

                    if file_type == 'other':
                        target_path = os.path.join(directory, 'Other files')
                    else:
                        target_path = os.path.join(directory, file_type.capitalize() + 's')

                    self.move_file(file_path, target_path)
            os.startfile(directory)


if __name__ == '__main__':
    window = Tk()
    window.title('File sorter')
    window.geometry('300x200')
    window.resizable(False, False)

    FileSorter(window)
    window.mainloop()
