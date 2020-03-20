import sys
import mock
import pytest
import bme680
from bme680.constants import CalibrationData


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


@pytest.fixture(scope='function', autouse=False)
def smbus_notpresent():
    """Mock smbus module."""
    smbus = mock.MagicMock()
    smbus.SMBus = MockSMBus
    sys.modules['smbus'] = smbus
    yield smbus
    del sys.modules['smbus']


@pytest.fixture(scope='function', autouse=False)
def smbus():
    """Mock smbus module."""
    smbus = mock.MagicMock()
    smbus.SMBus = MockSMBusPresent
    sys.modules['smbus'] = smbus
    yield smbus
    del sys.modules['smbus']


@pytest.fixture(scope='function', autouse=False)
def calibration():
    """Mock bme680 calibration."""
    calibration = CalibrationData()
    # Dump of calibration data borrowed from:
    # https://github.com/pimoroni/bme680-python/issues/11
    data = {
        'par_gh1': -30,
        'par_gh2': -24754,
        'par_gh3': 18,
        'par_h1': 676,
        'par_h2': 1029,
        'par_h3': 0,
        'par_h4': 45,
        'par_h5': 20,
        'par_h6': 120,
        'par_h7': -100,
        'par_p1': 36673,
        'par_p10': 30,
        'par_p2': -10515,
        'par_p3': 88,
        'par_p4': 7310,
        'par_p5': -129,
        'par_p6': 30,
        'par_p7': 46,
        'par_p8': -3177,
        'par_p9': -2379,
        'par_t1': 26041,
        'par_t2': 26469,
        'par_t3': 3,
        'range_sw_err': 0,
        'res_heat_range': 1,
        'res_heat_val': 48,
        't_fine': 136667
    }
    for k, v in data.items():
        setattr(calibration, k, v)
    return calibration
