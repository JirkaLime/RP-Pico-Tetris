# Nazev: SchemaBarvoBloko Prekladac
# Popis: Kod ktery podle schema barev vypise kod pro zobrazeni bloku s pouzitim daneho barevneho schema na Waveshare Pico LCD 1.3
# By: JirkaLime

# pip install pillow
from PIL import Image

alt = 1 # Alternativni zapis    [0 - OFF] [1 - ON]

# Konvertovani barev z RGB na Kompatibilni s displejem
def colour(R, G, B):
    rp = int(R * 31 / 255)
    if rp < 0: rp = 0
    r = rp * 8

    gp = int(G * 63 / 255)
    if gp < 0: gp = 0
    g = 0
    if gp & 1:  g += 8192
    if gp & 2:  g += 16384
    if gp & 4:  g += 32768
    if gp & 8:  g += 1
    if gp & 16: g += 2
    if gp & 32: g += 4

    bp = int(B * 31 / 255)
    if bp < 0: bp = 0
    b = bp * 256

    return r + g + b
# Konec

def process_image(file_path):
    img = Image.open(file_path)
    img = img.convert('RGB')  # Jen kdyby nahodou nebyl v RGB

    width, height = img.size
    if width != 3 or height != 23:
        raise ValueError("Error: Pouze img 3x23 pixelu!") # Kdyby to pouzival nekdo jiny nez ja tak at vi

    for section in range(8):
        x = 0
        y = section * 3

        pixels = [
            img.getpixel((x, y)),     # Pixel 1
            img.getpixel((x+1, y)),   # Pixel 2
            img.getpixel((x+2, y)),   # Pixel 3
            img.getpixel((x, y+1)),   # Pixel 4
            img.getpixel((x+1, y+1)), # Pixel 5
            img.getpixel((x+2, y+1))  # Pixel 6
        ]

        converted_colors = [colour(*pixel) for pixel in pixels]

        if (alt == 0):
            print(f"{section}: [{converted_colors[0]}, {converted_colors[3]}, {converted_colors[3]}, {converted_colors[1]}, {converted_colors[2]}, {converted_colors[2]}, {converted_colors[4]}, {converted_colors[4]}, {converted_colors[5]}], \n")

        else:
            print(f"{section}: np.array([[0, 0, 2, 2, {converted_colors[0]}], [2, 0, 8, 2, {converted_colors[3]}], [0, 2, 2, 8, {converted_colors[3]}], [2, 2, 8, 8, {converted_colors[1]}], [0, 10, 2, 2, {converted_colors[2]}], [10, 0, 2, 2, {converted_colors[2]}], [10, 2, 2, 8, {converted_colors[4]}], [2, 10, 8, 2, {converted_colors[4]}], [10, 10, 2, 2, {converted_colors[5]}]], dtype=np.uint16),\n")

# Vloz obrazek 3x23px
process_image('tetris_sch.png')

# Pozn.: Vse uz je opraveno kod funguje jak ma.
#        Mohl bych udelat upravu at kod funguje i pri obrazku vetsi jak 23px,
#        Ale jsem lenoch a takhle mi to staci.
#        + Pridal jsem alternativni efektivnejsi zapis.