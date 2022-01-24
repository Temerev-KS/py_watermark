from pathlib import Path


class FileFeeder:
    def __init__(self):
        self.images_file_path = list()
        pass
        
    def feed_directory(self, directory: str | Path, include_subfolders: bool = True, *args, **kwargs):
        if include_subfolders is True:
            for image_file_path in Path(directory).rglob('*.jpg'):
                # look for any Jpeg file in folder including subfolders, if found - append its path to the list
                self.images_file_path.append(str(image_file_path))
        elif include_subfolders is False:
            for image_file_path in Path(directory).glob('*.jpg'):
                # look for any Jpeg file only in specified folder, if found - append its path to the list
                self.images_file_path.append(str(image_file_path))
        else:
            raise ValueError(f'Include_subfolders only accepts True or False, but {include_subfolders} was provided.')
    
    def feed_file(self, file: str | (str, ...), *args, **kwargs):
        if (type(file) == tuple or type(file) == list) and len(file) >= 2:
            for image_file_path in file.glob('*.jpg'):
                # look for any Jpeg file only in specified folder, if found - append its path to the list
                self.images_file_path.append(str(image_file_path))
        else:
            self.images_file_path = file
        pass
