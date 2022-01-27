from pathlib import Path, PurePath


class Exporter:
    def __init__(self):
        self._name = None
        self._destination = None
        self._image = None
        self._destination_same_as_source = True
    
    def set_params(self, same_as_source: bool = True, destination: str = ''):
        """
        :param same_as_source toggle option to save marked file in the same folder as an original image
        :param destination will be used as path to destination folder for saving marked files,
        but only if same_as_source is False, otherwise destination parameter will be ignored
        """
        self._destination_same_as_source = same_as_source
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
        self._image.save(export_path)
# TODO: Create toggle to override existing files
