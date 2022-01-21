from PIL import Image
from fonts import FontsLibrary


def func():
    img = Image.open('img/dogo.jpeg')
    img = Image.open('img/dogo.jpeg')
    print(img.format)
    print(img.size)
    print(img.mode)
    img.save('test.jpg')
    
    
if __name__ == '__main__':
    # func()
    pil_fonts = FontsLibrary()
    print(pil_fonts.get_fonts_names_tuple())
    for key in pil_fonts.get_fonts_names_tuple():
        print(key)
    