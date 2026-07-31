from app.crc import crc8_sae_j1850
import pytest

def test_crc_returns_int():
    result = crc8_sae_j1850(b'2')
    assert isinstance(result, int)

def test_crc_range():
    result = crc8_sae_j1850(b'2')
    assert 0 <= result <= 255

def test_crc_same_data_returns_same_crc():
    crc1 = crc8_sae_j1850(b'2')
    crc2 = crc8_sae_j1850(b'2')
    assert crc1 == crc2

def test_crc_packet():
    data = bytes.fromhex("07 E8 08 00 01 02 03 04 05 06 07")
    crc  = crc8_sae_j1850(data)
    assert crc  == 0xC0

def test_crc_change_byte():
    data1 = bytes.fromhex("07 E8 08 00 01 02 03 04 05 06 07")
    crc1 = crc8_sae_j1850(data1)
    data2 = bytes.fromhex("07 E8 08 00 01 02 03 04 05 06 08")
    crc2 = crc8_sae_j1850(data2)
    assert crc1 != crc2

def test_crc_empty_data():
    result = crc8_sae_j1850(b"")
    assert result == 0

def test_crc_one_byte():
    result = crc8_sae_j1850(b"1")
    assert result == 0x6C

def test_crc_more_byte():
    result = crc8_sae_j1850(bytes(range(256)))
    assert result == 0x05

def test_crc_none():
    with pytest.raises(TypeError):
        crc8_sae_j1850(None)

def test_crc_int():
    with pytest.raises(TypeError):
        crc8_sae_j1850(123)

def test_crc_str():
    with pytest.raises(TypeError):
        crc8_sae_j1850('abc')