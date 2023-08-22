import hashlib
import random
import binascii
import qrcode

from stegano import lsb
import psycopg2
from io import BytesIO
import base64
import io

from PIL import Image

# DNA base pairs (A, T, C, G)
BASE_PAIRS = {
    '00': 'A',
    '01': 'T',
    '10': 'C',
    '11': 'G'
}

def add_user(username, passwordHash, randomVal, secID, qrImg, stegQRImg):
    conn = None 
    u = username
    ph = passwordHash
    rval = randomVal
    secid = secID
    qrimg = qrImg
    stegimg = stegQRImg
    insert_command = "INSERT INTO users(username, passwordhash, randomval, secid, qrimage, sqrimage) VALUES (%s,%s,%s,%s,%s,%s);"
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="postgres"
        )
        cur = conn.cursor()
        cur.execute(insert_command, (u, ph, rval, secid, qrimg, stegimg))
        cur.close()
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return "done"


def get_user(uname):
    conn = None
    data_rows = []
    u = uname
    select_command = " SELECT * FROM users where username = '{}';".format(u)
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="postgres"
        )
        cur = conn.cursor()
        cur.execute(select_command, (u))
        rows = cur.fetchall()
        data_rows = rows
        cur.close()
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return data_rows

def type1(s):
    """
    Type 1 function returns the first half and second half
    """
    mid = len(s) // 2
    first_half = s[:mid]
    second_half = s[mid:]
    return first_half, second_half

def reverse_type1(first_half, second_half):
    """
    Reversed Type 1 function combines two halves into a single string
    """
    combined_string = first_half + second_half
    return combined_string
    
def type2(s):
    """
    Type 2 function returns letters in odd position as one half and even porisiton as another half
    """
    odd_position = ''
    even_position = ''

    for i in range(len(s)):
        if i % 2 == 0:
            even_position += s[i]
        else:
            odd_position += s[i]

    return odd_position, even_position

def reverse_type2(odd_position, even_position):
    """
    Reversed Type 2 function combines odd-position letters and even-position letters
    """
    combined_string = ''
    max_length = max(len(odd_position), len(even_position))

    for i in range(max_length):
        if i < len(odd_position):
            combined_string += odd_position[i]
        if i < len(even_position):
            combined_string += even_position[i]

    return combined_string

def type3(s):
    """
    Type 3 function returns second half as first half and first half as second half. 
    """
    mid = len(s) // 2
    first_half = s[:mid]
    second_half = s[mid:]
    return second_half, first_half

def reverse_type3(second_half, first_half):
    """
    Reversed Type 3 function swaps the first and second halves
    """
    combined_string = second_half + first_half
    return combined_string

def random_hash_splitter(s):
    """
    Generate Two hashes from the given hash strings
    """
    hash = hashlib.sha3_256(s.encode('utf-8')).hexdigest()
    rand_num = random.randint(1, 3)
    if (rand_num == 1):
        h1, h2 = type1(hash)
    elif (rand_num == 2):
        h1, h2 = type2(hash)
    else:
        h1, h2 = type3(hash)
    return hash, str(rand_num), h1, h2

def re_get(v, H1, H2):
    if v == 1:
        h = reverse_type1(H1, H2)
    elif v == 2:
        h = reverse_type2(H1, H2)
    else:
        h = reverse_type3(H1, H2)
    return h

# Reverse of BASE_PAIRS
REVERSE_BASE_PAIRS = {v: k for k, v in BASE_PAIRS.items()}

def string_to_binary(input_string):
    binary_string = ''.join(format(ord(char), '08b') for char in input_string)
    return binary_string

def binary_to_string(input_binary):
    # Pad the binary string to ensure it has a multiple of 8 digits
    padded_binary = input_binary.zfill((len(input_binary) + 7) // 8 * 8)

    # Convert binary to string
    string_result = ''.join(chr(int(padded_binary[i:i+8], 2)) for i in range(0, len(padded_binary), 8))
    return string_result

def binary_to_dna(binary_data):
    # Convert binary data to DNA sequence
    dna_sequence = ''
    for i in range(0, len(binary_data), 2):
        dna_sequence += BASE_PAIRS[binary_data[i:i+2]]
    return dna_sequence

def dna_to_binary(dna_sequence):
    # Convert DNA sequence to binary data
    binary_data = ''
    for base in dna_sequence:
        binary_data += REVERSE_BASE_PAIRS[base]
    return binary_data

def dna_encrypt(text):
    binary_data = string_to_binary(text)
    dna_sequence = binary_to_dna(binary_data)
    return dna_sequence

def dna_decrypt(dna_sequence):
    binary_data = dna_to_binary(dna_sequence)
    text = binary_to_string(binary_data)
    return text

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    return img

def bytes_to_image(byte_data):
    img = Image.open(io.BytesIO(byte_data))
    return img

def hide_message(image_path, secret_message):
    img = image_path.convert('RGB')
    encoded_image = lsb.hide(img, secret_message)
    return encoded_image

def reveal_message(encoded_image):
    extracted_msg = lsb.reveal(encoded_image)
    return extracted_msg

def image_to_bytes(image_object):
    # Create an in-memory buffer to store the image bytes
    buffer = BytesIO()
    # Save the image to the buffer in PNG format (you can choose a different format if needed)
    image_object.save(buffer, format='PNG')
    # Get the bytes data from the buffer
    image_bytes = buffer.getvalue()
    # Close the buffer
    buffer.close()
    return image_bytes