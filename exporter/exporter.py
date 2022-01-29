import re
from pathlib import Path, PurePath


class Exporter:
    def __init__(self):
        self._name = None
        self._destination = None
        self._image = None
        self._destination_same_as_source = True
        self._override_destination = False
    
    def set_params(self, same_as_source: bool = True, destination: str = '', override: bool = False):
        """
        :param same_as_source toggle option to save marked file in the same folder as an original image
        :param destination will be used as path to destination folder for saving marked files,
        but only if same_as_source is False, otherwise destination parameter will be ignored
        :param override: will change filename of exported file if destination folder contains file with the same name
        """
        self._destination_same_as_source = same_as_source
        self._override_destination = override
        if self._destination_same_as_source is False:
            if not Path(destination).exists():
                Path(destination).mkdir()
            self._destination = destination
        
    def export_file(self, image_dict: dict):
        """
        :param image_dict expects as input a dictionary matching this pattern
        {'name':'filename.extension', 'path': 'path/to/dir', 'image': Image object (PIL)}
        """
        self._name = image_dict['file_name']
        self._image = image_dict['image']
        if self._destination_same_as_source:
            self._destination = image_dict['path']
        export_path = Path(PurePath(self._destination).joinpath(self._name))
        if export_path.exists() and self._override_destination is False:
            def file_name_index(index: int = 0):
                name_index = index + 1
                new_file_name = PurePath(self._name).stem + f'_marked_{name_index:03}' + PurePath(self._name).suffix
                new_export_path = Path(PurePath(self._destination).joinpath(new_file_name))
                if Path(new_export_path).exists():
                    file_name_index(name_index)
                else:
                    self._image.save(new_export_path)
            file_name_index()
        else:
            self._image.save(export_path)


# TODO: Figure out if regex file name index matching is even necessary
def regex_search():
    pattern = r'(.*?)_marked_([0-9]+)(\.\w{2,4})$'
    file_name = "picture_marked_888888.jpeg"
    print('Name ' + re.search(pattern, file_name).group(1))
    print('Index ' + re.search(pattern, file_name).group(2))
    print('Suffix ' + re.search(pattern, file_name).group(3))
    