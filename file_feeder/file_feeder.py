from pathlib import Path


# files = (p.resolve() for p in Path(path).glob("**/*") if p.suffix in {".c", ".cc", ".cpp", ".hxx", ".h"})
class FileFeeder:
    def __init__(self):
        self.images_file_path: list = list()
        self.file_types: (str, ...) = ('jpeg', 'jpg')
        
    def feed_directory(self, directory: str | Path, include_subfolders: bool = True, *args, **kwargs):
        if include_subfolders is True:
            for extension in self.file_types:
                for image_file_path in Path(directory).rglob(f'*.{extension}'):
                    # look for any Jpeg file in folder including subfolders, if found - append its path to the list
                    self.images_file_path.append(str(image_file_path))
        elif include_subfolders is False:
            for extension in self.file_types:
                for image_file_path in Path(directory).glob(f'*.{extension}'):
                    # look for any Jpeg file only in specified folder, if found - append its path to the list
                    self.images_file_path.append(str(image_file_path))
        else:
            raise ValueError(f'Include_subfolders only accepts True or False, but {include_subfolders} was provided.')
    
    def feed_file(self, file: str, *args, **kwargs):
        if (type(file) == tuple or type(file) == list) and len(file) >= 2:
            self.images_file_path = [image_file_path for image_file_path in file]
        else:
            self.images_file_path.append(file)
        pass


if __name__ == '__main__':
    def test_dir():
        test_obj = FileFeeder()
        test_obj.feed_directory('C:\python_projects\py_watermark\img')
        for i in test_obj.images_file_path:
            print(i)
            
    def test_without_subdir():
        test_obj = FileFeeder()
        test_obj.feed_directory('C:\python_projects\py_watermark\img', include_subfolders=False)
        for i in test_obj.images_file_path:
            print(i)

    def test_file():
        files = (
            'C:\python_projects\py_watermark\img\dogo_cmyk_af_ICC_discarded).jpeg',
            'C:\python_projects\py_watermark\img\dogo_cmyk_af_ICC_baked).jpeg'
        )
        test_obj = FileFeeder()
        test_obj.feed_file(files)
        print(type(test_obj.images_file_path))
        for i in test_obj.images_file_path:
            print(i)
        print(test_obj.images_file_path)
    
    # test_dir()
    # test_without_subdir()
    # test_file()
