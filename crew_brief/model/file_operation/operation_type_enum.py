from enum import IntEnum

from crew_brief.model.base import DatabaseEnumMeta

class FileOperationTypeEnum(IntEnum, metaclass=DatabaseEnumMeta):
    """
    Type of file operation to execute. This is like a command in the terminal.
    """

    __model__ = 'FileOperationType'

    __member_args__ = {
        'ZIP_APPEND': {
            'description': 'Append `target_file` to the ZIP file `leg_file`.',
        },
    }

    ZIP_APPEND = 1

    @classmethod
    def get_model(cls):
        return FileOperationType

    def _set_attrs(self, description):
        self.description = description

    def db_instance(self):
        model = self.get_model()

        return model(
            id = self.value,
            name = self.name,
            description = self.description,
        )


FileOperationTypeEnum.ZIP_APPEND._set_attrs(
    'Append `target_file` to the ZIP file `leg_file`.')
