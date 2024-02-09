import pytest
import bme680


def test_setup_not_present(smbus_notpresent):
    """Mock the adbsence of a BME680 and test initialisation."""
    with pytest.raises(RuntimeError):
        sensor = bme680.BME680()  # noqa F841


def test_setup_mock_present(smbus):
    """Mock the presence of a BME680 and test initialisation."""
    sensor = bme680.BME680()  # noqa F841
