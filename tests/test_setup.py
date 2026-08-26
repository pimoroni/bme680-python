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
