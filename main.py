from PIL import Image
from fonts import FontsLibrary
from watermark_engine import WatermarkEngine
from file_feeder import FileFeeder


def func():
    img = Image.open(r'C:\\python_projects\\py_watermark\test_dogo1.jpg')
    # img = Image.open('img/dogo.jpeg')
    print(img.format)
    print(img.size)
    print(img.mode)
    img.save('test.jpg')
    
    
def fonts_test():
    pil_fonts = FontsLibrary()
    print(pil_fonts.get_fonts_names_tuple())
    for key in pil_fonts.get_fonts_names_tuple():
        print(key)
    
    
def engine_test():
    def dummy_file_func(file_name='img/dogo.jpeg') -> Image:
        # READS FILE
        test_image = Image.open(file_name)
        return test_image
    
    def dummy_save_file_func(file_obj: Image, file_name: 'str' = 'test_dogo1.jpg'):
        # WRITES FILE
        file_obj.save(file_name)
    
    engine = WatermarkEngine()
    
    test_img = dummy_file_func()
    
    dummy_save_file_func(engine.apply_watermark(test_img))
    pass


def feed_and_process_test():
    file_feeder = FileFeeder()
    file_feeder.process_file(r'C:\python_projects\py_watermark\img\dogo.jpeg')
    engine = WatermarkEngine()
    for image in file_feeder.get_files():
        final_image = engine.apply_watermark(image)
        final_image['image'].show()
    
    
if __name__ == '__main__':
    # func()
    # fonts_test()
    # engine_test()
    feed_and_process_test()
    
    pass
    