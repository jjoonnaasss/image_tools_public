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

from PIL import Image, ImageEnhance

from src.values import *


class Params:
    def __init__(self, width=None, height=None, pos=None, left=None, top=None, perc=None, keep_aspect=None,
                 leq_geq=None, contrast=None, saturation=None, brightness=None, sharpness=None, flip_mode=None,
                 angle=None):
        if width is not None:
            self.width = int(width)
        if height is not None:
            self.height = int(height)
        if pos is not None:
            self.pos = pos
        if left is not None:
            self.left = int(left)
        if top is not None:
            self.top = int(top)
        if perc is not None:
            self.perc = int(perc)
        if keep_aspect is not None:
            self.keep_aspect = keep_aspect
        if leq_geq is not None:
            self.leq_geq = leq_geq
        if contrast is not None:
            self.contrast = float(contrast)
        if saturation is not None:
            self.saturation = float(saturation)
        if brightness is not None:
            self.brightness = float(brightness)
        if sharpness is not None:
            self.sharpness = float(sharpness)
        if flip_mode is not None:
            self.flip_mode = flip_mode
        if angle is not None:
            self.angle = angle


# returns all filenames in the given directory (only filenames without path to it)
def get_filenames(path):
    _, _, filenames = next(os.walk(path))
    return filenames


# crops the given image around a predefined position, params includes width, height of the resulting image and pos
def crop_img_predefined(img, params):
    img_width, img_height = img.size
    width = params.width if params.width < img_width else img_width
    height = params.height if params.height < img_height else img_height
    left, top = 0, 0

    if params.pos == 0:  # top left
        left = 0
        top = 0
    elif params.pos == 1:  # top middle
        left = (img_width - width) // 2
        top = 0
    elif params.pos == 2:  # top right
        left = img_width - width
        top = 0
    elif params.pos == 3:  # center left
        left = 0
        top = (img_height - height) // 2
    elif params.pos == 4:  # center middle
        left = (img_width - width) // 2
        top = (img_height - height) // 2
    elif params.pos == 5:  # center right
        left = img_width - width
        top = (img_height - height) // 2
    elif params.pos == 6:  # bottom left
        left = 0
        top = img_height - height
    elif params.pos == 7:  # bottom middle
        left = (img_width - width) // 2
        top = img_height - height
    elif params.pos == 8:  # bottom right
        left = img_width - width
        top = img_height - height

    right = left + width
    bottom = top + height

    return img.crop((left, top, right, bottom))


# crops the given image from a given position, params include left, top for the position and width, height of
# the resulting image
def crop_img_variable(img, params):
    img_width, img_height = img.size

    left = params.left if params.left < img_width else 0
    top = params.top if params.top < img_height else 0

    width = params.width if params.width + left < img_width else img_width - left
    height = params.height if params.height + top < img_height else img_height - top

    right = left + width
    bottom = top + height
    return img.crop((left, top, right, bottom))


# resizes the given image by a given percentage, params only include perc
def resize_img_percentage(img, params):
    factor = params.perc / 100
    img_width, img_height = img.size
    width, height = int(img_width * factor), int(img_height * factor)

    return img.resize((width, height))


# resizes the given image to specific dimensions, params include the dimensions (width, height), keep_aspect and leq_geq
def resize_img_dimensions(img, params):
    if not params.keep_aspect:
        return img.resize((params.width, params.height))

    img_width, img_height = img.size
    width, height = params.width, params.height

    if not params.leq_geq:
        factor = min(width / img_width, height / img_height)
    else:
        factor = max(width / img_width, height / img_height)
    width, height = int(img_width * factor), int(img_height * factor)

    return img.resize((width, height))


# enhances the given image, params include the values for the contrast, saturation, brightness and sharpness filters
def enhance_img(img, params):
    after_contrast = ImageEnhance.Contrast(img).enhance(params.contrast)
    after_saturation = ImageEnhance.Color(after_contrast).enhance(params.saturation)
    after_brightness = ImageEnhance.Brightness(after_saturation).enhance(params.brightness)
    after_sharpness = ImageEnhance.Sharpness(after_brightness).enhance(params.sharpness)

    return after_sharpness


# converts the given image to greyscale, params include nothing
def greyscale_img(img, params):
    return img.convert("L")


# flips the given image either vertically or horizontally, params include an int for this decision
def flip_img(img, params):
    return img.transpose(Image.FLIP_TOP_BOTTOM if params.flip_mode else Image.FLIP_LEFT_RIGHT)


# rotates the given image, params include the rotation angle
def rotate_img(img, params):
    return img.rotate(params.angle, expand=True)


# processes all images in the given path, passes the params to the wanted tool and saves the new images into
# the output directory
def process_imgs(path, params, tool, out_dir, lang, suffix):
    counter = 0
    path = r"{}".format(path)
    if os.path.isfile(path):
        files = [os.path.split(path)[1]]
        path = os.path.split(path)[0]
    else:
        files = get_filenames(path)

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    tool = get_tool_method(tool, lang)

    for file in files:
        try:
            img = Image.open(os.path.join(path, file))
            img_cropped = tool(img, params)
            img.close()

            if not img_cropped:
                continue

            name, extension = file.rsplit(".", 1)
            img_cropped.save(os.path.join(out_dir, name + suffix + "." + extension))
            counter += 1
            img_cropped.close()

        except Exception as e:
            print("error processing image:", e)

    print("Processed", counter, "images.")
    return counter


# returns a processed image instance for previewing
def preview_img(path, params, tool, lang, window, new_window):
    path = r"{}".format(path)
    if os.path.isfile(path):
        files = [os.path.split(path)[1]]
        path = os.path.split(path)[0]
    else:
        files = get_filenames(path)

    tool = get_tool_method(tool, lang)

    try:
        img = Image.open(os.path.join(path, files[0]))
        img = tool(img, params)
        if new_window:  # use standard size if the window was newly created, to prevent the (200, 200) bug
            params = Params(width=dimensions_preview[0], height=dimensions_preview[1], keep_aspect=True, leq_geq=0)
        else:
            params = Params(width=window.winfo_width(), height=window.winfo_height(), keep_aspect=True, leq_geq=0)
        return resize_img_dimensions(img, params)

    except Exception as e:
        print("error previewing image:", e)


# takes the name of the wanted tool and the current app language to return the wanted tool method
def get_tool_method(val, lang):
    if val == get_ui_text("tool_options", lang)[0]:
        return crop_img_predefined
    elif val == get_ui_text("tool_options", lang)[1]:
        return crop_img_variable
    elif val == get_ui_text("tool_options", lang)[2]:
        return resize_img_percentage
    elif val == get_ui_text("tool_options", lang)[3]:
        return resize_img_dimensions
    elif val == get_ui_text("tool_options", lang)[4]:
        return enhance_img
    elif val == get_ui_text("tool_options", lang)[5]:
        return greyscale_img
    elif val == get_ui_text("tool_options", lang)[6]:
        return flip_img
    elif val == get_ui_text("tool_options", lang)[7]:
        return rotate_img

# process_imgs(r"C:\Users\Jonas\Desktop\imgs", Params(200, 200), crop_img_center, "_crop", False)
