from datetime import datetime
import io

from pyadiflib import AdifParser

def test_parse_header():
    f = io.StringIO("""
ADIF Export Preamble
<adif_ver:5>1.0.0
<created_timestamp:15>20250601 151250
<programid:12>Test Program
<programversion:5>0.0.1
<eoh>
""")
    p = AdifParser(f)
    adif = p.parse()

    assert adif.version == '1.0.0'
    assert adif.created == datetime(2025, 6, 1, 15, 12, 50)
    assert adif.program_id == 'Test Program'
    assert adif.program_version == '0.0.1'
    assert len(adif.qsos) == 0

def test_parse_qsos():
    f = io.StringIO("""
ADIF Export
<adif_ver:5>3.1.1
<created_timestamp:15>20250601 151250
<programid:6>WSJT-X
<programversion:5>2.6.1
<eoh>
<call:6>IZ8DBJ <gridsquare:4>JN70 <mode:3>FT8 <rst_sent:3>-15 <rst_rcvd:3>-17 <qso_date:8>20250601 <time_on:6>151200 <qso_date_off:8>20250601 <time_off:6>151245 <band:3>3cm <freq:12>10489.541901 <station_callsign:5>G4IYT <my_gridsquare:6>IO91QV <tx_pwr:2>6W <prop_mode:3>SAT <eor>
<call:6>SP6IWQ <gridsquare:4>JO80 <mode:3>FT8 <rst_sent:3>+01 <rst_rcvd:3>-03 <qso_date:8>20250601 <time_on:6>151315 <qso_date_off:8>20250601 <time_off:6>151345 <band:3>3cm <freq:12>10489.541901 <station_callsign:5>G4IYT <my_gridsquare:6>IO91QV <tx_pwr:2>6W <prop_mode:3>SAT <eor>
<call:5>YB5QZ <gridsquare:4>OJ00 <mode:3>FT8 <rst_sent:3>-02 <rst_rcvd:3>-12 <qso_date:8>20250601 <time_on:6>151400 <qso_date_off:8>20250601 <time_off:6>151445 <band:3>3cm <freq:12>10489.541901 <station_callsign:5>G4IYT <my_gridsquare:6>IO91QV <tx_pwr:2>6W <prop_mode:3>SAT <eor>
""")
    p = AdifParser(f)
    adif = p.parse()

    assert len(adif.qsos) == 3
    assert adif.qsos[0].get('call') == 'IZ8DBJ'
    assert adif.qsos[1].get('call') == 'SP6IWQ'
    assert adif.qsos[2].get('call') == 'YB5QZ'
    assert adif.qsos[2].get('gridsquare') == 'OJ00'
    assert adif.qsos[2].get('band') == '3cm'
    assert adif.qsos[1].get('station_callsign') == 'G4IYT'

def test_parse_invalid_len():
    f = io.StringIO("""
ADIF Export
<adif_ver:5>3.1.1
<created_timestamp:15>20250601 151250
<programid:6>WSJT-X
<programversion:5>2.6.1
<eoh>
<call:5>YB5QZ <gridsquare:10>OJ00 <mode:3>FT8 <rst_sent:3>-02 <rst_rcvd:3>-12 <qso_date:8>20250601 <time_on:6>151400 <qso_date_off:8>20250601 <time_off:6>151445 <band:3>3cm <freq:12>10489.541901 <station_callsign:5>G4IYT <my_gridsquare:6>IO91QV <tx_pwr:2>6W <prop_mode:3>SAT <eor>
""")
    p = AdifParser(f)
    adif = p.parse()

    assert len(adif.qsos) == 1
    assert adif.qsos[0].get('call') == 'YB5QZ'

    # bad gridsquare should be corrupt and skip next field
    assert adif.qsos[0].get('gridsquare') != 'OJ00'
    assert adif.qsos[0].get('mode') is None
    assert adif.qsos[0].get('rst_sent') == '-02'
