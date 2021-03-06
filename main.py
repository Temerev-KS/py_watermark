from file_feeder import FileFeeder
from watermark_engine import WatermarkEngine
from exporter import Exporter

    
def full_cycle_test():
    file_feeder = FileFeeder()
    engine = WatermarkEngine()
    exporter = Exporter()
    exporter.set_params(same_as_source=False, destination=r'export_img')
    file_feeder.process_directory(r'img')
    # file_feeder.process_file(r'img/dogo.jpeg')
    for image in file_feeder.get_files():
        final_image = engine.apply_watermark(image)
        exporter.export_file(final_image)
    

if __name__ == '__main__':
    full_cycle_test()
    