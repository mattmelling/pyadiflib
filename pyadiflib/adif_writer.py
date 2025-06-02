import io
from pyadiflib import AdifFile
from datetime import datetime
from typing import Any, Optional

class AdifWriter:
    _file: io.TextIOBase

    def __init__(self, file: io.TextIOBase) -> None:
        self._file = file

    def value_to_string(self, value: Any) -> str:
        if value is datetime:
            return value.strftime('%Y%m%d %H%M%S')
        return str(value)

    def write_tag(self, name: str, value: Optional[Any], newline: bool=False) -> None:
        if value is None:
            self._file.write(f'<{name}>')
        else:
            val_str = str(value)
            val_len = len(val_str)
            self._file.write(f'<{name}:{val_len}>{val_str} ')
        if newline:
            self._file.write('\n')

    def write(self, adif: AdifFile) -> None:
        if adif.preamble is not None and len(adif.preamble) > 0:
            self._file.write(f'{adif.preamble}\n')
        if adif.version is not None and len(adif.version) > 0:
            self.write_tag('adif_ver', adif.version)
        if adif.created is not None:
            self.write_tag('created_time', adif.created)
        if adif.program_id is not None and len(adif.program_id) > 0:
            self.write_tag('programid', adif.program_id)
        if adif.program_version is not None and len(adif.program_version) > 0:
            self.write_tag('programversion', adif.program_version)
        self.write_tag('eoh', None, True)

        if adif.qsos is None:
            return

        for qso in adif.qsos:
            for k, v in qso.items():
                self.write_tag(k, v)
            self.write_tag('eor', None, True)
