import io
from pyadiflib import AdifWriter, AdifFile

def test_write_header():
    adif = AdifFile(preamble='test output', version='1.0.0', program_id='test program')
    buf = io.StringIO()
    writer = AdifWriter(buf)
    writer.write(adif)
    s = buf.getvalue()

    assert s.startswith('test output')
    assert '<adif_ver:5>1.0.0' in s
    assert '<programid:12>test program' in s
    assert s.endswith('<eoh>\n')

def test_write_qso():
    adif = AdifFile(preamble='test output', version='1.0.0', program_id='test program')
    adif.qsos = []
    adif.qsos.append({
        'call': 'G4IYT',
        'freq': 7110000,
        'band': '40m'
    })
    adif.qsos.append({
        'call': '2E0IYN',
        'freq': 1942000,
        'band': '160m'
    })
    buf = io.StringIO()
    writer = AdifWriter(buf)
    writer.write(adif)
    s = buf.getvalue()

    assert '<call:5>G4IYT ' in s
    assert '<band:3>40m ' in s
    assert '<freq:7>7110000 ' in s

    assert '<call:6>2E0IYN ' in s
    assert '<band:4>160m ' in s
    assert '<freq:7>1942000 ' in s

    assert s.endswith('<eor>\n')
