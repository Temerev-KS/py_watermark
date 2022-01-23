from PIL import ImageFont
from pathlib import Path
from fontTools import ttLib


class FontsLibrary:
    """Responsible for reading ttf files, getting names of the fonts, storing them for future retrieval.
    Can return "list" (tuple) of font names. Or using font name can create and return an ImageFont object"""
    def __init__(self):
        self._fonts = None
        self.load_fonts_library()
    
    def load_fonts_library(self):
        """Crawls fonts folder, if .ttf font file found -
        processes it and stores it in dictionary {'Font name'; 'path to font file'}"""
        fonts_folder = Path("fonts")
        self._fonts = dict()
        
        def read_font_name(font_file_path) -> str:
            # Read the font name from the font's file names table
            font_file_ttf = ttLib.TTFont(font_file_path)  # Open font file
            font_name_str = ""
            for record in font_file_ttf['name'].names:
                # determine what encoding table to use based
                if b'\x00' in record.string:
                    name_str = record.string.decode('utf-16-be')
                else:
                    name_str = record.string.decode('utf-8')
                # locate font name based on specifier name id (4)
                if record.nameID == 4 and not font_name_str:
                    font_name_str = name_str
            return font_name_str
        
        for font_file in fonts_folder.rglob('*.ttf'):
            # Reed and store font in dictionary {'Font name'; 'path to font file'}
            font_name_key = read_font_name(font_file)
            self._fonts[font_name_key] = str(font_file)
    
    def get_fonts_names_tuple(self) -> (str, str,):
        """Returns tuple of all available font names, each name is a string"""
        fonts_names = tuple(key for key in self._fonts.keys())
        return fonts_names
    
    def get_selected_font(self, font_name: str, font_size: int = 42) -> ImageFont:
        """Reads font file of specified font name and returns ImageFont object of specified size."""
        font_file = self._fonts[font_name]
        font_obj = ImageFont.truetype(font_file, font_size)
        return font_obj


if __name__ == '__main__':
    pass
