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

from PIL import ImageTk

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


# parses a bool from a string, everything except True and true is evaluated to False
def bool_from_string(string):
    if string in ["True", "true", "TRUE"]:
        return True
    return False


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
        self.output_default = config.get("main", "destination")

        # frames
        self.main_frame = None
        self.param_frame_width_height = None
        self.param_frame_position = None
        self.param_frame_left_top = None
        self.param_frame_percentage = None
        self.param_frame_aspect = None
        self.param_frame_enhance = None
        self.param_frame_flip = None
        self.param_frame_rotate = None

        # parameter text fields, IntVars ...
        self.param_width = None
        self.param_height = None
        self.param_position = None
        self.param_left = None
        self.param_top = None
        self.param_percentage = None
        self.param_aspect = None
        self.param_leq_geq = None
        self.param_contrast = None
        self.param_saturation = None
        self.param_brightness = None
        self.param_sharpness = None
        self.param_flip_mode = None
        self.param_rotate = None

        # radiobuttons that need to be toggled
        self.radios_leq_geq = None

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
        self.menu_lang_var = None
        self.menu_popups = None
        self.menu_popups_var_info = None

        # windows
        self.window_preview = None
        self.window_preview_canvas = None

        # preview window parameters
        self.window_preview_after = None  # to know if a preview reload has already been scheduled
        self.window_preview_last_width = 0
        self.window_preview_last_height = 0
        self.live_preview = None

        # images
        self.img_preview = None

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

    # is triggered when the setting for the info popup after processing is changed
    def command_change_setting_info(self):
        config.set("main", "info_popup", str(self.menu_popups_var_info.get()))
        save_config()

    # selects the clicked tool and shows/hides the parameters accordingly
    def command_tool_menu_clicked(self, value):
        if value == get_ui_text("tool_options", self.lang)[0]:  # crop at predefined position
            self.param_frame_width_height.grid(row=0, column=0)
            self.param_frame_position.grid(row=1, column=0)
            self.param_frame_left_top.grid_forget()
            self.param_frame_percentage.grid_forget()
            self.param_frame_aspect.grid_forget()
            self.param_frame_enhance.grid_forget()
            self.param_frame_flip.grid_forget()
            self.param_frame_rotate.grid_forget()
        elif value == get_ui_text("tool_options", self.lang)[1]:  # crop at variable position
            self.param_frame_width_height.grid(row=0, column=0)
            self.param_frame_position.grid_forget()
            self.param_frame_left_top.grid(row=1, column=0)
            self.param_frame_percentage.grid_forget()
            self.param_frame_aspect.grid_forget()
            self.param_frame_enhance.grid_forget()
            self.param_frame_flip.grid_forget()
            self.param_frame_rotate.grid_forget()
        elif value == get_ui_text("tool_options", self.lang)[2]:  # resize by percentage
            self.param_frame_width_height.grid_forget()
            self.param_frame_position.grid_forget()
            self.param_frame_left_top.grid_forget()
            self.param_frame_percentage.grid(row=0, column=0)
            self.param_frame_aspect.grid_forget()
            self.param_frame_enhance.grid_forget()
            self.param_frame_flip.grid_forget()
            self.param_frame_rotate.grid_forget()
        elif value == get_ui_text("tool_options", self.lang)[3]:  # resize by dimensions
            self.param_frame_width_height.grid(row=0, column=0)
            self.param_frame_position.grid_forget()
            self.param_frame_left_top.grid_forget()
            self.param_frame_percentage.grid_forget()
            self.param_frame_aspect.grid(row=1, column=0)
            self.param_frame_enhance.grid_forget()
            self.param_frame_flip.grid_forget()
            self.param_frame_rotate.grid_forget()
        elif value == get_ui_text("tool_options", self.lang)[4]:  # enhance images
            self.param_frame_width_height.grid_forget()
            self.param_frame_position.grid_forget()
            self.param_frame_left_top.grid_forget()
            self.param_frame_percentage.grid_forget()
            self.param_frame_aspect.grid_forget()
            self.param_frame_enhance.grid(row=0, column=0)
            self.param_frame_flip.grid_forget()
            self.param_frame_rotate.grid_forget()
        elif value == get_ui_text("tool_options", self.lang)[5]:  # apply greyscale
            self.param_frame_width_height.grid_forget()
            self.param_frame_position.grid_forget()
            self.param_frame_left_top.grid_forget()
            self.param_frame_percentage.grid_forget()
            self.param_frame_aspect.grid_forget()
            self.param_frame_enhance.grid_forget()
            self.param_frame_flip.grid_forget()
            self.param_frame_rotate.grid_forget()
        elif value == get_ui_text("tool_options", self.lang)[6]:  # flip images
            self.param_frame_width_height.grid_forget()
            self.param_frame_position.grid_forget()
            self.param_frame_left_top.grid_forget()
            self.param_frame_percentage.grid_forget()
            self.param_frame_aspect.grid_forget()
            self.param_frame_enhance.grid_forget()
            self.param_frame_flip.grid(row=0, column=0)
            self.param_frame_rotate.grid_forget()
        elif value == get_ui_text("tool_options", self.lang)[7]:  # rotate images
            self.param_frame_width_height.grid_forget()
            self.param_frame_position.grid_forget()
            self.param_frame_left_top.grid_forget()
            self.param_frame_percentage.grid_forget()
            self.param_frame_aspect.grid_forget()
            self.param_frame_enhance.grid_forget()
            self.param_frame_flip.grid_forget()
            self.param_frame_rotate.grid(row=0, column=0)

    # is triggered when the checkbox for keeping aspect ratio or not is clicked
    def command_aspect_check(self):
        self.radios_leq_geq[0].configure(state=("normal" if self.param_aspect.get() else "disabled"))
        self.radios_leq_geq[1].configure(state=("normal" if self.param_aspect.get() else "disabled"))

    # triggered when the suffix button is clicked, resets the suffix field to the default value
    def suffix_button_clicked(self):
        self.suffix_text_field.delete(0, tk.END)
        self.suffix_text_field.insert(0, self.suffix_default)

    # triggered when the new default suffix button is pressed, changes the default suffix to the current one
    def suffix_button_new_clicked(self):
        self.suffix_default = self.suffix_text_field.get()
        config.set("main", "suffix", self.suffix_text_field.get())
        save_config()

    # triggered when the default destination button is clicked, resets the destination field to the default
    def output_button_clicked(self):
        self.output_text_field.delete(0, tk.END)
        self.output_text_field.insert(0, self.output_default)

    # triggered when the new default destination button is pressed, changes the default destination to the current one
    def output_button_new_clicked(self):
        self.output_default = self.output_text_field.get()
        config.set("main", "destination", self.output_text_field.get())
        save_config()

    # resets all enhance parameter fields to 1.0
    def command_reset_enhance_button(self):
        self.param_contrast.delete(0, tk.END)
        self.param_contrast.insert(0, "1.0")
        self.param_saturation.delete(0, tk.END)
        self.param_saturation.insert(0, "1.0")
        self.param_brightness.delete(0, tk.END)
        self.param_brightness.insert(0, "1.0")
        self.param_sharpness.delete(0, tk.END)
        self.param_sharpness.insert(0, "1.0")

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
        self.menu_popups.entryconfigure(2, label=get_ui_text("menu_popups_info", self.lang))

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

    # opens a preview window if there is none, else displays new preview on the existing window
    def command_show_preview(self, scheduled=False):
        new_window = False
        # make sure there is a window do display the preview on
        if self.window_preview is None:
            if scheduled:  # don't open a new window, if the call was scheduled from a resize
                return
            self.open_preview_window()
            new_window = True
        else:
            try:
                self.window_preview.state()
            except tk.TclError:
                if scheduled:  # don't open a new window, if the call was scheduled from a resize
                    return
                self.window_preview.destroy()
                self.open_preview_window()
                new_window = True

        # get the preview image
        if self.input_text_field.get() == "" or self.output_text_field.get() == "":
            return
        tool = self.select_tool_sv.get()

        correct, msgs = self.validate_inputs()
        if correct:
            params = self.collect_tool_params()

            if ", " in self.input_text_field.get():
                paths = self.input_text_field.get().split(", ")
                self.img_preview = ImageTk.PhotoImage(process.preview_img(paths[0], params, tool, self.lang,
                                                                          self.window_preview, new_window))
            else:
                self.img_preview = ImageTk.PhotoImage(
                    process.preview_img(self.input_text_field.get(), params, tool, self.lang, self.window_preview,
                                        new_window))

        # actually place the preview on the window
        if self.window_preview_canvas is not None:
            self.window_preview_canvas.destroy()

        try:  # display preview
            canvas = tk.Canvas(self.window_preview, width=self.img_preview.width(), height=self.img_preview.height())
            canvas.pack()
            canvas.create_image(0, 0, anchor="nw", image=self.img_preview)
            self.window_preview_canvas = canvas
        except AttributeError:  # preview was not generated, maybe faulty user parameters
            pass

    # actually opens and configures a preview window
    def open_preview_window(self):
        self.window_preview = tk.Toplevel(self.root)
        self.window_preview.title(get_ui_text("title_preview", self.lang))
        self.window_preview.iconbitmap("./image_tools.ico")
        x_offset, y_offset = self.root.winfo_x() + dimensions_root[0] + distance_root_preview, self.root.winfo_y()
        self.window_preview.geometry("%dx%d+%d+%d" % (
            dimensions_preview[0], dimensions_preview[1], x_offset, y_offset))  # width x height + offsetslif
        self.window_preview.bind("<Configure>", self.callback_preview_resized)

    # triggers the actual image processing after reading in the parameters from the input fields
    def command_submit_button(self):
        if self.input_text_field.get() == "" or self.output_text_field.get() == "":
            show_errors([get_ui_text("error_io", self.lang)])
            return
        tool = self.select_tool_sv.get()

        correct, msgs = self.validate_inputs()
        if correct:
            params = self.collect_tool_params()
            count = 0
            if ", " in self.input_text_field.get():
                paths = self.input_text_field.get().split(", ")
                for path in paths:
                    count += process.process_imgs(path, params, tool, self.output_text_field.get(), self.lang,
                                                  self.suffix_text_field.get())
            else:
                count += process.process_imgs(self.input_text_field.get(), params, tool, self.output_text_field.get(),
                                              self.lang, self.suffix_text_field.get())
            if self.menu_popups_var_info.get():
                show_info([get_ui_text("info_result", self.lang) + str(count)])
        else:
            show_errors(msgs)

    # collects the parameters from the widgets and returns them in a Params object
    def collect_tool_params(self):
        tool = self.select_tool_sv.get()
        params = None
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
            params = process.Params(width=self.param_width.get(), height=self.param_height.get(),
                                    keep_aspect=self.param_aspect.get(), leq_geq=self.param_leq_geq.get())
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

        return params

    # is called when the preview window is resized, schedules a reload of the preview
    def callback_preview_resized(self, event):
        if self.window_preview_last_width == event.width and self.window_preview_last_height == event.height:
            if not self.live_preview.get():  # live preview depends on the resize event always firing
                return

        self.window_preview_last_width = event.width  # refreshing
        self.window_preview_last_height = event.height
        if self.window_preview_after is not None:
            self.root.after_cancel(self.window_preview_after)
        self.window_preview_after = self.root.after(after_resize, lambda: self.command_show_preview(True))

    # builds and runs the gui
    def run(self):
        root = tk.Tk()
        root.title("Image Tools")
        root.iconbitmap("./image_tools.ico")
        root.geometry("%dx%d" % dimensions_root)  # width x height
        root.resizable(0, 0)
        self.root = root

        # canvas = tk.Canvas(root, height=100, width=850, bg="#424949").grid(row=0, column=0, columnspan=3)

        self.setup_menu_bar()
        self.setup_main_frame()
        self.setup_tool_menu()
        self.setup_param_frames()
        self.setup_input_output()
        self.setup_suffix()
        self.setup_preview_process()

        # add spacing over the warnings
        self.main_frame.grid_rowconfigure(9, minsize=100)

        # load warnings to the main window
        self.setup_warnings()

        root.mainloop()

    def setup_menu_bar(self):
        menu_main = tk.Menu(self.root, bg=color_button_bg)
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

        menu_popups = tk.Menu(menu_settings)
        menu_popups_var_info = tk.BooleanVar()
        menu_popups_var_info.set(bool_from_string(config.get("main", "info_popup")))
        self.menu_popups_var_info = menu_popups_var_info
        menu_settings.add_cascade(label=get_ui_text("menu_popups", self.lang), menu=menu_popups)
        menu_popups.add_checkbutton(label=get_ui_text("menu_popups_info", self.lang),
                                    variable=self.menu_popups_var_info, onvalue=True, offvalue=False,
                                    command=self.command_change_setting_info)

        self.menu_main = menu_main
        self.menu_settings = menu_settings
        self.menu_lang = menu_lang
        self.menu_popups = menu_popups

    def setup_main_frame(self):
        main_frame = tk.Frame(self.root, bg=color_bg)
        main_frame.pack(fill=tk.BOTH, expand=1)
        self.main_frame = main_frame
        main_frame.grid_columnconfigure(0, minsize=150)
        # main_frame.place(relwidth=1, relheight=0.95, rely=0.05)

    def setup_tool_menu(self):
        select_label = tk.Label(self.main_frame, text=get_ui_text("label_tool", self.lang), bg=color_bg)
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
        param_frame = tk.Frame(self.main_frame, bg=color_bg)
        param_frame.grid(row=1, column=1)

        # param frame with width and height values (both crop tools)
        param_frame_width_height = tk.Frame(param_frame, bg=color_bg)
        param_frame_width_height.grid(row=0, column=0)
        self.param_frame_width_height = param_frame_width_height

        param_label_width = tk.Label(param_frame_width_height, text=get_ui_text("label_width", self.lang), bg=color_bg)
        param_label_width.grid(row=0, column=0, padx=2, pady=5)
        self.labels["label_width_0"] = param_label_width
        param_text_width = tk.Entry(param_frame_width_height, width=10, relief=tk.FLAT)
        param_text_width.grid(row=0, column=1, padx=5)
        self.param_width = param_text_width

        param_label_height = tk.Label(param_frame_width_height, text=get_ui_text("label_height", self.lang),
                                      bg=color_bg)
        param_label_height.grid(row=0, column=2, padx=2, pady=5)
        self.labels["label_height_0"] = param_label_height
        param_text_height = tk.Entry(param_frame_width_height, width=10, relief=tk.FLAT)
        param_text_height.grid(row=0, column=3, padx=5)
        self.param_height = param_text_height

        # param frame with position selection menu
        param_frame_position = tk.Frame(param_frame, bg=color_bg)
        param_frame_position.grid(row=1, column=0)
        self.param_frame_position = param_frame_position

        param_label_position = tk.Label(param_frame_position, text=get_ui_text("label_pos", self.lang), bg=color_bg)
        param_label_position.grid(row=1, column=0, padx=2, pady=5)
        self.labels["label_pos_0"] = param_label_position

        param_var_pos = tk.IntVar()
        param_var_pos.set(4)
        self.param_position = param_var_pos

        param_radio_pos_0 = tk.Radiobutton(param_frame_position, variable=param_var_pos, value=0, bg=color_bg)
        param_radio_pos_0.grid(row=0, column=1)
        param_radio_pos_1 = tk.Radiobutton(param_frame_position, variable=param_var_pos, value=1, bg=color_bg)
        param_radio_pos_1.grid(row=0, column=2, padx=5)
        param_radio_pos_2 = tk.Radiobutton(param_frame_position, variable=param_var_pos, value=2, bg=color_bg)
        param_radio_pos_2.grid(row=0, column=3)
        param_radio_pos_3 = tk.Radiobutton(param_frame_position, variable=param_var_pos, value=3, bg=color_bg)
        param_radio_pos_3.grid(row=1, column=1)
        param_radio_pos_4 = tk.Radiobutton(param_frame_position, variable=param_var_pos, value=4, bg=color_bg)
        param_radio_pos_4.grid(row=1, column=2, padx=5)
        param_radio_pos_5 = tk.Radiobutton(param_frame_position, variable=param_var_pos, value=5, bg=color_bg)
        param_radio_pos_5.grid(row=1, column=3)
        param_radio_pos_6 = tk.Radiobutton(param_frame_position, variable=param_var_pos, value=6, bg=color_bg)
        param_radio_pos_6.grid(row=2, column=1)
        param_radio_pos_7 = tk.Radiobutton(param_frame_position, variable=param_var_pos, value=7, bg=color_bg)
        param_radio_pos_7.grid(row=2, column=2, padx=5)
        param_radio_pos_8 = tk.Radiobutton(param_frame_position, variable=param_var_pos, value=8, bg=color_bg)
        param_radio_pos_8.grid(row=2, column=3)

        # param frame with left and top values (crop at specific position)
        param_frame_left_top = tk.Frame(param_frame, bg=color_bg)
        param_frame_left_top.grid(row=1, column=0)
        self.param_frame_left_top = param_frame_left_top

        param_label_left = tk.Label(param_frame_left_top, text=get_ui_text("label_left", self.lang), bg=color_bg)
        param_label_left.grid(row=0, column=0, padx=2, pady=5)
        self.labels["label_left_0"] = param_label_left
        param_text_left = tk.Entry(param_frame_left_top, width=10, relief=tk.FLAT)
        param_text_left.grid(row=0, column=1, padx=5)
        self.param_left = param_text_left

        param_label_top = tk.Label(param_frame_left_top, text=get_ui_text("label_top", self.lang), bg=color_bg)
        param_label_top.grid(row=0, column=2, padx=2, pady=5)
        self.labels["label_top_0"] = param_label_top
        param_text_top = tk.Entry(param_frame_left_top, width=10, relief=tk.FLAT)
        param_text_top.grid(row=0, column=3, padx=5)
        self.param_top = param_text_top

        param_frame_left_top.grid_forget()

        # param frame with percentage (resize by percentage)
        param_frame_percentage = tk.Frame(param_frame, bg=color_bg)
        param_frame_percentage.grid(row=0, column=0)
        self.param_frame_percentage = param_frame_percentage

        param_label_percentage = tk.Label(param_frame_percentage, text=get_ui_text("label_percentage", self.lang),
                                          bg=color_bg)
        param_label_percentage.grid(row=0, column=0, padx=2, pady=5)
        self.labels["label_percentage_0"] = param_label_percentage
        param_text_percentage = tk.Entry(param_frame_percentage, width=10, relief=tk.FLAT)
        param_text_percentage.grid(row=0, column=1, padx=5)
        self.param_percentage = param_text_percentage

        param_frame_percentage.grid_forget()

        # param frame with aspect ratio checkbox and radiobuttons
        param_frame_aspect = tk.Frame(param_frame, bg=color_bg)
        param_frame_aspect.grid(row=1, column=0)
        self.param_frame_aspect = param_frame_aspect

        param_label_aspect = tk.Label(param_frame_aspect, text=get_ui_text("label_aspect", self.lang), bg=color_bg)
        param_label_aspect.grid(row=0, column=0, padx=5)
        self.labels["label_aspect_0"] = param_label_aspect

        param_var_aspect = tk.BooleanVar()
        param_var_aspect.set(True)
        self.param_aspect = param_var_aspect
        param_checkbox_aspect = tk.Checkbutton(param_frame_aspect, text="", var=param_var_aspect, bg=color_bg,
                                               command=self.command_aspect_check)
        param_checkbox_aspect.grid(row=0, column=1)

        param_label_leq_geq_0 = tk.Label(param_frame_aspect, text=get_ui_text("label_leq_geq_0", self.lang),
                                         bg=color_bg)
        param_label_leq_geq_0.grid(row=1, column=0, padx=5)
        self.labels["label_leq_geq_0_0"] = param_label_leq_geq_0

        param_var_leq_geq = tk.IntVar()
        param_var_leq_geq.set(0)
        self.param_leq_geq = param_var_leq_geq

        param_radio_leq = tk.Radiobutton(param_frame_aspect, text="<=", variable=param_var_leq_geq, value=0,
                                         bg=color_bg)
        param_radio_leq.grid(row=1, column=1)
        param_radio_geq = tk.Radiobutton(param_frame_aspect, text=">=", variable=param_var_leq_geq, value=1,
                                         bg=color_bg)
        param_radio_geq.grid(row=1, column=2)
        self.radios_leq_geq = [param_radio_leq, param_radio_geq]

        param_label_leq_geq_1 = tk.Label(param_frame_aspect, text=get_ui_text("label_leq_geq_1", self.lang),
                                         bg=color_bg)
        param_label_leq_geq_1.grid(row=1, column=3, padx=5)
        self.labels["label_leq_geq_0_1"] = param_label_leq_geq_1

        param_frame_aspect.grid_forget()

        # param frame with image enhancement values
        param_frame_enhance = tk.Frame(param_frame, bg=color_bg)
        param_frame_enhance.grid(row=0, column=0)
        self.param_frame_enhance = param_frame_enhance

        param_label_contrast = tk.Label(param_frame_enhance, text=get_ui_text("label_contrast", self.lang), bg=color_bg)
        param_label_contrast.grid(row=0, column=0, padx=2, pady=5)
        self.labels["label_contrast_0"] = param_label_contrast
        param_text_contrast = tk.Entry(param_frame_enhance, width=10, relief=tk.FLAT)
        param_text_contrast.grid(row=0, column=1, padx=5)
        param_text_contrast.insert(0, "1.0")
        self.param_contrast = param_text_contrast

        param_label_saturation = tk.Label(param_frame_enhance, text=get_ui_text("label_saturation", self.lang),
                                          bg=color_bg)
        param_label_saturation.grid(row=0, column=2, padx=2, pady=5)
        self.labels["label_saturation_0"] = param_label_saturation
        param_text_saturation = tk.Entry(param_frame_enhance, width=10, relief=tk.FLAT)
        param_text_saturation.grid(row=0, column=3, padx=5)
        param_text_saturation.insert(0, "1.0")
        self.param_saturation = param_text_saturation

        param_label_brightness = tk.Label(param_frame_enhance, text=get_ui_text("label_brightness", self.lang),
                                          bg=color_bg)
        param_label_brightness.grid(row=1, column=0, padx=2, pady=5)
        self.labels["label_brightness_0"] = param_label_brightness
        param_text_brightness = tk.Entry(param_frame_enhance, width=10, relief=tk.FLAT)
        param_text_brightness.grid(row=1, column=1, padx=5)
        param_text_brightness.insert(0, "1.0")
        self.param_brightness = param_text_brightness

        param_label_sharpness = tk.Label(param_frame_enhance, text=get_ui_text("label_sharpness", self.lang),
                                         bg=color_bg)
        param_label_sharpness.grid(row=1, column=2, padx=2, pady=5)
        self.labels["label_sharpness_0"] = param_label_sharpness
        param_text_sharpness = tk.Entry(param_frame_enhance, width=10, relief=tk.FLAT)
        param_text_sharpness.grid(row=1, column=3, padx=5)
        param_text_sharpness.insert(0, "1.0")
        self.param_sharpness = param_text_sharpness

        reset_button = tk.Button(self.param_frame_enhance, text=get_ui_text("button_enhance", self.lang), padx=5,
                                 pady=2, fg=color_button_text, bg=color_button_bg, activebackground=color_button_text,
                                 command=self.command_reset_enhance_button, relief=tk.FLAT)
        reset_button.grid(row=1, column=4, padx=5)
        self.buttons["button_enhance_0"] = reset_button

        param_label_enhance_info = tk.Label(param_frame_enhance, text=get_ui_text("label_enhance_info", self.lang),
                                            bg=color_bg)
        param_label_enhance_info.grid(row=2, column=1, pady=5, columnspan=2, sticky="E")
        self.labels["label_enhance_info_0"] = param_label_enhance_info

        param_frame_enhance.grid_forget()

        # param frame with radiobuttons to choose flip mode
        param_frame_flip = tk.Frame(param_frame, bg=color_bg)
        param_frame_flip.grid(row=0, column=0)
        self.param_frame_flip = param_frame_flip

        param_var_flip = tk.IntVar()
        param_var_flip.set(0)
        self.param_flip_mode = param_var_flip

        param_radio_flip_v = tk.Radiobutton(param_frame_flip, text=get_ui_text("radio_flip_v", self.lang), padx=10,
                                            variable=param_var_flip, value=0, bg=color_bg)
        param_radio_flip_v.grid(row=0, column=0)
        self.buttons["radio_flip_v_0"] = param_radio_flip_v

        param_radio_flip_h = tk.Radiobutton(param_frame_flip, text=get_ui_text("radio_flip_h", self.lang), padx=10,
                                            variable=param_var_flip, value=1, bg=color_bg)
        param_radio_flip_h.grid(row=0, column=1)
        self.buttons["radio_flip_h_0"] = param_radio_flip_h

        param_frame_flip.grid_forget()

        # param frame with angle for rotating images
        param_frame_rotate = tk.Frame(param_frame, bg=color_bg)
        param_frame_rotate.grid(row=0, column=0)
        self.param_frame_rotate = param_frame_rotate

        param_label_rotate = tk.Label(param_frame_rotate, text=get_ui_text("label_angle", self.lang), bg=color_bg)
        param_label_rotate.grid(row=0, column=0, padx=2, pady=5)
        self.labels["label_angle_0"] = param_label_rotate
        param_text_rotate = tk.Entry(param_frame_rotate, width=10, relief=tk.FLAT)
        param_text_rotate.grid(row=0, column=1, padx=5)
        self.param_rotate = param_text_rotate

        param_frame_rotate.grid_forget()

    def setup_input_output(self):
        # INPUT PATH
        input_label = tk.Label(self.main_frame, text=get_ui_text("label_input", self.lang), bg=color_bg)
        input_label.grid(row=3, column=0, padx=5, sticky="E")
        self.labels["label_input_0"] = input_label

        input_text_field = tk.Entry(self.main_frame, width=75, relief=tk.FLAT)
        input_text_field.grid(row=3, column=1, padx=5)
        self.input_text_field = input_text_field

        input_open_folder_button = tk.Button(self.main_frame, text=get_ui_text("button_folder", self.lang), padx=10,
                                             pady=5,
                                             fg=color_button_text, bg=color_button_bg,
                                             activebackground=color_button_text,
                                             command=lambda: self.input_select_dir(), relief=tk.FLAT)
        input_open_folder_button.grid(row=3, column=3, pady=2)
        self.buttons["button_folder_0"] = input_open_folder_button

        input_open_files_button = tk.Button(self.main_frame, text=get_ui_text("button_files", self.lang), padx=10,
                                            pady=5,
                                            fg=color_button_text, bg=color_button_bg,
                                            activebackground=color_button_text,
                                            command=lambda: self.input_select_files(), relief=tk.FLAT)
        input_open_files_button.grid(row=3, column=4, pady=2, padx=5)
        self.buttons["button_files_0"] = input_open_files_button

        # OUTPUT PATH
        output_label = tk.Label(self.main_frame, text=get_ui_text("label_output", self.lang), bg=color_bg)
        output_label.grid(row=5, column=0, padx=5, sticky="E")
        self.labels["label_output_0"] = output_label

        output_text_field = tk.Entry(self.main_frame, width=75, relief=tk.FLAT)
        output_text_field.grid(row=5, column=1, padx=5)
        self.output_text_field = output_text_field

        output_open_folder_button = tk.Button(self.main_frame, text=get_ui_text("button_folder", self.lang), padx=10,
                                              pady=5,
                                              fg=color_button_text, bg=color_button_bg,
                                              activebackground=color_button_text,
                                              command=lambda: self.output_select_dir(), relief=tk.FLAT)
        output_open_folder_button.grid(row=5, column=3, pady=2)
        self.buttons["button_folder_1"] = output_open_folder_button

        output_new_default_button = tk.Button(self.main_frame, text=get_ui_text("button_new_dest", self.lang),
                                              padx=2, pady=5, fg=color_button_text, bg=color_button_bg,
                                              activebackground=color_button_text,
                                              command=self.output_button_new_clicked, relief=tk.FLAT)
        output_new_default_button.grid(row=6, column=1, pady=2, padx=5, sticky="W")
        self.buttons["button_new_dest_0"] = output_new_default_button

        output_default_button = tk.Button(self.main_frame, text=get_ui_text("button_default", self.lang), padx=2,
                                          pady=5, fg=color_button_text, bg=color_button_bg,
                                          activebackground=color_button_text,
                                          command=self.output_button_clicked, relief=tk.FLAT)
        output_default_button.grid(row=6, column=1, pady=2, padx=50)
        self.buttons["button_default_0"] = output_default_button

    def setup_suffix(self):
        suffix_label = tk.Label(self.main_frame, text=get_ui_text("label_suffix", self.lang), bg=color_bg)
        suffix_label.grid(row=7, column=0, padx=5, sticky="E")
        self.labels["label_suffix_0"] = suffix_label

        suffix_text_field = tk.Entry(self.main_frame, width=25, relief=tk.FLAT)
        suffix_text_field.grid(row=7, column=1, padx=5, sticky="W")
        suffix_text_field.delete(0, tk.END)
        suffix_text_field.insert(0, self.suffix_default)
        self.suffix_text_field = suffix_text_field

        suffix_new_default_button = tk.Button(self.main_frame, text=get_ui_text("button_new_suffix", self.lang),
                                              padx=10,
                                              pady=5, fg=color_button_text, bg=color_button_bg,
                                              activebackground=color_button_text,
                                              command=self.suffix_button_new_clicked, relief=tk.FLAT)
        suffix_new_default_button.grid(row=7, column=1, pady=2, padx=5, sticky="E")
        self.buttons["button_new_suffix_0"] = suffix_new_default_button

        suffix_default_button = tk.Button(self.main_frame, text=get_ui_text("button_default", self.lang), padx=10,
                                          pady=5,
                                          fg=color_button_text, bg=color_button_bg, activebackground=color_button_text,
                                          command=self.suffix_button_clicked, relief=tk.FLAT)
        suffix_default_button.grid(row=7, column=3, pady=2, sticky="W")
        self.buttons["button_default_1"] = suffix_default_button

    def setup_preview_process(self):
        preview_live_var = tk.BooleanVar()
        preview_live_var.set(True)
        self.live_preview = preview_live_var
        preview_live_checkbox = tk.Checkbutton(self.main_frame, text=get_ui_text("button_live", self.lang),
                                               var=preview_live_var, bg=color_bg)
        preview_live_checkbox.grid(row=8, column=0, sticky="E")

        preview_button = tk.Button(self.main_frame, text=get_ui_text("button_preview", self.lang), padx=10, pady=5,
                                   fg=color_button_text, bg=color_button_preview_bg,
                                   activebackground=color_button_text,
                                   command=self.command_show_preview, relief=tk.FLAT)
        preview_button.grid(row=8, column=1, pady=5, padx=5, sticky="W")
        self.buttons["button_preview_0"] = preview_button

        process_button = tk.Button(self.main_frame, text=get_ui_text("button_process", self.lang), padx=10, pady=5,
                                   fg=color_button_text, bg=color_button_process_bg,
                                   activebackground=color_button_text,
                                   command=lambda: self.command_submit_button(), relief=tk.FLAT)
        process_button.grid(row=8, column=1, pady=5)
        self.buttons["button_process_0"] = process_button

    def setup_warnings(self):
        warning_overwrite = tk.Message(self.main_frame, text=get_ui_text("warning_overwrite", self.lang), width=450,
                                       bg=color_bg)
        warning_overwrite.grid(row=10, column=1, pady=10, sticky="W")
        self.labels["warning_overwrite_0"] = warning_overwrite

        warning_filename = tk.Message(self.main_frame, text=get_ui_text("warning_filename", self.lang), width=400,
                                      bg=color_bg)
        warning_filename.grid(row=11, column=1, pady=10, sticky="W")
        self.labels["warning_filename_0"] = warning_filename


if __name__ == "__main__":
    gui = GUI()
