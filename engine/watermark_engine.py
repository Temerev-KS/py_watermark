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
            'BLACK': (255, 255, 255),
            'WHITE': (0, 0, 0),
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
        # self._current_image_path = None  # TODO: MAY BE WILL NOT NEED THAT IN THE FUTURE DEVELOPMENT
        self._current_img_size = None
        self._current_img_width = None
        self._current_img_height = None
        self._current_img_colorspace = None
        
        self.mark_text: str = "KT"
        self.font_size: int = 250
        self.font: str = 'OpenSans-SemiBold'
        self.alignment_vertical: str = 'BOTTOM'
        self.alignment_horizontal: str = 'RIGHT'
        self.margin_horizontal: int = 50
        self.margin_vertical: int = 50
        self.anchor: str = 'rd'
        self.color: str = 'MUSTARD'
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
        self.mark_text: str = ""
        self.font_size: int = 250
        self.font: str = 'OpenSans-SemiBold'
        self.alignment_vertical: str = 'BOTTOM'
        self.alignment_horizontal: str = 'RIGHT'
        self.margin_horizontal: int = 50
        self.margin_vertical: int = 50
        self.anchor: str = 'rd'
        self.color: str = 'WHITE'
        self.opacity: int = 125
        self.across: bool = False
    
    def apply_watermark(
            self, image_obj: Image,
    ):
        self._current_img_obj = image_obj
        self._gather_info()
        self._create_watermark()
        
        return self._output_result()
    
    def _check_values(self):
        # TODO: Check if image exists
        # TODO: Check if image has correct colorspace
        # TODO: Check if image size is no smaller then watermark
        # TODO: Check if parameters passed are actually correct (font, font size, margins, dont color, opacity)
        # TODO: Check if watermark will fit into image width and specified margin
        pass
    
    def _gather_info(self):
        self._current_img_name = self._current_img_obj.filename
        self._current_img_size = self._current_img_obj.size
        self._current_img_width = self._current_img_obj.width
        self._current_img_height = self._current_img_obj.height
        self._current_img_colorspace = self._current_img_obj.mode
    
    def _calculate_placement(self, margin_h, margin_v):
        #    left middle right
        #   ┌─────┬─────┬─────┐
        #   │ lt  │ mt  │ rt  │  top
        #   ├─────┼─────┼─────┤
        #   │ lm  │ mm  │ rm  │  middle
        #   ├─────┼─────┼─────┤
        #   │ ld  │ md  │ rd  │  bottom
        #   └─────┴─────┴─────┘
        # https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html#PIL.ImageDraw.ImageDraw.textbbox
        # TODO: Create a mechanism that will output exactly where to put watermark
        # TODO: based on parameters like (width and height), watermark size, font, image size
        # X - Y (width , HEIGHT)
        top = 0 + abs(margin_v)
        center = self._current_img_height / 2 + margin_v
        bottom = self._current_img_height - abs(margin_v)
        
        left = 0 + abs(margin_h)
        middle = self._current_img_width / 2 + margin_h
        right = self._current_img_width - abs(margin_h)
        
        top_left = (top, left)
        top_middle = (top, middle)
        top_right = (top, right)
        center_left = (center, left)
        center_middle = (center, middle)
        center_right = (center, right)
        bottom_left = (bottom, left)
        bottom_middle = (bottom, middle)
        bottom_right = (bottom, right)
    
    def _create_watermark(self):
        # Initiate font class
        font = ImageFont.truetype(self._font_list[self.font], self.font_size)
        # Create a new image the size of the _current_image
        mark_image = Image.new("RGBA", (self._current_img_width, self._current_img_height), (255, 255, 255, 0))
        # Initiate class that will rasterize font on to the image
        text_typist = ImageDraw.Draw(mark_image)
        text_typist.text(
            (int(1000), int(300)),  # TODO: This needs to be predetermined
            self.mark_text,
            fill=(*self._color_list[self.color], self.opacity),
            anchor=self.anchor,
            font=font
        )
        self._current_mk_img_obj = Image.alpha_composite(self._current_img_obj.convert('RGBA'), mark_image)
    
    # TODO: Translate chosen side to anchor values https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html
    
    # TODO: Using predetermined parameters call for method to actually apply watermark
    
    def _output_result(self) -> Image:
        # TODO: Create function that returns modified image object
        final_image = self._current_mk_img_obj.convert('RGB')
        return final_image


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
    
    # TODO: DO STUFF WITH IMAGE HERE
    
    dummy_save_file_func(engine.apply_watermark(test_img))
    pass
