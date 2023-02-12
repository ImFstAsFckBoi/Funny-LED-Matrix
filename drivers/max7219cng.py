from drivers.spi import SPI
from time import sleep


class max7219cng():
    """ Wrapper around an SPI connection to the
        max7219cng controller on the LED Matrix.
    """

    def __init__(self, clk: int,
                 cs: int,
                 mosi: int,
                 scan_limit: int = 7,
                 verbose=False):
        """Init connection max7219cng unit.

        Args:
            `clk` (int): GPIO pin to use at clock.
            `cs` (int): GPIO pin to use as chip select.
            `mosi` (int): GPIO pin to use as MOSI / DIN (Data In)
            `scan_limit` (int, optional): Number of columns to enable.
            Defaults to 7 (all).
            `verbose` (bool, optional): Enable verbose logging to stdout.
            Defaults to False.
        """
        self.__spi_conn = SPI(clk=clk,
                              cs=cs,
                              mosi=mosi,
                              miso=None,
                              verbose=verbose)

        # Zero out all registers
        for cmd in range(16):
            packet = cmd << 8
            self.write(packet)

        # Set the scan limit register
        self.write_str(f'1011{bin(scan_limit)[2:].zfill(8)}')

        # Disable shutdown register.
        self.write_str('110000000001')

    def __del__(self):
        # Re-enable shutdown register.
        self.write_str('110000000000')

    def write(self, packet: int):
        """Write a packet to the unit.

        Args:
            `packet` (int): 12 LSBs of an integer representing the packet.

        Raises:
            IndexError: To large to be a valid packet (more than 12 bits set).
        """
        # 4095 = 0b_1111_1111_1111 (max number with 12 LSB set)
        if packet > 4095:
            raise IndexError('Packets set bits must be 12 bits long.')

        self.__spi_conn.put(packet, 12)

    def write_str(self, string: str):
        """Write a packet represented as a string of 12 1:s and 0:s.

        Args:
            `string` (str): 12 bits (1:s and 0:s) to send.

        Raises:
            IndexError: To long string (> 12).
        """
        if len(string) != 12:
            raise IndexError("The packet string must be 12 bits (chars) long.")
        self.__spi_conn.put(int(string, 2), 12)

    def test(self, time_secs: int = 1):
        self.write_str('111100000001')
        sleep(time_secs)
        self.write_str('111100000000')
