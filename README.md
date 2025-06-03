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

## Worked example
This is what I needed the library for in the first place. I have a WSJTX log containing a bunch of FT8 QSOs made on QO-100 and want to correct the TX/RX frequencies, set bands, and sat name.

This program reads the original log, updates the entries, and writes it back out to another log that I then import into Cloudlog.

```
from pyadiflib import AdifParser, AdifWriter

infile = open('wsjtx_log.adi')
adif = AdifParser(infile).parse()
infile.close()

for qso in adif.qsos:
    qso['band_rx'] = '3cm'
    qso['band'] = '13cm'
    qso['sat_name'] = 'QO-100'

    freq = float(qso.get('freq', 0))
    if freq > 0:
        freq_tx = freq - 10489.500 + 2400
        qso['freq'] = freq_tx
        qso['freq_rx'] = freq

outfile = open('output.adi', 'w')
writer = AdifWriter(outfile)
writer.write(adif)
outfile.close()
```
