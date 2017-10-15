from . import constants
import math

class BME680(constants.BME680):
    def __init__(self):
        constants.BME680.__init__(self)

    def init(self):
        pass

    def soft_reset(self):
        pass

    def set_sensor_mode(self):
        pass

    def get_sensor_mode(self, mode):
        pass

    def set_profile_duration(self, duration):
        pass

    def get_profile_duration(self):
        pass

    def _get_sensor_data(self):
        pass

    def _get_regs(self, addr, length):
        pass

    def _get_calibration_data(self):
        calibration = self._get_regs(constants.COEFF_ADDR1, constants.COEFF_ADDR1_LEN)
        calibration += self._get_regs(constants.COEFF_ADDR2, constants.COEFF_ADDR2_LEN)

        heat_range = self._get_regs(constants.ADDR_RES_HEAT_RANGE_ADDR, 1)[0]
        heat_value = self._get_regs(constants.ADDR_RES_HEAT_VAL_ADDR, 1)[0]
        sw_error = self._get_regs(constants.ADDR_RANGE_SW_ERR_ADDR, 1)[0]

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
        var1 = ((1340 + (5 * self.calibration_data.range_sw_err)) * (constants.lookupTable1[gas_range])) / 65536
        var2 = (((gas_res_adc * 32768) - (16777216)) + var1)
        var3 = ((constants.lookupTable2[gas_range] * var1) / 512)
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
