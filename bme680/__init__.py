from .constants import *
import math
import smbus
import time

class BME680(BME680Data):
    def __init__(self, i2c_addr=I2C_ADDR_PRIMARY, i2c_device=None):
        BME680Data.__init__(self)

        self.i2c_addr = i2c_addr
        self._i2c = i2c_device
        if self._i2c is None:
            self._i2c = smbus.SMBus(1)

        self.chip_id = self._get_regs(CHIP_ID_ADDR, 1)
        if self.chip_id != CHIP_ID:
            raise RuntimeError("BME680 Not Found. Invalid CHIP ID: 0x{0:02x}".format(self.chip_id))

        self.soft_reset()
        self.set_power_mode(SLEEP_MODE)

        self._get_calibration_data()

        self.set_humidity_oversample(OS_2X)
        self.set_pressure_oversample(OS_4X)
        self.set_temperature_oversample(OS_8X)
        self.set_filter(FILTER_SIZE_3)
        self.set_gas_status(ENABLE_GAS_MEAS)

        self.get_sensor_data()

    def soft_reset(self):
        self._set_regs(SOFT_RESET_ADDR, SOFT_RESET_CMD) 
        time.sleep(RESET_PERIOD / 1000.0)

    def set_humidity_oversample(self, value):
        self.tph_settings.os_hum = value
        temp = self._get_regs(CONF_OS_H_ADDR, 1)
        temp &= ~OSH_MSK
        temp |= value << OSH_POS
        self._set_regs(CONF_OS_H_ADDR, temp)

    def set_pressure_oversample(self, value):
        self.tph_settings.os_pres = value
        temp = self._get_regs(CONF_T_P_MODE_ADDR, 1)
        temp &= ~OSP_MSK
        temp |= value << OSP_POS
        self._set_regs(CONF_T_P_MODE_ADDR, temp)

    def set_temperature_oversample(self, value):
        self.tph_settings.os_temp = value
        temp = self._get_regs(CONF_T_P_MODE_ADDR, 1)
        temp &= ~OST_MSK
        temp |= value << OST_POS
        self._set_regs(CONF_T_P_MODE_ADDR, temp)

    def set_filter(self, value):
        self.tph_settings.filter = value
        temp = self._get_regs(CONF_ODR_FILT_ADDR, 1)
        temp &= ~FILTER_MSK
        temp |= value << FILTER_POS
        self._set_regs(CONF_ODR_FILT_ADDR, temp)

    def set_gas_status(self, value):
        temp = self._get_regs(CONF_ODR_RUN_GAS_NBC_ADDR, 1)
        temp &= ~RUN_GAS_MSK
        temp |= (value << RUN_GAS_POS)
        self.gas_settings.run_gas = value
        self._set_regs(CONF_ODR_RUN_GAS_NBC_ADDR, temp)

    def set_gas_heater_temperature(self, value):
        self.gas_settings.heatr_temp = value
        temp = self._calc_heater_resistance(self.gas_settings.heatr_temp)
        self._set_regs(RES_HEAT0_ADDR, temp)

    def set_gas_heater_duration(self, value):
        self.gas_settings.heatr_dur = value
        temp = self._calc_heater_duration(self.gas_settings.heatr_dur)
        self._set_regs(GAS_WAIT0_ADDR, temp)

    def set_power_mode(self, value, blocking=True):
        if value not in (SLEEP_MODE, FORCED_MODE):
            print("Power mode should be one of SLEEP_MODE or FORCED_MODE")

        self.power_mode = value

        temp = self._get_regs(CONF_T_P_MODE_ADDR, 1)
        temp &= ~ MODE_MSK
        temp |= self.power_mode
        self._set_regs(CONF_T_P_MODE_ADDR, temp)

        while blocking and self.get_power_mode() != self.power_mode:
            time.sleep(POLL_PERIOD_MS / 1000.0)

    def get_power_mode(self):
        self.power_mode = self._get_regs(CONF_T_P_MODE_ADDR, 1)
        return self.power_mode

    def set_profile_duration(self, duration):
        pass

    def get_profile_duration(self):
        pass

    def get_sensor_data(self):
        self.set_power_mode(FORCED_MODE)
        tries = 10

        for x in range(10):
            regs = self._get_regs(FIELD0_ADDR, FIELD_LENGTH)

            self.data.status = regs[0] & NEW_DATA_MSK
            self.data.gas_index = regs[0] & GAS_INDEX_MSK
            self.data.meas_index = regs[1]

            adc_pres = (regs[2] << 12) | (regs[3] << 4) | (regs[4] >> 4)
            adc_temp = (regs[5] << 12) | (regs[6] << 4) | (regs[7] >> 4)
            adc_hum = (regs[8] << 8) | regs[9]
            adc_gas_res = (regs[13] << 2) | (regs[14] >> 6)
            gas_range = regs[14] & GAS_RANGE_MSK

            self.data.status |= regs[14] & GASM_VALID_MSK
            self.data.status |= regs[14] & HEAT_STAB_MSK

            self.data.heat_stable = (self.data.status & HEAT_STAB_MSK) > 0

            if self.data.status & NEW_DATA_MSK:
                temperature = self._calc_temperature(adc_temp)
                self.data.temperature = temperature / 100.0
                self.ambient_temperature = temperature # Saved for heater calc

                self.data.pressure = self._calc_pressure(adc_pres) / 1000.0
                self.data.humidity = self._calc_humidity(adc_hum) / 1000.0
                self.data.gas_resistance = self._calc_gas_resistance(adc_gas_res, gas_range)
                return True
            else:
                time.sleep(POLL_PERIOD_MS / 1000.0)

        return False

    def _set_regs(self, register, value):
        if isinstance(value, int):
            self._i2c.write_byte_data(self.i2c_addr, register, value)
        else:
            self._i2c.write_i2c_block_data(self.i2c_addr, register, value)

    def _get_regs(self, register, length):
        if length == 1:
            return self._i2c.read_byte_data(self.i2c_addr, register)
        else:
            return self._i2c.read_i2c_block_data(self.i2c_addr, register, length)

    def _get_calibration_data(self):
        calibration = self._get_regs(COEFF_ADDR1, COEFF_ADDR1_LEN)
        calibration += self._get_regs(COEFF_ADDR2, COEFF_ADDR2_LEN)

        heat_range = self._get_regs(ADDR_RES_HEAT_RANGE_ADDR, 1)
        heat_value = twos_comp(self._get_regs(ADDR_RES_HEAT_VAL_ADDR, 1), bits=8)
        sw_error = twos_comp(self._get_regs(ADDR_RANGE_SW_ERR_ADDR, 1), bits=8)

        self.calibration_data.set_from_array(calibration)
        self.calibration_data.set_other(heat_range, heat_value, sw_error)
        
    def _calc_temperature(self, temperature_adc):
        var1 = (temperature_adc / 8) - (self.calibration_data.par_t1 * 2)
        var2 = (var1 * self.calibration_data.par_t2) / 2048
        var3 = ((var1 / 2) * (var1 / 2)) / 4096
        var3 = ((var3) * (self.calibration_data.par_t3 * 16)) / 16384

        # Save teperature data for pressure calculations
        self.calibration_data.t_fine = (var2 + var3)
        calc_temp = (((self.calibration_data.t_fine * 5) + 128) / 256)

        return calc_temp

    def _calc_pressure(self, pressure_adc):
        var1 = (self.calibration_data.t_fine / 2) - 64000
        var2 = ((var1 / 4) * (var1 / 4)) / 2048
        var2 = (var2 * self.calibration_data.par_p6) / 4
        var2 = var2 + ((var1 * self.calibration_data.par_p5) * 2)
        var2 = (var2 / 4) + (self.calibration_data.par_p4 * 65536)
        
        var1 = ((var1 / 4) * (var1 / 4)) / 8192
        var1 = ((var1 * (self.calibration_data.par_p3 * 32)) / 8) + ((self.calibration_data.par_p2 * var1) / 2)
        var1 = var1 / 262144
        var1 = ((32768 + var1) * self.calibration_data.par_p1) / 32768
        calc_pres = 1048576 - pressure_adc
        calc_pres = (calc_pres - (var2 / 4096)) * 3125
        calc_pres = (calc_pres / var1) * 2
        var1 = (self.calibration_data.par_p9 * (((calc_pres / 8) * (calc_pres / 8)) / 8192)) / 4096
        var2 = ((calc_pres / 4) * self.calibration_data.par_p8) / 8192
        var3 = ((calc_pres / 256)
                * (calc_pres / 256)
                * (calc_pres / 256)
                * self.calibration_data.par_p10) / 131072
        calc_pres = calc_pres + ((var1 + var2 + var3 + (self.calibration_data.par_p7 * 128)) / 16)

        return calc_pres

    def _calc_humidity(self, humidity_adc):
        temp_scaled = ((self.calibration_data.t_fine * 5) + 128) / 256
        var1 = (humidity_adc - ((self.calibration_data.par_h1 * 16))) \
                - (((temp_scaled * self.calibration_data.par_h3) / (100)) / 2)
        var2 = (self.calibration_data.par_h2
                * (((temp_scaled * self.calibration_data.par_h4) / (100))
                + (((temp_scaled * ((temp_scaled * self.calibration_data.par_h5) / (100))) / 64)
                / (100)) + (1 * 16384))) / 1024
        var3 = var1 * var2
        var4 = self.calibration_data.par_h6 * 128
        var4 = ((var4) + ((temp_scaled * self.calibration_data.par_h7) / (100))) / 16
        var5 = ((var3 / 16384) * (var3 / 16384)) / 1024
        var6 = (var4 * var5) / 2
        calc_hum = (((var3 + var6) / 1024) * (1000)) / 4096

        return min(max(calc_hum,0),100000)

    def _calc_gas_resistance(self, gas_res_adc, gas_range):
        var1 = ((1340 + (5 * self.calibration_data.range_sw_err)) * (lookupTable1[gas_range])) / 65536
        var2 = (((gas_res_adc * 32768) - (16777216)) + var1)
        var3 = ((lookupTable2[gas_range] * var1) / 512)
        calc_gas_res = ((var3 + (var2 / 2)) / var2)

        return calc_gas_res

    def _calc_heater_resistance(self, temperature):
        temperature = min(max(temperature,200),400)

        var1 = ((self.ambient_temperature * self.calibration_data.par_gh3) / 1000) * 256
        var2 = (self.calibration_data.par_gh1 + 784) * (((((self.calibration_data.par_gh2 + 154009) * temperature * 5) / 100) + 3276800) / 10)
        var3 = var1 + (var2 / 2)
        var4 = (var3 / (self.calibration_data.res_heat_range + 4))
        var5 = (131 * self.calibration_data.res_heat_val) + 65536
        heatr_res_x100 = (((var4 / var5) - 250) * 34)
        heatr_res = ((heatr_res_x100 + 50) / 100)

        return int(heatr_res)

    def _calc_heater_duration(self, duration):
        if duration < 0xfc0:
            factor = 0

            while duration > 0x3f:
                duration /= 4
                factor += 1

            return int(duration + (factor * 64))

        return 0xff
