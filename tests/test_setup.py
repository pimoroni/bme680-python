import pytest

import bme680


def test_setup_not_present(smbus_notpresent):
    """Mock the adbsence of a BME680 and test initialisation."""
    with pytest.raises(RuntimeError):
        sensor = bme680.BME680()  # noqa F841


def test_setup_mock_present(smbus):
    """Mock the presence of a BME680 and test initialisation."""
    sensor = bme680.BME680()  # noqa F841


def test_gas_valid_and_heat_stable_flags(smbus, calibration):
    """Validate that gasm_valid and heat_stab are unpacked from field 0."""
    sensor = bme680.BME680()
    sensor.calibration_data = calibration

    sensor._i2c.regs[bme680.FIELD0_ADDR] = bme680.NEW_DATA_MSK
    sensor._i2c.regs[bme680.FIELD0_ADDR + 14] = 0
    assert sensor.get_sensor_data() is True
    assert sensor.data.gas_valid is False
    assert sensor.data.heat_stable is False

    sensor._i2c.regs[bme680.FIELD0_ADDR + 14] = bme680.GASM_VALID_MSK | bme680.HEAT_STAB_MSK
    assert sensor.get_sensor_data() is True
    assert sensor.data.gas_valid is True
    assert sensor.data.heat_stable is True


def test_get_power_mode_masks_register(smbus):
    """Validate that get_power_mode returns only the mode bits."""
    sensor = bme680.BME680()

    sensor.set_temperature_oversample(bme680.OS_8X)
    sensor.set_pressure_oversample(bme680.OS_4X)
    sensor.set_power_mode(bme680.FORCED_MODE)

    assert sensor._i2c.regs[bme680.CONF_T_P_MODE_ADDR] & ~bme680.MODE_MSK != 0
    assert sensor.get_power_mode() == bme680.FORCED_MODE


def test_set_power_mode_forced_does_not_hang(smbus):
    """Validate that setting FORCED_MODE returns when the sensor self-clears to sleep."""
    sensor = bme680.BME680()

    original = type(sensor._i2c).read_byte_data

    def read_byte_data(self, addr, register):
        value = original(self, addr, register)
        if register == bme680.CONF_T_P_MODE_ADDR:
            value &= ~bme680.MODE_MSK
        return value

    type(sensor._i2c).read_byte_data = read_byte_data
    try:
        sensor.set_power_mode(bme680.FORCED_MODE)
        assert sensor.get_power_mode() == bme680.SLEEP_MODE
    finally:
        type(sensor._i2c).read_byte_data = original


def test_set_power_mode_sleep_waits(smbus):
    """Validate that setting SLEEP_MODE polls until the sensor reports sleep."""
    sensor = bme680.BME680()

    sensor.set_power_mode(bme680.SLEEP_MODE)
    assert sensor.get_power_mode() == bme680.SLEEP_MODE
