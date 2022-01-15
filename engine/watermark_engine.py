from PIL import Image, ImageDraw, ImageFont


class WatermarkEngine:
    def __init__(self):
        self._font_list = {
            'OpenSans-Regular': '../fonts/ttf/Open_Sans/static/OpenSans/OpenSans-Regular.ttf',
            'OpenSans-SemiBold': '../fonts/ttf/Open_Sans/static/OpenSans/OpenSans-SemiBold.ttf',
            'OpenSans-Bold': '../fonts/ttf/Open_Sans/static/OpenSans/OpenSans-Bold.ttf',
            'Caveat': '../fonts/ttf/Caveat/static/Caveat-Regular.ttf',
        }
        self._color_list = {
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
        self._current_img_obj = None
        self._current_mk_img_obj = None
        self._current_img_name = None  # path with filename in one str
        self._current_img_size = None
        self._current_img_width = None
        self._current_img_height = None
        self._current_img_colorspace = None
        self._current_watermark_placement = None
        
        self.mark_text: str = "BIG BAD WOLF"
        self.font_size: int = 250
        self.font: str = 'OpenSans-SemiBold'
        self.alignment_vertical: str = 'top'
        self.alignment_horizontal: str = 'middle'
        self.margin_horizontal: int = 100
        self.margin_vertical: int = 50
        self.anchor: str = 'xx'
        self.color: str = 'WHITE'
        self.opacity: int = 125
        self.across: bool = False
    
    def parameters_set(self,
                       mark_text: str = None,
                       font_size: int = None,
                       font: str = None,
                       alignment_vertical: str = None,
                       alignment_horizontal: str = None,
                       margin_horizontal: int = None,
                       margin_vertical: int = None,
                       anchor: str = None,
                       color: str = None,
                       opacity: int = None,
                       across: bool = None,
                       ):
        """
        Changes one or multiple parameters.
        
        :param mark_text: A text to be applied as watermark (eg. Author's name, date of creation or smt. else)
        :param font_size: Font size in pixels
        :param font: Font name. Available 'OpenSans-Regular', 'OpenSans-SemiBold', 'OpenSans-Bold', 'Caveat
        :param alignment_vertical: Placement on vertical axis relative to an image (TOP, CENTER, BOTTOM)
        :param alignment_horizontal: Placement on horizontal axis relative to an image (LEFT, MIDDLE, RIGHT)
        :param margin_horizontal: Size (in pix) of horizontal shift relative to selected horizontal_alignment.
                                  Negative values will be applied only if alignment set to middle
        :param margin_vertical: Size (in pix) of vertical shift relative to selected vertical_alignment
                                  Negative values will be applied only if alignment set to center
        :param anchor: PILLOW text property responsible for anchor point of the text
        :param color: Font color. Available options: BLACK, WHITE, GRAY, RUBY, PINK, GRASS, PISTACHIO,
                                                     ORANGE, BLUE, INDIGO, PURPLE, YELLOW, BEIGE, MUSTARD,
        :param opacity: Text opacity. Value from 0 to 255 (0 - completely transparent, 255 - completely opaque)
        :param across: Bol value. Disregards positioning, and forces watermark to go diagonally across the whole image.
                        example would be something like  TOP SECRET, CONFIDENTIAL, or EYES ONLY.
        """
        if mark_text is not None:
            self.mark_text = mark_text
        if font_size is not None:
            self.font_size = font_size
        if font is not None:
            self.font = font
        if alignment_vertical is not None:
            self.alignment_vertical = alignment_vertical
        if alignment_horizontal is not None:
            self.alignment_horizontal = alignment_horizontal
        if margin_horizontal is not None:
            self.margin_horizontal = margin_horizontal
        if margin_vertical is not None:
            self.margin_vertical = margin_vertical
        if anchor is not None:
            self.anchor = anchor
        if color is not None:
            self.color = color
        if opacity is not None:
            self.opacity = opacity
        if across is not None:
            self.across = across
        pass
    
    def parameters_reset(self):
        """
        Resets parameters to the "default" values.
        """
        self.mark_text: str = ""
        self.font_size: int = 250
        self.font: str = 'OpenSans-SemiBold'
        self.alignment_vertical: str = 'bottom'
        self.alignment_horizontal: str = 'right'
        self.margin_horizontal: int = 100
        self.margin_vertical: int = 50
        self.anchor: str = 'rd'
        self.color: str = 'WHITE'
        self.opacity: int = 125
        self.across: bool = False
    
    def apply_watermark(self, image_obj: Image):
        self._current_img_obj = image_obj
        self._check_values()
        self._gather_info()
        self._calculate_placement()
        self._create_watermark()
        return self._output_result()
    
    def _check_values(self):
        # TODO: Check if image exists
        # TODO: Check if image has correct colorspace
        # TODO: Check if image size is no smaller then watermark
        # TODO: Check if parameters passed are actually correct (font, font size, margins, dont color, opacity)
        # TODO: Check if watermark will fit into image width and specified margin
        
        # https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html#PIL.ImageDraw.ImageDraw.textbbox

        pass
    
    def _gather_info(self):
        self._current_img_name = self._current_img_obj.filename
        self._current_img_size = self._current_img_obj.size
        self._current_img_width = self._current_img_obj.width
        self._current_img_height = self._current_img_obj.height
        self._current_img_colorspace = self._current_img_obj.mode
    
    def _calculate_placement(self):
        """
        Calculates placement of the watermark based on the chosen anchor and current image dimensions
        """
        #    left middle right
        #   ┌─────┬─────┬─────┐
        #   │ lt  │ mt  │ rt  │  top
        #   ├─────┼─────┼─────┤
        #   │ lm  │ mm  │ rm  │  center
        #   ├─────┼─────┼─────┤
        #   │ ld  │ md  │ rd  │  bottom
        #   └─────┴─────┴─────┘
        
        # Each function calculates coordinate (x or y) and sets PIL anchor accordingly
        # https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html
        def top():
            self.anchor = self.anchor.replace(self.anchor[1], 't', 1)
            return 0 + abs(self.margin_vertical)
        
        def center():
            self.anchor = self.anchor.replace(self.anchor[1], 'm', 1)
            return self._current_img_height / 2 + self.margin_vertical
        
        def bottom():
            self.anchor = self.anchor.replace(self.anchor[1], 'd', 1)
            return self._current_img_height - abs(self.margin_vertical)
        
        def left():
            self.anchor = self.anchor.replace(self.anchor[0], 'l', 1)
            return 0 + abs(self.margin_horizontal)
        
        def middle():
            self.anchor = self.anchor.replace(self.anchor[0], 'm', 1)
            return self._current_img_width / 2 + self.margin_horizontal
        
        def right():
            self.anchor = self.anchor.replace(self.anchor[0], 'r', 1)
            return self._current_img_width - abs(self.margin_horizontal)
        
        # Store functions to call them later using string
        alignments_vertical = {
            'top': top,
            'center': center,
            'bottom': bottom,
        }
        alignments_horizontal = {
            'left': left,
            'middle': middle,
            'right': right
        }
        # Construct tuple of X,Y coordinates using calls to stored functions
        self._current_watermark_placement = (
            alignments_horizontal[self.alignment_horizontal](),
            alignments_vertical[self.alignment_vertical]()
        )
    
    def _create_watermark(self):
        # Initiate font class
        font_obj = ImageFont.truetype(self._font_list[self.font], self.font_size)
        # Create a new image the size of the _current_image
        mark_image = Image.new("RGBA", (self._current_img_width, self._current_img_height), (255, 255, 255, 0))
        # Initiate class that will rasterize font on to the image
        text_typist = ImageDraw.Draw(mark_image)
        text_typist.text(
            self._current_watermark_placement,
            self.mark_text,
            fill=(*self._color_list[self.color], self.opacity),
            anchor=self.anchor,
            font=font_obj
        )
        appropriate_colorspace_img_obj = self._current_img_obj.convert('RGBA')
        self._current_mk_img_obj = Image.alpha_composite(appropriate_colorspace_img_obj, mark_image)
    
    def _output_result(self) -> Image:
        final_rgb_image = self._current_mk_img_obj.convert('RGB')
        return final_rgb_image


if __name__ == '__main__':
    def dummy_file_func(file_name='../img/dogo.jpeg') -> Image:
        # READS FILE
        test_image = Image.open(file_name)
        return test_image
    
    
    def dummy_save_file_func(file_obj: Image, file_name: 'str' = 'test_dogo.jpg'):
        # WRITES FILE
        file_obj.save(file_name)
    
    
    engine = WatermarkEngine()
    
    test_img = dummy_file_func()
    
    dummy_save_file_func(engine.apply_watermark(test_img))
    pass
