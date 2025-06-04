import io
import os

from typing import Optional, Any, Iterable, Dict
from datetime import datetime

from pyadiflib import AdifFile

class AdifParser:
    _file: io.TextIOWrapper

    def __init__(self, file: io.TextIOWrapper) -> None:
        self._file = file

        off = file.tell()
        file.seek(0, os.SEEK_END)
        self._size = file.tell() - off - 4
        file.seek(off, os.SEEK_SET)

    def read_until(self, ch: str) -> str:
        str = ''
        s = self._file.read(1)
        while s != ch:
            if s == '':
                break
            str += s
            s = self._file.read(1)
        return str

    def read_tag(self) -> tuple[str, Optional[str]]:
        self.read_until('<')
        adif_tag = self.read_until('>')

        if ':' not in adif_tag:
            return (adif_tag.lower(), None)

        tag, sz = adif_tag.split(':')
        val = self._file.read(int(sz)).strip()
        return (tag.lower(), val)

    def read_tags(self) -> Iterable[tuple[str, Optional[str]]]:
        while self._file.tell() <= self._size:
            yield self.read_tag()

    def read_header(self, adif: AdifFile) -> None:
        adif.preamble = self.read_until('<').strip()
        self._file.seek(len(adif.preamble) - 1, os.SEEK_SET)

        tag = None
        for tag, val in self.read_tags():
            if tag == 'eoh':
                break
            elif tag == 'adif_ver':
                adif.version = val
            elif tag == 'created_timestamp' and val is not None:
                adif.created = datetime.strptime(val, '%Y%m%d %H%M%S')
            elif tag == 'programid':
                adif.program_id = val
            elif tag == 'programversion':
                adif.program_version = val

    def parse(self) -> AdifFile:
        adif = AdifFile()
        adif.qsos = []

        self.read_header(adif)

        qso: Dict[str, Any] = {}
        for tag, val in self.read_tags():
            if tag == 'eor':
                adif.qsos.append(qso)
                qso = {}
                continue
            qso[tag] = val

        return adif
