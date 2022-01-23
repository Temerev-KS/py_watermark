from PIL import Image, ImageDraw, UnidentifiedImageError
from fonts import FontsLibrary
from color_library import ColorLibrary


class WatermarkEngine:
    def __init__(self):
        self.font_library = FontsLibrary()
        self.color_library = ColorLibrary()
        self._img_obj = None
        self._marked_img_obj = None
        self._img_name = None  # path with filename in one str
        self._img_size = None
        self._img_width = None
        self._img_height = None
        self._img_colorspace = None
        self._watermark_placement = None
        self._anchor: str = 'mm'
        
        self.mark_text: str = ''
        self.font_size: int = 0
        self.font: str = ''
        self.alignment_vertical: str = ''
        self.alignment_horizontal: str = ''
        self.margin_horizontal: int = 0
        self.margin_vertical: int = 0
        self.color: str = ''
        self.opacity: int = 0
        self.across: bool = False
        
        self.parameters_reset()
    
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
            self._anchor = anchor
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
        self.mark_text: str = "BIG BAD WOLF"
        self.font_size: int = 250
        self.font: str = 'Open Sans SemiBold'
        self.alignment_vertical: str = 'center'
        self.alignment_horizontal: str = 'middle'
        self.margin_horizontal: int = 100
        self.margin_vertical: int = 50
        self._anchor: str = 'mm'
        self.color: str = 'BLACK'
        self.opacity: int = 125
        self.across: bool = False
    
    def apply_watermark(self, image_obj: Image):
        if image_obj is None:  # If we've been passed any object to work with - continue, else skip this one
            pass
        else:
            self._img_obj = image_obj
            try:
                self._gather_info()
            except (FileNotFoundError, UnidentifiedImageError):  # If file not found or has unexpected format - skip
                return
            self._check_values()
            self._calculate_placement()
            self._create_watermark()
            return self._output_result()
    
    def _check_values(self):
        # TODO: Check if image has correct colorspace
        # If FIle in CMYK and ICC is discarded or baked- colors will be off to a green/yellow'ish hue
        # If File was converted to CMYK with PIL.Image.convert - converting int back to RGB will yield a good resold
        # Temporary solution is to convert image anyway, but this is something that has to be improved in the future
        # May LOG that file as something that needs to be checked after conversion
        # TODO: Check if parameters passed are actually correct
        #  (font, font size, margins, .font color, opacity, no "\n" characters)
        # May be better solution would be to pre check some parameters before launching apply method
        # Or even better solution would be to check them on the fly as the parameters are being set
        # TODO: Check if watermark will fit into image width and specified margin
    
        current_font = self.font_library.get_selected_font(self.font, self.font_size)
        sample_image = Image.new("RGBA", (1, 1), (255, 255, 255, 0))
        measure_image = ImageDraw.Draw(sample_image)
        text_bounding_box = measure_image.textbbox((0, 0), self.mark_text, current_font, spacing=400)
        text_width = text_bounding_box[2] - text_bounding_box[0] + self.margin_horizontal
        text_height = text_bounding_box[3] - text_bounding_box[1] + self.margin_vertical
        if text_width > self._img_width or text_height > self._img_width:
            print('watermark is too big')
            
        # And if it does not? What?
        # Options: Skip it  |  Reduce the size of the watermark temporary for one file  |  Continue anyway  |
        # Continue and log it
        
        # https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html#PIL.ImageDraw.ImageDraw.textbbox

        pass
    
    def _gather_info(self):
        self._img_name = self._img_obj.filename
        self._img_size = self._img_obj.size
        self._img_width = self._img_obj.width
        self._img_height = self._img_obj.height
        self._img_colorspace = self._img_obj.mode
    
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
            self._anchor = self._anchor.replace(self._anchor[1], 't', 1)
            return 0 + abs(self.margin_vertical)
        
        def center():
            self._anchor = self._anchor.replace(self._anchor[1], 'm', 1)
            return self._img_height / 2 + self.margin_vertical
        
        def bottom():
            self._anchor = self._anchor.replace(self._anchor[1], 'd', 1)
            return self._img_height - abs(self.margin_vertical)
        
        def left():
            self._anchor = self._anchor.replace(self._anchor[0], 'l', 1)
            return 0 + abs(self.margin_horizontal)
        
        def middle():
            self._anchor = self._anchor.replace(self._anchor[0], 'm', 1)
            return self._img_width / 2 + self.margin_horizontal
        
        def right():
            self._anchor = self._anchor.replace(self._anchor[0], 'r', 1)
            return self._img_width - abs(self.margin_horizontal)
        
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
        self._watermark_placement = (
            alignments_horizontal[self.alignment_horizontal](),
            alignments_vertical[self.alignment_vertical]()
        )
    
    def _create_watermark(self):
        # Load the font and specify font size
        font = self.font_library.get_selected_font(self.font, self.font_size)
        # Create a new image the size of the _current_image
        mark_image = Image.new("RGBA", (self._img_width, self._img_height), (255, 255, 255, 0))
        # Initiate class that will rasterize font on to the image
        text_typist = ImageDraw.Draw(mark_image)
        text_typist.text(
            self._watermark_placement,
            self.mark_text,
            fill=(*self.color_library.get_rgb_color_value(self.color), self.opacity),
            anchor=self._anchor,
            font=font
        )
        appropriate_colorspace_img_obj = self._img_obj.convert('RGBA')
        self._marked_img_obj = Image.alpha_composite(appropriate_colorspace_img_obj, mark_image)
    
    def _output_result(self) -> Image:
        final_rgb_image = self._marked_img_obj.convert('RGB')
        return final_rgb_image


if __name__ == '__main__':
    pass
