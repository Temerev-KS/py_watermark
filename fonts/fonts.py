from PIL import ImageFont
from pathlib import Path
from fontTools import ttLib


class FontsLibrary:
    def __init__(self):
        self.fonts_list = None
        self.load_fonts_library()
    
    def load_fonts_library(self):
        # for found font in files create font object and store in some variable
        self.fonts_list = dict()
        fonts_folder = Path("fonts")
        for font_file in fonts_folder.rglob('*.ttf'):
            # print(font_file.resolve())
            self.fonts_list[self.read_font_name(font_file)] = ImageFont.truetype(font=font_file.resolve().__str__())
    
    @staticmethod
    def read_font_name(font_file_path) -> str:
        # Read the font name from the font's file names table
        font_file = ttLib.TTFont(font_file_path)
        font_name_str = ""
        for record in font_file['name'].names:
            # determine what encoding table to use based
            if b'\x00' in record.string:
                name_str = record.string.decode('utf-16-be')
            else:
                name_str = record.string.decode('utf-8')
            # locate font name based on specifier name id (4)
            if record.nameID == 4 and not font_name_str:
                font_name_str = name_str
        return font_name_str
    
    def get_fonts_list(self):
        return self.fonts_list


if __name__ == '__main__':
    pass
