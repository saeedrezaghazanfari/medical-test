import os
from random import randint


# before function File storage
def get_filename_ext_rand(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    random1 = randint(100, 999)
    random2 = randint(100, 999)
    output = f'{random1}{random2}'
    return ext.lower(), output


# ######### for users imgs ######### #
def expriment_result_image_pat(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"exprements/{final_name}"