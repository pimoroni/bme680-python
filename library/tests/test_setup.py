import sys
import mock
import pytest
import bme680


class MockSMBus:
    """Mock a basic non-presence SMBus device to cause BME680 to fail.

    Returns 0 in all cases, so that CHIP_ID will never match.

    """

    def __init__(self, bus):  # noqa D107
        pass

    def read_byte_data(self, addr, register):
        """Return 0 for all read attempts."""
        return 0


class MockSMBusPresent:
    """Mock enough of the BME680 for the library to initialise and test."""

    def __init__(self, bus):
        """Initialise with test data."""
        self.regs = [0 for _ in range(256)]
        self.regs[bme680.CHIP_ID_ADDR] = bme680.CHIP_ID

    def read_byte_data(self, addr, register):
        """Read a single byte from fake registers."""
        return self.regs[register]

    def write_byte_data(self, addr, register, value):
        """Write a single byte to fake registers."""
        self.regs[register] = value

    def read_i2c_block_data(self, addr, register, length):
        """Read up to length bytes from register."""
        return self.regs[register:register + length]


def test_setup_not_present():
    """Mock the adbsence of a BME680 and test initialisation."""
    sys.modules['smbus'] = mock.MagicMock()
    sys.modules['smbus'].SMBus = MockSMBus

    with pytest.raises(RuntimeError):
        sensor = bme680.BME680()  # noqa F841


def test_setup_mock_present():
    """Mock the presence of a BME680 and test initialisation."""
    sys.modules['smbus'] = mock.MagicMock()
    sys.modules['smbus'].SMBus = MockSMBusPresent

    sensor = bme680.BME680()  # noqa F841
