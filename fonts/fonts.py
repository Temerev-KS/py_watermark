import sys
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
    def read_font_name(some_font_file):
        font_specifier_name_id = 4
        
        def short_name(font):
            """Get the short name from the font's names table"""
            name = ""
            for record in font['name'].names:
                if b'\x00' in record.string:
                    name_str = record.string.decode('utf-16-be')
                else:
                    name_str = record.string.decode('utf-8')
                if record.nameID == font_specifier_name_id and not name:
                    name = name_str
            return name
        tt = ttLib.TTFont(some_font_file)
        font_name = short_name(tt)
        return font_name
    
    def get_fonts_list(self):
        return self.fonts_list


if __name__ == '__main__':
    pass
