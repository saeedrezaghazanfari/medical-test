import os, base64
from random import randint, choice


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


def random_code():
    char_list = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
    ]
    code = ''
    for _ in range(1, 10):
        code += choice(char_list)
    return code


def encode_str(password):
    encoded_value=base64.b64encode(password.encode("ascii","strict"))  
    return encoded_value


def decode_str(password):
    msg=base64.b64decode(password)
    decoded_value=msg.decode('ascii','strict')
    return decoded_value