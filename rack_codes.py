import json
import numpy as np
import os
import qrcode
from fpdf import FPDF
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def create_qrcode(data, fname):
    equipment_filepath = os.path.join(os.getcwd(), "rack_codes")
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=4,
        border=10,
    )
    # Add file to fill data
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(os.path.join(equipment_filepath, fname))
    img2 = Image.open(os.path.join(equipment_filepath, fname))
    arial_path = os.path.join(os.getcwd(), "CMS", "bin", "fonts", "arial.ttf")
    draw = ImageDraw.Draw(img2)
    font = ImageFont.truetype(arial_path, 15)
    location = data.split(" ")[0]
    box = data.split(" ")[1].replace("box_", "")
    draw.text((50, 145), f"Location: {location}\n     Box: {box}", (0), font=font)
    img2.save(os.path.join(equipment_filepath, fname))

def print_codes():
    pdf = FPDF()
    page_index = 1
    imagelist = sorted([os.path.join(os.getcwd(), "rack_codes", i) for i in os.listdir(os.path.join(os.getcwd(), "rack_codes"))])
    last_page = int(np.ceil(len(imagelist)/10))
    pdf.add_page()
    n = 0
    i = 0
    for image in imagelist:
        if n == 10:
            pdf.add_page()
            n = 0
            i = 0
        if i%2 == 0:
            pdf.image(image, 25, 16 + 26.5*i, 55, 50)
            n += 1
            i += 1
        elif i%2 == 1:
            if i == 1:
                pdf.image(image, 135,  16 + 26.5*(i-1), 55, 50)
                n += 1
                i += 1
            else:
                pdf.image(image, 135,  16 + 26.5*(i-1), 55, 50)
                n += 1
                i += 1
    p_p = os.path.join(os.getcwd(), f"rack_qr_codes.pdf")
    pdf.output(p_p, "F")

def main():
    path = os.path.join(os.getcwd(), "racks.json")
    with open(path, 'r') as f:
        data = json.load(f)
    for i in data:
        if data[i]:
            for box in data[i]:
                create_qrcode(data=f"{i} {box}", fname=f"{i}_{box}.png")

if __name__ == "__main__":
    print_codes()
