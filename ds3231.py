import utime

class DS3231:
    def __init__(self, i2c, address=0x68):
        self.i2c = i2c
        self.address = address

    def _bcd2dec(self, bcd):
        return (bcd // 16) * 10 + (bcd % 16)

    def _dec2bcd(self, dec):
        return (dec // 10) * 16 + (dec % 10)

    def get_time(self):
        data = self.i2c.readfrom_mem(self.address, 0x00, 7)
        seconds = self._bcd2dec(data[0] & 0x7F)
        minutes = self._bcd2dec(data[1])
        hours = self._bcd2dec(data[2] & 0x3F)
        day = self._bcd2dec(data[4])
        month = self._bcd2dec(data[5] & 0x1F)
        year = self._bcd2dec(data[6]) + 2000
        return (year, month, day, hours, minutes, seconds)

    def set_time(self, datetime):
        year, month, day, hours, minutes, seconds, _, _ = datetime
        self.i2c.writeto_mem(self.address, 0x00, bytes([
            self._dec2bcd(seconds),
            self._dec2bcd(minutes),
            self._dec2bcd(hours),
            0,  # weekday not used
            self._dec2bcd(day),
            self._dec2bcd(month),
            self._dec2bcd(year - 2000)
        ]))

    def get_temperature(self):
        data = self.i2c.readfrom_mem(self.address, 0x11, 2)
        temp_msb = data[0]
        temp_lsb = data[1]
        temp = temp_msb + ((temp_lsb >> 6) * 0.25)
        return temp
