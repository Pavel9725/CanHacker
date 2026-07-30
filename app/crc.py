def crc8_sae_j1850(data: bytes) -> int:
    crc = 0xFF
    poly = 0x1D

    for byte in data:
        crc ^= byte

        for _ in range(8):
            if crc & 0x80:
                crc = ((crc << 1) ^ poly) & 0xFF
            else:
                crc = (crc << 1) & 0xFF

    return crc ^ 0xFF