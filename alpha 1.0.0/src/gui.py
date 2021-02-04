"""
Copyright © 2021 Jonas Wombacher

This file is part of Image Tools.

Image Tools is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Image Tools is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Image Tools.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import tkinter as tk
from configparser import ConfigParser
from tkinter import filedialog, messagebox

import src.process_imgs as process
from src.values import *

config = ConfigParser()
config.read("config.ini")


# saves the config to the config file, e.g. after changing language or the default suffix
def save_config():
    with open('config.ini', 'w') as f:
        config.write(f)
        f.close()


# display a popup with the given error messages to the user, errors has to be a list of strings
def show_errors(errors):
    msg_string = ""
    for error in errors:
        msg_string += error + "\n"
    tk.messagebox.showerror(title="Error!", message=msg_string)


# display a popup with the given information messages, information has to be a list of strings
def show_info(information):
    msg_string = ""
    for info in information:
        msg_string += info + "\n"
    tk.messagebox.showinfo(message=msg_string)


class GUI:
    def __init__(self):
        self.root = None

        # text fields for source, destination and suffix
        self.input_text_field = None
        self.output_text_field = None
        self.suffix_text_field = None

        # language to start the application in
        self.lang = config.get("main", "language")
        self.suffix_default = config.get("main", "suffix")

        # frames
        self.main_frame = None
        self.param_frame_width_height = None
        self.param_frame_position = None
        self.param_frame_left_top = None
        self.param_frame_percentage = None
        self.param_frame_enhance = None
        self.param_frame_flip = None
        self.param_frame_rotate = None

        # parameter text fields, IntVars ...
        self.menu_lang_var = None
        self.param_width = None
        self.param_height = None
        self.param_position = None
        self.param_left = None
        self.param_top = None
        self.param_percentage = None
        self.param_contrast = None
        self.param_saturation = None
        self.param_brightness = None
        self.param_sharpness = None
        self.param_flip_mode = None
        self.param_rotate = None

        # used when changing the language
        self.labels = {}  # dictionary to hold all labels, the keys are the text-codes needed to get the labels' text
        self.buttons = {}  # always append e.g. _0 to the key in order to distinguish widgets with the same text

        # variables for the selection menus
        self.select_tool_menu = None
        self.select_tool_sv = None

        # menus
        self.menu_main = None
        self.menu_settings = None
        self.menu_lang = None

        self.run()

    # opens a filedialog and fills in the selected source directory
    def input_select_dir(self):
        directory = filedialog.askdirectory(title=get_ui_text("filedialog_folder", self.lang))
        self.input_text_field.delete(0, tk.END)
        self.input_text_field.insert(0, directory)

        if directory != "" and self.output_text_field.get() == "":
            self.output_text_field.delete(0, tk.END)
            self.output_text_field.insert(0, directory + "/" + get_ui_text("default_out", self.lang))

    # opens a filedialog and fills in the selected source files
    def input_select_files(self):
        files = filedialog.askopenfilenames(title=get_ui_text("filedialog_files", self.lang),
                                            filetypes=((get_ui_text("filedialog_types", self.lang), "*.png;*.jpg"),))
        self.input_text_field.delete(0, tk.END)
        self.input_text_field.insert(0, ", ".join(files))
        # make sure the filenames contain no commas
        if len(files) > 0 and len(files) - 1 < self.input_text_field.get().count(","):
            self.input_text_field.delete(0, tk.END)
            show_errors([get_ui_text("error_filename", self.lang)])

        if files != "" and self.output_text_field.get() == "":
            self.output_text_field.delete(0, tk.END)
            self.output_text_field.insert(0, os.path.split(files[0])[0] + "/" + get_ui_text("default_out", self.lang))

    # opens a filedialog and fills in the selected destination directory
    def output_select_dir(self):
        directory = filedialog.askdirectory(title=get_ui_text("filedialog_folder", self.lang))
        self.output_text_field.delete(0, tk.END)
        self.output_text_field.insert(0, directory)

    # changes the current app language to the given lang
    def command_change_language(self, lang):
        self.lang = lang
        config.set("main", "language", lang)
        save_config()

        for key in self.labels:
            self.labels[key]["text"] = get_ui_text(key[:-2], lang)
        for key in self.buttons:
            self.buttons[key]["text"] = get_ui_text(key[:-2], lang)
        self.refresh_tool_menu("EN" if lang == "DE" else "DE")
        self.refresh_menu_bar()
        self.refresh_suffix("EN" if lang == "DE" else "DE")

    # selects the clicked tool and shows/hides the parameters accordingly
    def command_tool_menu_clicked(self, value):
        if value == get_ui_text("tool_options", self.lang)[0]:  # crop at predefined position
            self.param_frame_width_height.grid(row=0, column=0)
            self.param_frame_position.grid(row=1, column=0)
            self.param_frame_left_top.grid_forget()
            self.param_frame_percentage.grid_forget()
            self.param_frame_enhance.grid_forget()
            self.param_frame_flip.grid_forget()
            self.param_frame_rotate.grid_forget()
        elif value == get_ui_text("tool_options", self.lang)[1]:  # crop at variable position
            self.param_frame_width_height.grid(row=0, column=0)
            self.param_frame_position.grid_forget()
            self.param_frame_left_top.grid(row=1, column=0)
            self.param_frame_percentage.grid_forget()
            self.param_frame_enhance.grid_forget()
            self.param_frame_flip.grid_forget()
            self.param_frame_rotate.grid_forget()
        elif value == get_ui_text("tool_options", self.lang)[2]:  # resize by percentage
            self.param_frame_width_height.grid_forget()
            self.param_frame_position.grid_forget()
            self.param_frame_left_top.grid_forget()
            self.param_frame_percentage.grid(row=0, column=0)
            self.param_frame_enhance.grid_forget()
            self.param_frame_flip.grid_forget()
            self.param_frame_rotate.grid_forget()
        elif value == get_ui_text("tool_options", self.lang)[3]:  # resize by dimensions
            self.param_frame_width_height.grid(row=0, column=0)
            self.param_frame_position.grid_forget()
            self.param_frame_left_top.grid_forget()
            self.param_frame_percentage.grid_forget()
            self.param_frame_enhance.grid_forget()
            self.param_frame_flip.grid_forget()
            self.param_frame_rotate.grid_forget()
        elif value == get_ui_text("tool_options", self.lang)[4]:  # enhance images
            self.param_frame_width_height.grid_forget()
            self.param_frame_position.grid_forget()
            self.param_frame_left_top.grid_forget()
            self.param_frame_percentage.grid_forget()
            self.param_frame_enhance.grid(row=0, column=0)
            self.param_frame_flip.grid_forget()
            self.param_frame_rotate.grid_forget()
        elif value == get_ui_text("tool_options", self.lang)[5]:  # apply greyscale
            self.param_frame_width_height.grid_forget()
            self.param_frame_position.grid_forget()
            self.param_frame_left_top.grid_forget()
            self.param_frame_percentage.grid_forget()
            self.param_frame_enhance.grid_forget()
            self.param_frame_flip.grid_forget()
            self.param_frame_rotate.grid_forget()
        elif value == get_ui_text("tool_options", self.lang)[6]:  # flip images
            self.param_frame_width_height.grid_forget()
            self.param_frame_position.grid_forget()
            self.param_frame_left_top.grid_forget()
            self.param_frame_percentage.grid_forget()
            self.param_frame_enhance.grid_forget()
            self.param_frame_flip.grid(row=0, column=0)
            self.param_frame_rotate.grid_forget()
        elif value == get_ui_text("tool_options", self.lang)[7]:  # rotate images
            self.param_frame_width_height.grid_forget()
            self.param_frame_position.grid_forget()
            self.param_frame_left_top.grid_forget()
            self.param_frame_percentage.grid_forget()
            self.param_frame_enhance.grid_forget()
            self.param_frame_flip.grid_forget()
            self.param_frame_rotate.grid(row=0, column=0)

    # triggered when the suffix button is clicked, resets the suffix field to the default value
    def suffix_button_clicked(self):
        self.suffix_text_field.delete(0, tk.END)
        self.suffix_text_field.insert(0, self.suffix_default)

    # triggered when the new default suffix button is pressed, changes the default suffix to the current one
    def suffix_button_new_clicked(self):
        self.suffix_default = self.suffix_text_field.get()
        config.set("main", "suffix", self.suffix_text_field.get())
        save_config()

    # rebuilds the tool menu when the language was changed
    def refresh_tool_menu(self, old_lang):
        self.select_tool_menu.destroy()
        old_options = get_ui_text("tool_options", old_lang)
        for i in range(len(old_options)):
            if self.select_tool_sv.get() == old_options[i]:
                self.select_tool_sv.set(get_ui_text("tool_options", self.lang)[i])
                self.command_tool_menu_clicked(self.select_tool_sv.get())
                break

        select_menu = tk.OptionMenu(self.main_frame, self.select_tool_sv, *get_ui_text("tool_options", self.lang),
                                    command=lambda x: self.command_tool_menu_clicked(x))
        select_menu.config(width=tool_menu_width)
        select_menu.grid(row=0, column=1, pady=20)
        self.select_tool_menu = select_menu

    # refreshes the labels in the menu bar when the language was changed
    def refresh_menu_bar(self):
        self.menu_main.entryconfigure(1, label=get_ui_text("menu_settings", self.lang))
        self.menu_settings.entryconfigure(1, label=get_ui_text("menu_lang", self.lang))

    # refreshes the suffix if it has the default value when the language was changed
    def refresh_suffix(self, old_lang):
        if self.suffix_text_field.get() == get_ui_text("default_suffix", old_lang):
            self.suffix_text_field.delete(0, tk.END)
            self.suffix_text_field.insert(0, get_ui_text("default_suffix", self.lang))

    # method validating all user input, returns a bool (True = correct) and a list of error messages, if there are some
    def validate_inputs(self):
        correct = True
        errors = []

        try:  # check the input path
            input_text = self.input_text_field.get()
            if ", " in input_text:
                for path in input_text.split(", "):
                    if not os.path.isfile(path):
                        correct = False
                        break
            else:
                if not os.path.isdir(input_text) and not os.path.isfile(input_text):
                    correct = False
        except:
            correct = False
        if not correct:
            errors.append(get_ui_text("error_input", self.lang))

        try:  # check the output path
            if not os.path.isdir(self.output_text_field.get()):
                print(self.output_text_field.get().rsplit("/", 1)[0])
                if not os.path.isdir(self.output_text_field.get().rsplit("/", 1)[0]):
                    correct = False
                    errors.append(get_ui_text("error_output", self.lang))
        except:
            correct = False
            errors.append(get_ui_text("error_output", self.lang))

        # make sure the filenames contain no commas
        if "," in self.input_text_field.get():
            for path in self.input_text_field.get().split(", "):
                if not os.path.isfile(path.replace(",", "")):
                    correct = False
                    errors.append(get_ui_text("error_filename", self.lang))
                    break

        try:  # check the tool parameters (pixels, percentage)
            greater_than_0 = True
            if self.param_width.winfo_ismapped():
                if not int(self.param_width.get()) > 0:
                    greater_than_0 = False
            if self.param_height.winfo_ismapped():
                if not int(self.param_height.get()) > 0:
                    greater_than_0 = False
            if self.param_percentage.winfo_ismapped():
                if not int(self.param_percentage.get().replace("%", "")) > 0:
                    greater_than_0 = False
            if not greater_than_0:
                correct = False
                errors.append(get_ui_text("error_params_zero", self.lang))
        except:
            correct = False
            errors.append(get_ui_text("error_params_num", self.lang))

        try:  # check the tool parameters (enhance factors + left & top + angle)
            geq_0 = True
            if self.param_left.winfo_ismapped():
                if not int(self.param_left.get()) >= 0:
                    geq_0 = False
            if self.param_top.winfo_ismapped():
                if not int(self.param_top.get()) >= 0:
                    geq_0 = False
            if self.param_contrast.winfo_ismapped():
                if not float(self.param_contrast.get()) >= 0:
                    geq_0 = False
            if self.param_saturation.winfo_ismapped():
                if not float(self.param_saturation.get()) >= 0:
                    geq_0 = False
            if self.param_brightness.winfo_ismapped():
                if not float(self.param_brightness.get()) >= 0:
                    geq_0 = False
            if self.param_sharpness.winfo_ismapped():
                if not float(self.param_sharpness.get()) >= 0:
                    geq_0 = False
            if not geq_0:
                correct = False
                errors.append((get_ui_text("error_params_zero", self.lang)))

            if self.param_rotate.winfo_ismapped():
                angle = float(self.param_rotate.get())
        except:
            correct = False
            errors.append(get_ui_text("error_params_num", self.lang))

        try:  # check the suffix
            suffix = self.suffix_text_field.get()
            for char in "<>:\"/\\|?*":
                if char in suffix:
                    correct = False
                    errors.append(get_ui_text("error_suffix", self.lang))
                    break
        except:
            correct = False
            errors.append(get_ui_text("error_suffix", self.lang))

        return correct, errors

    # triggers the actual image processing after reading in the parameters from the input fields
    def command_submit_button(self):
        if self.input_text_field.get() == "" or self.output_text_field.get() == "":
            show_errors([get_ui_text("error_io", self.lang)])
            return
        tool = self.select_tool_sv.get()

        correct, msgs = self.validate_inputs()
        params = None
        if correct:
            if tool == get_ui_text("tool_options", self.lang)[0]:  # crop around predefined position
                params = process.Params(width=self.param_width.get(), height=self.param_height.get(),
                                        pos=self.param_position.get())
            elif tool == get_ui_text("tool_options", self.lang)[1]:  # crop at variable position
                params = process.Params(width=self.param_width.get(), height=self.param_height.get(),
                                        left=self.param_left.get(), top=self.param_top.get())
            elif tool == get_ui_text("tool_options", self.lang)[2]:  # resize by percentage
                percentage = int(self.param_percentage.get().replace("%", ""))
                params = process.Params(perc=percentage)
            elif tool == get_ui_text("tool_options", self.lang)[3]:  # resize by dimensions
                params = process.Params(width=self.param_width.get(), height=self.param_height.get())
            elif tool == get_ui_text("tool_options", self.lang)[4]:  # enhance images
                contrast, saturation = float(self.param_contrast.get()), float(self.param_saturation.get())
                brightness, sharpness = float(self.param_brightness.get()), float(self.param_sharpness.get())
                params = process.Params(contrast=contrast, saturation=saturation, brightness=brightness,
                                        sharpness=sharpness)
            elif tool == get_ui_text("tool_options", self.lang)[5]:  # apply greyscale
                params = process.Params()
            elif tool == get_ui_text("tool_options", self.lang)[6]:  # flip images
                params = process.Params(flip_mode=self.param_flip_mode.get())
            elif tool == get_ui_text("tool_options", self.lang)[7]:  # rotate images
                params = process.Params(angle=float(self.param_rotate.get()))

            count = 0
            if ", " in self.input_text_field.get():
                paths = self.input_text_field.get().split(", ")
                for path in paths:
                    count += process.process_imgs(path, params, tool, self.output_text_field.get(), self.lang,
                                                  self.suffix_text_field.get())
            else:
                count += process.process_imgs(self.input_text_field.get(), params, tool, self.output_text_field.get(),
                                              self.lang, self.suffix_text_field.get())
            show_info([get_ui_text("info_result", self.lang) + str(count)])
        else:
            show_errors(msgs)

    # builds and runs the gui
    def run(self):
        root = tk.Tk()
        root.title("Image Tools")
        root.iconbitmap("./image_tools.ico")
        root.geometry("850x800")  # width x height
        root.resizable(0, 0)
        self.root = root

        # canvas = tk.Canvas(root, height=100, width=850, bg="#424949").grid(row=0, column=0, columnspan=3)

        self.setup_menu_bar()
        self.setup_main_frame()
        self.setup_tool_menu()
        self.setup_param_frames()
        self.setup_input_output()
        self.setup_suffix()
        self.setup_process_button()

        # add spacing over the warnings
        self.main_frame.grid_rowconfigure(9, minsize=100)

        self.setup_warnings()

        root.mainloop()

    def setup_menu_bar(self):
        menu_main = tk.Menu(self.root, bg="#424949")
        self.root.config(menu=menu_main)

        menu_settings = tk.Menu(menu_main)
        menu_main.add_cascade(label=get_ui_text("menu_settings", self.lang), menu=menu_settings)
        menu_lang = tk.Menu(menu_settings)
        menu_lang_var = tk.IntVar()
        menu_lang_var.set(0 if self.lang == "EN" else 1)
        self.menu_lang_var = menu_lang_var
        menu_settings.add_cascade(label=get_ui_text("menu_lang", self.lang), menu=menu_lang)
        menu_lang.add_radiobutton(label="English", value=0, variable=self.menu_lang_var,
                                  command=lambda: self.command_change_language("EN"))
        menu_lang.add_radiobutton(label="Deutsch", value=1, variable=self.menu_lang_var,
                                  command=lambda: self.command_change_language("DE"))

        self.menu_main = menu_main
        self.menu_settings = menu_settings
        self.menu_lang = menu_lang

    def setup_main_frame(self):
        main_frame = tk.Frame(self.root, bg="#ABB2B9")
        main_frame.pack(fill=tk.BOTH, expand=1)
        self.main_frame = main_frame
        main_frame.grid_columnconfigure(0, minsize=150)
        # main_frame.place(relwidth=1, relheight=0.95, rely=0.05)

    def setup_tool_menu(self):
        select_label = tk.Label(self.main_frame, text=get_ui_text("label_tool", self.lang))
        select_label.grid(row=0, column=0, padx=5, sticky="E")
        self.labels["label_tool_0"] = select_label

        select_tool_sv = tk.StringVar()
        select_tool_sv.set(get_ui_text("tool_options", self.lang)[0])
        select_tool_menu = tk.OptionMenu(self.main_frame, select_tool_sv, *get_ui_text("tool_options", self.lang),
                                         command=lambda x: self.command_tool_menu_clicked(x))
        select_tool_menu.config(width=tool_menu_width)
        select_tool_menu.grid(row=0, column=1, pady=20)
        self.select_tool_menu = select_tool_menu
        self.select_tool_sv = select_tool_sv

    def setup_param_frames(self):
        # parent frame for the param frames
        param_frame = tk.Frame(self.main_frame, bg="#ABB2B9")
        param_frame.grid(row=1, column=1)

        # param frame with width and height values (both crop tools)
        param_frame_width_height = tk.Frame(param_frame, bg="#ABB2B9")
        param_frame_width_height.grid(row=0, column=0)
        self.param_frame_width_height = param_frame_width_height

        param_label_width = tk.Label(param_frame_width_height, text=get_ui_text("label_width", self.lang))
        param_label_width.grid(row=0, column=0, padx=2, pady=5)
        self.labels["label_width_0"] = param_label_width
        param_text_width = tk.Entry(param_frame_width_height, width=10)
        param_text_width.grid(row=0, column=1, padx=5)
        self.param_width = param_text_width

        param_label_height = tk.Label(param_frame_width_height, text=get_ui_text("label_height", self.lang))
        param_label_height.grid(row=0, column=2, padx=2, pady=5)
        self.labels["label_height_0"] = param_label_height
        param_text_height = tk.Entry(param_frame_width_height, width=10)
        param_text_height.grid(row=0, column=3, padx=5)
        self.param_height = param_text_height

        # param frame with position selection menu
        param_frame_position = tk.Frame(param_frame, bg="#ABB2B9")
        param_frame_position.grid(row=1, column=0)
        self.param_frame_position = param_frame_position

        param_label_position = tk.Label(param_frame_position, text=get_ui_text("label_pos", self.lang))
        param_label_position.grid(row=1, column=0, padx=2, pady=5)
        self.labels["label_pos_0"] = param_label_position

        param_var_pos = tk.IntVar()
        param_var_pos.set(4)
        self.param_position = param_var_pos

        param_radio_pos_0 = tk.Radiobutton(param_frame_position, variable=param_var_pos, value=0)
        param_radio_pos_0.grid(row=0, column=1)
        param_radio_pos_1 = tk.Radiobutton(param_frame_position, variable=param_var_pos, value=1)
        param_radio_pos_1.grid(row=0, column=2)
        param_radio_pos_2 = tk.Radiobutton(param_frame_position, variable=param_var_pos, value=2)
        param_radio_pos_2.grid(row=0, column=3)
        param_radio_pos_3 = tk.Radiobutton(param_frame_position, variable=param_var_pos, value=3)
        param_radio_pos_3.grid(row=1, column=1)
        param_radio_pos_4 = tk.Radiobutton(param_frame_position, variable=param_var_pos, value=4)
        param_radio_pos_4.grid(row=1, column=2)
        param_radio_pos_5 = tk.Radiobutton(param_frame_position, variable=param_var_pos, value=5)
        param_radio_pos_5.grid(row=1, column=3)
        param_radio_pos_6 = tk.Radiobutton(param_frame_position, variable=param_var_pos, value=6)
        param_radio_pos_6.grid(row=2, column=1)
        param_radio_pos_7 = tk.Radiobutton(param_frame_position, variable=param_var_pos, value=7)
        param_radio_pos_7.grid(row=2, column=2)
        param_radio_pos_8 = tk.Radiobutton(param_frame_position, variable=param_var_pos, value=8)
        param_radio_pos_8.grid(row=2, column=3)

        # param frame with left and top values (crop at specific position)
        param_frame_left_top = tk.Frame(param_frame, bg="#ABB2B9")
        param_frame_left_top.grid(row=1, column=0)
        self.param_frame_left_top = param_frame_left_top

        param_label_left = tk.Label(param_frame_left_top, text=get_ui_text("label_left", self.lang))
        param_label_left.grid(row=0, column=0, padx=2, pady=5)
        self.labels["label_left_0"] = param_label_left
        param_text_left = tk.Entry(param_frame_left_top, width=10)
        param_text_left.grid(row=0, column=1, padx=5)
        self.param_left = param_text_left

        param_label_top = tk.Label(param_frame_left_top, text=get_ui_text("label_top", self.lang))
        param_label_top.grid(row=0, column=2, padx=2, pady=5)
        self.labels["label_top_0"] = param_label_top
        param_text_top = tk.Entry(param_frame_left_top, width=10)
        param_text_top.grid(row=0, column=3, padx=5)
        self.param_top = param_text_top

        param_frame_left_top.grid_forget()

        # param frame with percentage (resize by percentage)
        param_frame_percentage = tk.Frame(param_frame, bg="#ABB2B9")
        param_frame_percentage.grid(row=0, column=0)
        self.param_frame_percentage = param_frame_percentage

        param_label_percentage = tk.Label(param_frame_percentage, text=get_ui_text("label_percentage", self.lang))
        param_label_percentage.grid(row=0, column=0, padx=2, pady=5)
        self.labels["label_percentage_0"] = param_label_percentage
        param_text_percentage = tk.Entry(param_frame_percentage, width=10)
        param_text_percentage.grid(row=0, column=1, padx=5)
        self.param_percentage = param_text_percentage

        param_frame_percentage.grid_forget()

        # param frame with image enhancement values
        param_frame_enhance = tk.Frame(param_frame, bg="#ABB2B9")
        param_frame_enhance.grid(row=0, column=0)
        self.param_frame_enhance = param_frame_enhance

        param_label_contrast = tk.Label(param_frame_enhance, text=get_ui_text("label_contrast", self.lang))
        param_label_contrast.grid(row=0, column=0, padx=2, pady=5)
        self.labels["label_contrast_0"] = param_label_contrast
        param_text_contrast = tk.Entry(param_frame_enhance, width=10)
        param_text_contrast.grid(row=0, column=1, padx=5)
        param_text_contrast.insert(0, "1.0")
        self.param_contrast = param_text_contrast

        param_label_saturation = tk.Label(param_frame_enhance, text=get_ui_text("label_saturation", self.lang))
        param_label_saturation.grid(row=0, column=2, padx=2, pady=5)
        self.labels["label_saturation_0"] = param_label_saturation
        param_text_saturation = tk.Entry(param_frame_enhance, width=10)
        param_text_saturation.grid(row=0, column=3, padx=5)
        param_text_saturation.insert(0, "1.0")
        self.param_saturation = param_text_saturation

        param_label_brightness = tk.Label(param_frame_enhance, text=get_ui_text("label_brightness", self.lang))
        param_label_brightness.grid(row=1, column=0, padx=2, pady=5)
        self.labels["label_brightness_0"] = param_label_brightness
        param_text_brightness = tk.Entry(param_frame_enhance, width=10)
        param_text_brightness.grid(row=1, column=1, padx=5)
        param_text_brightness.insert(0, "1.0")
        self.param_brightness = param_text_brightness

        param_label_sharpness = tk.Label(param_frame_enhance, text=get_ui_text("label_sharpness", self.lang))
        param_label_sharpness.grid(row=1, column=2, padx=2, pady=5)
        self.labels["label_sharpness_0"] = param_label_sharpness
        param_text_sharpness = tk.Entry(param_frame_enhance, width=10)
        param_text_sharpness.grid(row=1, column=3, padx=5)
        param_text_sharpness.insert(0, "1.0")
        self.param_sharpness = param_text_sharpness

        param_label_enhance_info = tk.Label(param_frame_enhance, text=get_ui_text("label_enhance_info", self.lang))
        param_label_enhance_info.grid(row=2, column=1, pady=5, columnspan=2, sticky="E")
        self.labels["label_enhance_info_0"] = param_label_enhance_info

        param_frame_enhance.grid_forget()

        # param frame with radiobuttons to choose flip mode
        param_frame_flip = tk.Frame(param_frame, bg="#ABB2B9")
        param_frame_flip.grid(row=0, column=0)
        self.param_frame_flip = param_frame_flip

        param_var_flip = tk.IntVar()
        param_var_flip.set(0)
        self.param_flip_mode = param_var_flip

        param_radio_flip_v = tk.Radiobutton(param_frame_flip, text=get_ui_text("radio_flip_v", self.lang), padx=10,
                                            variable=param_var_flip, value=0)
        param_radio_flip_v.grid(row=0, column=0)
        self.buttons["radio_flip_v_0"] = param_radio_flip_v

        param_radio_flip_h = tk.Radiobutton(param_frame_flip, text=get_ui_text("radio_flip_h", self.lang), padx=10,
                                            variable=param_var_flip, value=1)
        param_radio_flip_h.grid(row=0, column=1)
        self.buttons["radio_flip_h_0"] = param_radio_flip_h

        param_frame_flip.grid_forget()

        # param frame with angle for rotating images
        param_frame_rotate = tk.Frame(param_frame, bg="#ABB2B9")
        param_frame_rotate.grid(row=0, column=0)
        self.param_frame_rotate = param_frame_rotate

        param_label_rotate = tk.Label(param_frame_rotate, text=get_ui_text("label_angle", self.lang))
        param_label_rotate.grid(row=0, column=0, padx=2, pady=5)
        self.labels["label_angle_0"] = param_label_rotate
        param_text_rotate = tk.Entry(param_frame_rotate, width=10)
        param_text_rotate.grid(row=0, column=1, padx=5)
        self.param_rotate = param_text_rotate

        param_frame_rotate.grid_forget()

    def setup_input_output(self):
        # INPUT PATH
        input_label = tk.Label(self.main_frame, text=get_ui_text("label_input", self.lang))
        input_label.grid(row=3, column=0, padx=5, sticky="E")
        self.labels["label_input_0"] = input_label

        input_text_field = tk.Entry(self.main_frame, width=75)
        input_text_field.grid(row=3, column=1, padx=5)
        self.input_text_field = input_text_field

        input_open_folder_button = tk.Button(self.main_frame, text=get_ui_text("button_folder", self.lang), padx=10,
                                             pady=5,
                                             fg="#CCD1D1", bg="#424949", activebackground="#CCD1D1",
                                             command=lambda: self.input_select_dir())
        input_open_folder_button.grid(row=3, column=3, pady=2)
        self.buttons["button_folder_0"] = input_open_folder_button

        input_open_files_button = tk.Button(self.main_frame, text=get_ui_text("button_files", self.lang), padx=10,
                                            pady=5,
                                            fg="#CCD1D1", bg="#424949", activebackground="#CCD1D1",
                                            command=lambda: self.input_select_files())
        input_open_files_button.grid(row=3, column=4, pady=2)
        self.buttons["button_files_0"] = input_open_files_button

        # OUTPUT PATH
        output_label = tk.Label(self.main_frame, text=get_ui_text("label_output", self.lang))
        output_label.grid(row=5, column=0, padx=5, sticky="E")
        self.labels["label_output_0"] = output_label

        output_text_field = tk.Entry(self.main_frame, width=75)
        output_text_field.grid(row=5, column=1, padx=5)
        self.output_text_field = output_text_field

        output_open_folder_button = tk.Button(self.main_frame, text=get_ui_text("button_folder", self.lang), padx=10,
                                              pady=5,
                                              fg="#CCD1D1", bg="#424949", activebackground="#CCD1D1",
                                              command=lambda: self.output_select_dir())
        output_open_folder_button.grid(row=5, column=3, pady=2)
        self.buttons["button_folder_1"] = output_open_folder_button

    def setup_suffix(self):
        suffix_label = tk.Label(self.main_frame, text=get_ui_text("label_suffix", self.lang))
        suffix_label.grid(row=6, column=0, padx=5, sticky="E")
        self.labels["label_suffix_0"] = suffix_label

        suffix_text_field = tk.Entry(self.main_frame, width=25)
        suffix_text_field.grid(row=6, column=1, padx=5, sticky="W")
        suffix_text_field.delete(0, tk.END)
        suffix_text_field.insert(0, self.suffix_default)
        self.suffix_text_field = suffix_text_field

        suffix_new_default_button = tk.Button(self.main_frame, text=get_ui_text("button_new_suffix", self.lang),
                                              padx=10,
                                              pady=5, fg="#CCD1D1", bg="#424949", activebackground="#CCD1D1",
                                              command=self.suffix_button_new_clicked)
        suffix_new_default_button.grid(row=6, column=1, pady=2, sticky="E")
        self.buttons["button_new_suffix_0"] = suffix_new_default_button

        suffix_default_button = tk.Button(self.main_frame, text=get_ui_text("button_suffix", self.lang), padx=10,
                                          pady=5,
                                          fg="#CCD1D1", bg="#424949", activebackground="#CCD1D1",
                                          command=self.suffix_button_clicked)
        suffix_default_button.grid(row=6, column=3, pady=2, sticky="W")
        self.buttons["button_suffix_0"] = suffix_default_button

    def setup_process_button(self):
        process_button = tk.Button(self.main_frame, text=get_ui_text("button_process", self.lang), padx=10, pady=5,
                                   fg="#CCD1D1", bg="#424949",
                                   activebackground="#CCD1D1",
                                   command=lambda: self.command_submit_button())
        process_button.grid(row=8, column=1, pady=5)
        self.buttons["button_process_0"] = process_button

    def setup_warnings(self):
        warning_overwrite = tk.Message(self.main_frame, text=get_ui_text("warning_overwrite", self.lang), width=450)
        warning_overwrite.grid(row=10, column=1, pady=10, sticky="W")
        self.labels["warning_overwrite_0"] = warning_overwrite

        warning_filename = tk.Message(self.main_frame, text=get_ui_text("warning_filename", self.lang), width=400)
        warning_filename.grid(row=11, column=1, pady=10, sticky="W")
        self.labels["warning_filename_0"] = warning_filename


gui = GUI()
