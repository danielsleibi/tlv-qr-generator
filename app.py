# -*- coding: utf-8 -*-
import qrcode
import tkinter as tk
from tkinter import filedialog

def open_file_dialog():
    root = tk.Tk()  # Create the root window
    root.withdraw()  # Hide the root window

    # Open the file picker dialog
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("All files", "*.*"), ("JSON files", "*.json")]
    )

    if file_path:
        print(f"Selected file: {file_path}")
    else:
        print("No file selected")
    return file_path


def crc16(data: bytes, poly: int = 0x1021, init_val: int = 0xFFFF) -> int:
    crc = init_val
    for byte in data:
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ poly
            else:
                crc <<= 1
            crc &= 0xFFFF  # Ensure CRC is 16-bit
    return crc


def has_sub(field):
    field_int = int(field)
    if field_int >= 2 and field_int <= 51:
        return True
    
    if field_int == 62:
        return True
    
    if field_int == 64:
        return True
    
    if field_int >= 65 and field_int <= 79:
        return True
    
    if field_int >= 80 and field_int <= 99:
        return True

    return False


def decode_sub(k, v):
    tlv = decode(v, is_sub=True)
    return f'{k}{str(len(tlv)).zfill(2)}{tlv}'


def decode(json, is_sub=False):
    tlv = ''
    for k, v in json.items():
        tlv += decode_sub(k, v) if has_sub(k) and not is_sub else f'{k}{str(len(v)).zfill(2)}{v}'
    return tlv

def add_crc(data):
    data += '6304'
    return data + f'{crc16(data.encode('utf-8')):04X}'

def gen_qr(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    img.save("qrcode.png")

    img.show()

if __name__ == "__main__":
    import json
    import pyperclip

 
    file_path = open_file_dialog()

    with open(file_path, 'r') as file:
        data = decode(json.load(file))
        data = add_crc(data)
        gen_qr(data)

        print(data)
        pyperclip.copy(data)
        print('Copied to clipboard!!!')