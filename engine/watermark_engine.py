from PIL import Image, ImageDraw, ImageFont, ImageChops


class WatermarkEngine:
    def __init__(self):
        self._font_list = {
            'OpenSans': '../fonts/ttf/Open_Sans/static/OpenSans/OpenSans-Regular.ttf',
            'Caveat': '../fonts/ttf/Caveat/static/Caveat-Regular.ttf',
        }
        self._current_image_obj = None
        self._current_marked_image_obj = None
        self._current_image_name = None  # path with filename in one str
        self._current_image_path = None  # TODO: MAY BE WILL NOT NEED THAT IN THE FUTURE DEVELOPMENT
        self._current_image_size = None
        self._current_image_width = None
        self._current_image_height = None
        self._current_image_colorspace = None
        # TODO: create variables for parameters
        pass

    def apply_watermark(
            self, image_obj: Image,
            watermark_content: str = "KT",
            font_size: int = 150,
            font: str = 'OpenSans',
            margin_horizontal: int = 30,
            margin_vertical: int = 30,
            side: str = 'bottom',
            color: str = 'WHITE',
            opacity: int = '30',
            across: bool = False
    ):
        # TODO: Collect all methods here
        self._current_image_obj = image_obj
        self._gather_info()
        self._create_watermark(
            font=self._font_list[font],
            size=font_size,
            content=watermark_content,
        )
        return self._current_marked_image_obj
    
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
    
    def _calculate_placement(self):
        # https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html#PIL.ImageDraw.ImageDraw.textbbox
        # TODO: Create a mechanism that will output exactly where to put watermark
        # TODO: based on parameters like (width and height), watermark size, font, image size
        
        pass
    
    def _create_watermark(self, font, size, content):
        # TODO: Look into https://pythonhosted.org/blend_modes/
        # TODO: Also this !!!! more important https://colab.research.google.com/drive/1CJy_vzoOcQdomINNMz1TyjXLGsZLZzwF?usp=sharing
        
        # Initiate font class
        font = ImageFont.truetype(font, size)
        # Create new image the size of the _current_image
        watermark_image = Image.new(
            self._current_image_colorspace,
            (self._current_image_width, self._current_image_height),
            "white"
        )
        # Initiate class that will rasterize font on to the image
        draw_engine = ImageDraw.Draw(watermark_image)
        # Draw letters
        draw_engine.text((self._current_image_width, self._current_image_height), content, fill="black", anchor="rd", font=font)
        self._current_marked_image_obj = ImageChops.multiply(self._current_image_obj, watermark_image)
    # TODO: Translate chosen side to anchor values https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html
        
        # TODO: Using predetermined parameters call for method to actually apply watermark
        pass
    
    def _output_result(self):
        # TODO: Create function that returns modified image object
        pass


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
