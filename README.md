I needed a quick and dirty ADIF reader/writer for a log cleanup exercise. I couldn't find another library that 'felt right', so this emerged.

## Reading
```
from pyadiflib import AdifFile, AdifParser
f = open('log.adi')
adif = AdifParser(f).parse()
print(adif)
>>> AdifFile(
    preamble='ADIF Export',
    version='3.1.1',
    created=datetime.datetime(2025, 6, 1, 15, 12, 50),
    program_id='WSJT-X',
    program_version='2.6.1',
    qsos=[
        {
            'call': 'IZ8DBJ',
            'gridsquare': 'JN70',
            'mode': 'FT8',
            # --8<---
        }
    ]
)
```

QSOs come out as a list of dicts, no processing is done on the values and everything is a string.

## Writing
```
from pyadiflib import AdifFile, AdifWriter
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
writer.write()

print(buf.getvalue())
```

Populate the AdifFile struct and add QSOs to the list of dicts, then write them out. No special value handling apart from datetimes which are automatically formatted as strings.
