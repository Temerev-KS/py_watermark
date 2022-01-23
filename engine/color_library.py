class ColorLibrary:
    """Class responsible for storing and returning color data for the watermark"""
    def __init__(self):
        self.rgb_colors = None
        self.load_rgb_colors()
        
    def load_rgb_colors(self):
        self.rgb_colors = {
            # BLACK, WHITE, GRAY, RUBY, PINK, GRASS, PISTACHIO, ORANGE, BLUE, INDIGO, PURPLE, YELLOW, BEIGE, MUSTARD,
            'BLACK': (0, 0, 0),
            'WHITE': (255, 255, 255),
            'GRAY': (127, 127, 127),
            'RUBY': (191, 10, 48),
            'PINK': (230, 0, 126),
            'GRASS': (0, 154, 23),
            'PISTACHIO': (180, 231, 183),
            'ORANGE': (255, 123, 0),
            'BLUE': (49, 99, 156),
            'INDIGO': (0, 27, 148),
            'PURPLE': (91, 10, 145),
            'YELLOW': (255, 233, 0),
            'BEIGE': (244, 226, 198),
            'MUSTARD': (234, 170, 0)
        }
        
    def get_rgb_color_value(self, color_name: str) -> (int, int, int):
        """Returns 8 bit rgb color values of color from dictionary"""
        if color_name in self.rgb_colors:
            return self.rgb_colors[color_name]
        else:
            raise KeyError(f'Unknown Color "{color_name}"')
    
    def get_all_rgb_color_names(self) -> (str, ...):
        """Returns a tuple with the names of all available colors"""
        color_names = tuple(key for key in self.rgb_colors.keys())
        return color_names
        