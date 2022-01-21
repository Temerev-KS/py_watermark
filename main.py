from PIL import Image
from fonts import FontsLibrary
from watermark_engine import WatermarkEngine


def func():
    img = Image.open('img/dogo.jpeg')
    img = Image.open('img/dogo.jpeg')
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
    def dummy_file_func(file_name='../img/dogo.jpeg') -> Image:
        # READS FILE
        # test_image = Image.open(file_name)
        test_image = Image.open('C:\python_projects\py_watermark\img\dogo_cmyk_PILL.jpeg')
        return test_image
    
    def dummy_save_file_func(file_obj: Image, file_name: 'str' = 'test_dogo.jpg'):
        # WRITES FILE
        file_obj.save(file_name)
    
    engine = WatermarkEngine()
    
    test_img = dummy_file_func()
    
    dummy_save_file_func(engine.apply_watermark(test_img))
    pass
    
if __name__ == '__main__':
    # func()
    # fonts_test()
    engine_test()
    pass
    