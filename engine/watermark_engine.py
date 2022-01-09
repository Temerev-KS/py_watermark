from PIL import Image


class WatermarkEngine:
    def __init__(self):
        self._current_image_name = None
        self._current_image_path = None
        self._current_image_size = None
        # TODO: create variables for parameters
        pass

    def apply_watermark(self):
        # TODO: Collect all methods here
        pass
    
    def _check_values(self):
        # TODO: Check if image exists
        # TODO: Check if image has correct colorspace
        # TODO: Check if image size is no smaller then watermark
        # TODO: Check if parameters passed are actually correct (font, font size, margins, dont color, opacity)
        # TODO: Check if watermark will fit into image width and specified margin
        pass
    
    def _gather_info(self):
        # TODO: store in variable image size
        # TODO: store in variable colorspace ???
        pass
    
    def _calculate_placement(self):
        # TODO: Create a mechanism that will output exactly where to put watermark
        # TODO: based on parameters like (width and height), watermark size, font, image size
        
        pass
    
    def _create_watermark(self):
        # TODO: Using predetermined parameters call for method to actually apply watermark
        pass
    
    def _output_result(self):
        # TODO: Create function that returns modified image object
        pass


if __name__ == '__main__':
    def dummy_file_func(file_name='img/dogo.jpeg') -> Image:
        # READS FILE
        test_image = Image.open(file_name)
        return test_image
    
    def dummy_save_file_func(file_obj: Image, file_name: 'str' = 'test_dogo.jpg'):
        # WRITES FILE
        file_obj.save(file_name)
    
    
    engine = WatermarkEngine()
    
    test_img = dummy_file_func()
    
    # TODO: DO STUFF WITH IMAGE HERE
    
    dummy_save_file_func(test_img)
    pass
