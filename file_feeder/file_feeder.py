from pathlib import Path


# files = (p.resolve() for p in Path(path).glob("**/*") if p.suffix in {".c", ".cc", ".cpp", ".hxx", ".h"})
class FileFeeder:
    def __init__(self):
        self._images_files_path: list = list()
        self._file_types: (str, ...) = ('jpeg', 'jpg')
        
    def process_directory(self, directory: str | Path, include_subfolders: bool = True, *args, **kwargs):
        if include_subfolders is True:
            for extension in self._file_types:
                for image_file_path in Path(directory).rglob(f'*.{extension}'):
                    # look for any Jpeg file in folder including subfolders, if found - append its path to the list
                    self._images_files_path.append(
                        {'name': image_file_path.name, 'path': str(image_file_path)}
                    )
                    
        elif include_subfolders is False:
            for extension in self._file_types:
                for image_file_path in Path(directory).glob(f'*.{extension}'):
                    # look for any Jpeg file only in specified folder, if found - append its path to the list
                    self._images_files_path.append(
                        {'name': image_file_path.name, 'path': str(image_file_path)}
                    )
        else:
            raise ValueError(f'Include_subfolders only accepts True or False, but {include_subfolders} was provided.')
    
    def process_file(self, file: str, *args, **kwargs):
        if (type(file) == tuple or type(file) == list) and len(file) >= 2:
            # self._images_files_path = [image_file_path for image_file_path in file]
            for item in file:
                image_file_path = Path(item)
                self._images_files_path.append(
                    {'name': image_file_path.name, 'path': str(image_file_path)}
                )
        else:
            image_file_path = Path(file)
            self._images_files_path.append(
                {'name': image_file_path.name, 'path': str(image_file_path)}
            )
    
    def get_files(self):
        return self._images_files_path


if __name__ == '__main__':
    def test_dir():
        test_obj = FileFeeder()
        test_obj.process_directory('C:\python_projects\py_watermark\img')
        for i in test_obj._images_files_path:
            print(i)
            
    def test_without_subdir():
        test_obj = FileFeeder()
        test_obj.process_directory('C:\python_projects\py_watermark\img', include_subfolders=False)
        for i in test_obj._images_files_path:
            print(i)

    def test_file():
        files = (
            'C:\python_projects\py_watermark\img\dogo_cmyk_af_ICC_discarded).jpeg',
            'C:\python_projects\py_watermark\img\dogo_cmyk_af_ICC_baked).jpeg'
        )
        test_obj = FileFeeder()
        test_obj.process_file(files)
        print(type(test_obj._images_files_path))
        for i in test_obj._images_files_path:
            print(i)
    
    # test_dir()
    # test_without_subdir()
    # test_file()
