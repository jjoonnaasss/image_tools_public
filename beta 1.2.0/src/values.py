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
             "label_percentage": "Size > 0 (%):", "label_aspect": "Keep aspect ratio",
             "label_leq_geq_0": "Resulting dimensions", "label_leq_geq_1": "given dimensions",
             "label_contrast": "Contrast >= 0:", "label_saturation": "Saturation >= 0:",
             "label_brightness": "Brightness >= 0:", "label_sharpness": "Sharpness >= 0:",
             "label_enhance_info": "1.0 means no change", "label_input": "Select the image source:",
             "label_output": "Select the destination folder:", "label_suffix": "Set suffix:",
             "label_angle": "Angle (degrees):", "label_watermark": "Select watermark image:"}

menu_EN = {"menu_settings": "Settings", "menu_lang": "Language", "menu_popups": "Pop-ups",
           "menu_popups_info": "Info after processing", "menu_help": "Help", "menu_about": "About",
           "menu_preview": "Preview", "menu_preview_disable": "Keep live preview disabled"}

filedialog_EN = {"filedialog_folder": "Select a folder.", "filedialog_files": "Select one or multiple file(s).",
                 "filedialog_file": "Select a file.", "filedialog_types": "Images"}

errors_EN = {"error": "Error!", "error_io": "Image source and destination folder may not be empty!",
             "error_input": "The image source has to be a path to a folder or one or multiple images!",
             "error_output": "The destination folder has to be a path to a folder!",
             "error_params_num": "Tool parameters have to be whole or decimal numbers!",
             "error_params_zero": "Tool parameters have to be greater than (equal to) zero!",
             "error_suffix": "The suffix may not contain the following characters: \\ /:*?\"<>|",
             "error_filename": "The names of the source files may not contain commas!",
             "error_watermark_file": "The watermark image has to be a valid file path!"}

warnings_EN = {
    "warning_overwrite": "Warning: Using the same folder as source and destination with an empty suffix and the same file type will overwrite the original image!",
    "warning_filename": "Warning: Filenames including commas are not supported!",
    "warning_move": "Hint: Please disable the live preview in order to move the main window without problems!"}

buttons_EN = {"button_enhance": "Set all to 1.0", "button_folder": "Open folder", "button_files": "Open file(s)",
              "button_file": "Open file", "button_output": "Set as default destination", "button_default": "Default",
              "button_new_dest": "Save as new default destination", "button_new_suffix": "Save as new default suffix",
              "button_preview": "Preview", "button_live": "Live", "button_process": "Process images",
              "radio_flip_v": "flip vertically", "radio_flip_h": "flip horizontally",
              "radio_position_pre": "Predefined position", "radio_position_var": "Variable position"}

selection_EN = {"tool_options": ["Crop images", "Resize by percentage",
                                 "Resize to specific dimensions",
                                 "Enhance images, e.g. per contrast", "Convert to greyscale", "Flip images",
                                 "Rotate images (counterclockwise)", "Apply watermark"]}

help_EN = {"help_tools": {
    "Tool: Crop images": "This tool crops the image into a rectangle of the given width and height. You can choose one of two position options to determine from which part of the image the rectangle is taken.\nThe first option lets you choose one of nine predefined ones.\nThe second option has the values \"Left\" and \"Top\", which define the position of the rectangle's upper left corner in the image.\n(Pixel-) coordinates always start in the upper left corner of the image with (0, 0). The x-coordinate (\"Left\") increases, the further right you are. The y-coordinate (\"Top\") increases, the further down you are.",
    "Tool: Resize by percentage": "This tool scales the image to have the given percentage of its original size.",
    "Tool: Resize to specific dimensions": "This tool scales the image to have the given width and height.\nIf \"Keep aspect ratio\" is not selected, the resulting image will always exactly match the given width and height.\nIf it is selected however, it will only match width and height, if they suit the original image's aspect ratio. Otherwise, one dimension will match the given one and the other will either be smaller (\"<=\") or bigger (\">=\") than the given one.",
    "Tool: Enhance images, e.g. per contrast": "This tool changes the image's contrast, saturation, brightness and sharpness by the given factors.\nA factor of 1.0 means the image's according attribute is not altered.",
    "Tool: Convert to greyscale": "This tool converts the image into a greyscale image.",
    "Tool: Flip images": "This tool flips the image either vertically or horizontally.",
    "Tool: Rotate images (counterclockwise)": "This tool rotates the image by the given angle. Positive values result in counterclockwise rotation and negative values in clockwise rotation.",
    "Tool: Apply watermark": "This tool pastes one image as a watermark onto other images."}}

about_EN = {
    "about_it": ["Image Tools", "Version: v1.2.0-beta", "Published: February 8, 2021", "Developed by: Jonas Wombacher",
                 "https://github.com/jjoonnaasss/image_tools_public/releases", "", "Open website?"],
    "about_url": "https://github.com/jjoonnaasss/image_tools_public/releases"}

misc_EN = {"default_out": "processed", "default_suffix": "_processed", "info_result": "Number of processed images:",
           "title_preview": "Image Tools Preview"}

EN = {**labels_EN, **menu_EN, **filedialog_EN, **errors_EN, **warnings_EN, **buttons_EN, **selection_EN, **help_EN,
      **about_EN, **misc_EN}

labels_DE = {"label_tool": "Werkzeug auswählen:", "label_width": "Breite (Pixel):", "label_height": "Höhe (Pixel)",
             "label_pos": "Position:", "label_left": "Links (Pixel):", "label_top": "Oben (Pixel):",
             "label_percentage": "Größe > 0 (%):", "label_aspect": "Seitenverhältnis beibehalten",
             "label_leq_geq_0": "Ergebnis-Dimensionen", "label_leq_geq_1": "angegebene Dimensionen",
             "label_contrast": "Kontrast >= 0:", "label_saturation": "Sättigung >= 0:",
             "label_brightness": "Helligkeit >= 0:", "label_sharpness": "Schärfe >= 0:",
             "label_enhance_info": "1.0 heißt keine Änderung", "label_input": "Bild-Quelle auswählen:",
             "label_output": "Ziel-Ordner auswählen", "label_suffix": "Suffix wählen:", "label_angle": "Winkel (Grad):",
             "label_watermark": "Wasserzeichen-Bild auswählen:"}

menu_DE = {"menu_settings": "Einstellungen", "menu_lang": "Sprache", "menu_popups": "Pop-ups",
           "menu_popups_info": "Info nach Bearbeitung", "menu_help": "Hilfe", "menu_about": "Über",
           "menu_preview": "Vorschau", "menu_preview_disable": "Live-Vorschau dauerhaft deaktivieren"}

filedialog_DE = {"filedialog_folder": "Ordner auswählen.", "filedialog_files": "Eine oder mehrere Datei(en) auswählen.",
                 "filedialog_file": "Datei auswählen.", "filedialog_types": "Bilder"}

errors_DE = {"error": "Fehler!", "error_io": "Die Bild-Quelle und der Ziel-Ordner dürfen nicht leer sein!",
             "error_input": "Die Bild-Quelle muss ein Pfad zu einem Ordner oder einem oder mehreren Bildern sein!",
             "error_output": "Der Ziel-Ordner muss ein Pfad zu einem Ordner sein!",
             "error_params_num": "Parameter müssen ganze Zahlen oder Dezimalzahlen sein!",
             "error_params_zero": "Parameter müssen größer (gleich) Null sein!",
             "error_suffix": "Das Suffix darf folgende Zeichen nicht enthalten: \\ /:*?\"<>|",
             "error_filename": "Die Namen der Quell-Dateien dürfen keine Kommata enthalten!",
             "error_watermark_file": "Das Wasserzeichen-Bild muss ein gültiger Dateipfad sein!"}

warnings_DE = {
    "warning_overwrite": "Warnung: Bei Benutzen des selben Ordners als Quelle und Ziel mit einem leeren Suffix und gleichem Dateityp wird das originale Bild überschrieben!",
    "warning_filename": "Warnung: Dateinamen, die Kommata enthalten, werden nicht unterstützt!",
    "warning_move": "Hinweis: Live-Preview bitte deaktivieren, um das Hauptfenster problemlos zu bewegen!"}

buttons_DE = {"button_enhance": "Alle auf 1.0 setzen", "button_folder": "Ordner öffnen",
              "button_files": "Datei(en) öffnen", "button_file": "Datei öffnen", "button_default": "Standardwert",
              "button_new_dest": "Als neues Standardziel speichern",
              "button_new_suffix": "Als neues Standard-Suffix speichern", "button_preview": "Vorschau",
              "button_live": "Live", "button_process": "Bilder bearbeiten", "radio_flip_v": "Vertikal spiegeln",
              "radio_flip_h": "Horizontal spiegeln", "radio_position_pre": "Vordefinierte Position",
              "radio_position_var": "Variable Position"}

selection_DE = {"tool_options": ["Bilder zuschneiden",
                                 "Größe nach Prozentwert ändern",
                                 "Größe auf feste Abmessungen ändern",
                                 "Bilder verbessern, z.B. per Kontrast", "Zu Graustufen konvertieren",
                                 "Bilder spiegeln", "Bilder drehen (gegen den Uhrzeigersinn)",
                                 "Wasserzeichen einfügen"]}

help_DE = {"help_tools": {
    "Werkzeug: Bilder zuschneiden": "Dieses Werkzeug schneidet ein Rechteck mit der gegebenen Breite und Höhe aus dem Bild aus. Man kann eine von zwei Methoden wählen, um festzulegen, aus welchem Teil des Bilder das Rechteck entnommen wird.\nBei der ersten Option kann man eine von neun vordefinierten Positionen wählen.\nBei der zweiten Option gibt es die Werte \"Links\" und \"Oben\", welche die Position der linken oberen Ecke des Rechtecks im Bild festlegen.\n(Pixel-) Koordinaten beginnen immer in der linken oberen Ecke des Bilder mit (0, 0). Die x-Koordinate (\"Links\") steigt, je weiter rechts man sich befindet. Die y-Koordinate (\"Oben\") steigt, je weiter unten man sich befindet.",
    "Werkzeug: Größe nach Prozentwert ändern": "Dieses Werkzeug ändert die Größe des Bildes auf den gegebenen Prozentsatz seiner ursprünglichen Größe.",
    "Werkzeug: Größe auf feste Abmessungen ändern": "Dieses Werkzeug ändert die Größe des Bildes auf die gegebene Breite und Höhe.\nWenn \"Seitenverhältnis beibehalten\" nicht ausgewählt ist, wird das resultierende Bild immer genau mit gegebener Breite und Höhe übereinstimmen.\nWenn es aber ausgewählt ist, wird das Bild nur mit Breite und Höhe übereinstimmen, wenn diese zum ursprünglichen Seitenverhältnis passen. Andernfalls wird eine Dimension mit der angegebenen übereinstimmen, während die andere entweder kleiner (\"<=\") oder größer (\">=\") als die angegebene sein wird.",
    "Werkzeug: Bilder verbessern, z.B. per Kontrast": "Dieses Werkzeug verändert Kontrast, Sättigung, Helligkeit und Schärfe des Bildes um die gegebenen Faktoren.\nEin Faktor von 1.0 bedeutet, dass das entsprechende Attribut des Bildes nicht verändert wird.",
    "Werkzeug: Zu Graustufen konvertieren": "Dieses Werkzeug konvertiert das Bild zu einem Graustufenbild.",
    "Werkzeug: Bilder spiegeln": "Dieses Werkzeug spiegelt das Bild entweder an seiner vertikalen oder horizontalen Achse.",
    "Werkzeug: Bilder drehen (gegen den Uhrzeigersinn)": "Dieses Werkzeug dreht das Bild um den gegebenen Winkel. Positive Werte ergeben eine Rotation gegen den Uhrzeigersinn und negative Werte eine Rotation im Uhrzeigersinn.",
    "Werkzeug: Wasserzeichen einfügen": "Dieses Werkzeug kopiert ein Bild als Wasserzeichen auf andere Bilder."}}

about_DE = {
    "about_it": ["Image Tools", "Version: v1.2.0-beta", "Veröffentlicht: 08.02.2021", "Entwickelt von: Jonas Wombacher",
                 "https://github.com/jjoonnaasss/image_tools_public/releases", "", "Website öffnen?"],
    "about_url": "https://github.com/jjoonnaasss/image_tools_public/releases"}

misc_DE = {"default_out": "bearbeitet", "default_suffix": "_bearbeitet",
           "info_result": "Anzahl der bearbeiteten Bilder:", "title_preview": "Image Tools Vorschau"}

DE = {**labels_DE, **menu_DE, **filedialog_DE, **errors_DE, **warnings_DE, **buttons_DE, **selection_DE, **help_DE,
      **about_DE, **misc_DE}


def get_ui_text(val, lang):
    if lang == "EN":
        return EN[val]
    else:
        return DE[val]


# window dimensions
dimensions_root = (850, 700)
dimensions_preview = (500, 500)
dimensions_help = (400, 500)

# window distance
distance_root_preview = 50

# after durations
live_preview_clock = 500

# widget dimensions
tool_menu_width = 60
scrollbar_width = 17

# colors
color_bg = "#ABB2B9"  # grey
color_button_text = "#CCD1D1"  # light grey
color_button_bg = "#424949"  # dark grey
color_button_preview_bg = "#7D6608"  # yellow-brown
color_button_process_bg = "#196F3D"  # dark green
