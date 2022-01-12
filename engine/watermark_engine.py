from PIL import Image, ImageDraw, ImageFont


class WatermarkEngine:
    def __init__(self):
        self._font_list = {
            'OpenSans-Regular': '../fonts/ttf/Open_Sans/static/OpenSans/OpenSans-Regular.ttf',
            'OpenSans-SemiBold': '../fonts/ttf/Open_Sans/static/OpenSans/OpenSans-SemiBold.ttf',
            'OpenSans-Bold': '../fonts/ttf/Open_Sans/static/OpenSans/OpenSans-Bold.ttf',
            'Caveat': '../fonts/ttf/Caveat/static/Caveat-Regular.ttf',
        }
        self.color_list = {
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
        self._current_image_obj = None
        self._current_marked_image_obj = None
        self._current_image_name = None  # path with filename in one str
        # self._current_image_path = None  # TODO: MAY BE WILL NOT NEED THAT IN THE FUTURE DEVELOPMENT
        self._current_image_size = None
        self._current_image_width = None
        self._current_image_height = None
        self._current_image_colorspace = None

    def apply_watermark(
            self, image_obj: Image,
            watermark_content: str = "KT",
            font_size: int = 250,
            font: str = 'OpenSans-SemiBold',
            alignment_vertical: str = 'BOTTOM',
            alignment_horizontal: str = 'RIGHT',
            margin_horizontal: int = 50,
            margin_vertical: int = 50,
            anchor: str = 'rd',
            color: str = 'MUSTARD',
            opacity: int = 125,
            across: bool = False
    ):
        self._current_image_obj = image_obj
        self._gather_info()
        self._create_watermark(
            font=self._font_list[font],
            size=font_size,
            content=watermark_content,
            opacity=opacity,
            color=color,
            anchor=anchor
        )
        
        return self._output_result()
    
    def _check_values(self):
        # TODO: Check if image exists
        # TODO: Check if image has correct colorspace
        # TODO: Check if image size is no smaller then watermark
        # TODO: Check if parameters passed are actually correct (font, font size, margins, dont color, opacity)
        # TODO: Check if watermark will fit into image width and specified margin
        pass
    
    def _gather_info(self):
        self._current_image_name = self._current_image_obj.filename
        self._current_image_size = self._current_image_obj.size
        self._current_image_width = self._current_image_obj.width
        self._current_image_height = self._current_image_obj.height
        self._current_image_colorspace = self._current_image_obj.mode
    
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
        # (ld / lm / lt) (mt / mm / md) (rt / rm / rd)
        # Vertical alignment: TOP MIDDLE BOTTOM
        # Vertical margin:
        # Horizontal alignment: LEFT MIDDLE RIGHT
        # Horizontal margin:
        # X - Y (width , HEIGHT)
        top = 0 + abs(margin_v)
        center = self._current_image_height / 2 + margin_v
        bottom = self._current_image_height - abs(margin_v)
        
        left = 0 + abs(margin_h)
        middle = self._current_image_width / 2 + margin_h
        right = self._current_image_width - abs(margin_h)
        
        top_left = (top, left)
        top_middle = (top, middle)
        top_right = (top, right)
        center_left = (center, left)
        center_middle = (center, middle)
        center_right = (center, right)
        bottom_left = (bottom, left)
        bottom_middle = (bottom, middle)
        bottom_right = (bottom, right)
        
    def _create_watermark(self, font, size, content, opacity, color, anchor):
        # Initiate font class
        font = ImageFont.truetype(font, size)
        # Create new image the size of the _current_image
        watermark_image = Image.new(
            "RGBA", (self._current_image_width, self._current_image_height), (255, 255, 255, 0)
        )
        # Initiate class that will rasterize font on to the image
        text_typist = ImageDraw.Draw(watermark_image)
        text_typist.text(
            (int(1000), int(300)),  # TODO: This needs to be predetermined
            content, fill=(*self.color_list[color], opacity), anchor=anchor, font=font
        )
        self._current_marked_image_obj = Image.alpha_composite(
            self._current_image_obj.convert('RGBA'),
            watermark_image
        )
    # TODO: Translate chosen side to anchor values https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html
        
        # TODO: Using predetermined parameters call for method to actually apply watermark
    
    def _output_result(self) -> Image:
        # TODO: Create function that returns modified image object
        final_image = self._current_marked_image_obj.convert('RGB')
        # final_image.show()
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
