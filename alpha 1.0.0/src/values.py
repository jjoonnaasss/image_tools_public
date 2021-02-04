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

labels_EN = {"label_tool": "Select a tool:", "label_width": "Width (pixels):", "label_height": "Height (pixels):",
             "label_pos": "Position:", "label_left": "Left (pixels):", "label_top": "Top (pixels):",
             "label_percentage": "Size > 0 (%):", "label_contrast": "Contrast >= 0:",
             "label_saturation": "Saturation >= 0:", "label_brightness": "Brightness >= 0:",
             "label_sharpness": "Sharpness >= 0:", "label_enhance_info": "1.0 means no change",
             "label_input": "Select the image source:", "label_output": "Select the destination folder:",
             "label_suffix": "Set suffix:", "label_angle": "Angle (degrees):"}

menu_EN = {"menu_settings": "Settings", "menu_lang": "Language"}

filedialog_EN = {"filedialog_folder": "Select a folder.", "filedialog_files": "Select one or multiple file(s).",
                 "filedialog_types": "Images"}

errors_EN = {"error_io": "Image source and destination folder may not be empty!",
             "error_input": "The image source has to be a path to a folder or one or multiple images!",
             "error_output": "The destination folder has to be a path to a folder!",
             "error_params_num": "Tool parameters have to be whole or decimal numbers!",
             "error_params_zero": "Tool parameters have to be greater than (equal to) zero!",
             "error_suffix": "The suffix may not contain the following characters: \\ /:*?\"<>|",
             "error_filename": "The names of the source files may not contain commas!"}

warnings_EN = {
    "warning_overwrite": "Warning: Using the same folder as source and destination with an empty suffix and the same file type will overwrite the original image!",
    "warning_filename": "Warning: Filenames including commas are not supported!"}

buttons_EN = {"button_folder": "Open folder", "button_files": "Open file(s)", "button_suffix": "Default",
              "button_new_suffix": "Save as new default", "button_process": "Process images",
              "radio_flip_v": "flip vertically", "radio_flip_h": "flip horizontally"}

selection_EN = {"tool_options": ["Crop at predefined position", "Crop at variable position", "Resize by percentage",
                                 "Resize to specific dimensions (keeps aspect ratio)",
                                 "Enhance images, e.g. per contrast", "Convert to greyscale", "Flip images",
                                 "Rotate images (counterclockwise)"]}

misc_EN = {"default_out": "processed", "default_suffix": "_processed", "info_result": "Number of processed images:"}

EN = {**labels_EN, **menu_EN, **filedialog_EN, **errors_EN, **warnings_EN, **buttons_EN, **selection_EN, **misc_EN}

labels_DE = {"label_tool": "Aktion auswählen:", "label_width": "Breite (Pixel):", "label_height": "Höhe (Pixel)",
             "label_pos": "Position:", "label_left": "Links (Pixel):", "label_top": "Oben (Pixel):",
             "label_percentage": "Größe > 0 (%):", "label_contrast": "Kontrast >= 0:",
             "label_saturation": "Sättigung >= 0:", "label_brightness": "Helligkeit >= 0:",
             "label_sharpness": "Schärfe >= 0:", "label_enhance_info": "1.0 heißt keine Änderung",
             "label_input": "Bild-Quelle auswählen:", "label_output": "Ziel-Ordner auswählen",
             "label_suffix": "Suffix wählen:", "label_angle": "Winkel (Grad):"}

menu_DE = {"menu_settings": "Einstellungen", "menu_lang": "Sprache"}

filedialog_DE = {"filedialog_folder": "Ordner auswählen.", "filedialog_files": "Eine oder mehrere Datei(en) auswählen.",
                 "filedialog_types": "Bilder"}

errors_DE = {"error_io": "Die Bild-Quelle und der Ziel-Ordner dürfen nicht leer sein!",
             "error_input": "Die Bild-Quelle muss ein Pfad zu einem Ordner oder einem oder mehreren Bildern sein!",
             "error_output": "Der Ziel-Ordner muss ein Pfad zu einem Ordner sein!",
             "error_params_num": "Parameter müssen ganze Zahlen oder Dezimalzahlen sein!",
             "error_params_zero": "Parameter müssen größer (gleich) Null sein!",
             "error_suffix": "Das Suffix darf folgende Zeichen nicht enthalten: \\ /:*?\"<>|",
             "error_filename": "Die Namen der Quell-Dateien dürfen keine Kommata enthalten!"}

warnings_DE = {
    "warning_overwrite": "Warnung: Bei Benutzen des selben Ordners als Quelle und Ziel mit einem leeren Suffix und gleichem Dateityp wird das originale Bild überschrieben!",
    "warning_filename": "Warnung: Dateinamen, die Kommata enthalten, werden nicht unterstützt!"}

buttons_DE = {"button_folder": "Ordner öffnen", "button_files": "Datei(en) öffnen", "button_suffix": "Standardwert",
              "button_new_suffix": "Als neuen Standardwert speichern", "button_process": "Bilder bearbeiten",
              "radio_flip_v": "Vertikal spiegeln", "radio_flip_h": "Horizontal spiegeln"}

selection_DE = {"tool_options": ["An vordefinierter Position ausschneiden", "An variabler Position ausschneiden",
                                 "Größe nach Prozentwert ändern",
                                 "Größe auf feste Abmessungen ändern (hält Seitenverhältnis bei)",
                                 "Bilder verbessern, z.B. per Kontrast", "Zu Graustufen konvertieren",
                                 "Bilder spiegeln", "Bilder drehen (gegen den Uhrzeigersinn)"]}

misc_DE = {"default_out": "bearbeitet", "default_suffix": "_bearbeitet",
           "info_result": "Anzahl der bearbeiteten Bilder:"}

DE = {**labels_DE, **menu_DE, **filedialog_DE, **errors_DE, **warnings_DE, **buttons_DE, **selection_DE, **misc_DE}


def get_ui_text(val, lang):
    if lang == "EN":
        return EN[val]
    else:
        return DE[val]


# widget dimensions
tool_menu_width = 60
