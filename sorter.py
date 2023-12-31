import os
import json
import shutil
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox


class FileSorter:
    def __init__(self, master: Tk):
        self.files_by_type = self.__load_extensions()
        self.directory = None

        self.window = master

        self.label = ttk.Label(self.window, text='Choose directory')
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.input = ttk.Entry(self.window, width=30)
        self.input.grid(row=0, column=1)

        self.browse_button = ttk.Button(self.window, text='Browse', command=self.__browse_directory)
        self.browse_button.grid(row=0, column=2, padx=10, pady=10)

        self.sort_button = ttk.Button(self.window, text='Sort', command=self.__sort_files)
        self.sort_button.grid(row=1, column=2, padx=10, pady=10)

        self.clear_button = ttk.Button(self.window, text='Clear', command=self.__clear)
        self.clear_button.grid(row=1, column=1, padx=(110, 0), pady=10)

    @classmethod
    def __load_extensions(cls):
        with open('extensions.json', 'r') as file:
            return json.load(file)

    def __clear(self):
        self.input.delete(0, END)

    def __get_file_type(self, file_extension: str):
        for file_type, extensions in self.files_by_type.items():
            if file_extension.lower() in extensions:
                return file_type

        return 'other'

    @classmethod
    def __move_file(cls, src_path, target_dir):
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        shutil.move(str(src_path), str(os.path.join(target_dir, os.path.basename(src_path))))

    def __browse_directory(self):
        if new_directory := filedialog.askdirectory():
            self.input.delete(0, END)
            self.input.insert(0, new_directory)

    def __get_dir_path(self):
        if dir_path := self.input.get():
            self.directory = dir_path

    def __sort_files(self):
        self.__get_dir_path()

        if self.directory:
            try:
                for file in os.listdir(self.directory):
                    file_path = os.path.join(self.directory, file)
                    if os.path.isfile(file_path):
                        f_extension = os.path.splitext(file_path)[1][1:]
                        file_type = self.__get_file_type(f_extension)

                        if file_type == 'other':
                            target_path = os.path.join(self.directory, 'Other files')
                        else:
                            target_path = os.path.join(self.directory, file_type.capitalize() + ' files')

                        self.__move_file(file_path, target_path)
                self.__clear()
                os.startfile(self.directory)
                self.directory = None
            except FileNotFoundError:
                messagebox.showerror("Directory error", "No such directory")
        else:
            messagebox.showwarning('Warning!', 'Specify directory for sorting')


if __name__ == '__main__':
    window = Tk()
    window.title('File sorter')
    window.geometry('400x100')
    window.resizable(False, False)

    FileSorter(window)
    window.mainloop()
