#include "bme680.h"
#include <stdio.h>
#include <string.h>

struct bme680_dev gas_sensor;

uint8_t coeff1[25] = {
	192,  108,  103,  3,    47,   80,   144,  236,
	214,  88,   255,  42,   30,   169,  255,  54,
	30,   0,    0,    199,  239,  69,   248,  30,
	1
};
uint8_t coeff2[16] = {
		  64,   206,  39,   0,    45,   20,   120,
	156,  24,   102,  142,  171,  226,  18,   16,
	0
};

int8_t user_i2c_read(uint8_t dev_id, uint8_t reg_addr, uint8_t *data, uint16_t len){
	switch(reg_addr){
		case BME680_CHIP_ID_ADDR:
			data[0] = BME680_CHIP_ID;
			return BME680_OK;

		case BME680_COEFF_ADDR1:
			memcpy(data, coeff1, len);
			return BME680_OK;
			
		case BME680_COEFF_ADDR2:
			memcpy(data, coeff2, len);
			return BME680_OK;
	}
	return 0;
}

int8_t user_i2c_write(uint8_t dev_id, uint8_t reg_addr, uint8_t *data, uint16_t len){
	return 0;
}

void user_delay_ms(uint32_t period){
	return;
}

int main(){
	gas_sensor.dev_id = BME680_I2C_ADDR_PRIMARY;
	gas_sensor.intf = BME680_I2C_INTF;
	gas_sensor.read = user_i2c_read;
	gas_sensor.write = user_i2c_write;
	gas_sensor.delay_ms = user_delay_ms;

	int8_t rslt = BME680_OK;
	rslt = bme680_init(&gas_sensor);
	if(rslt == BME680_OK){
		printf("CHIP OK\n");
		printf("%d\n",gas_sensor.calib.par_t1);
		printf("%d\n",gas_sensor.calib.par_t2);
	}

	uint8_t buff[15] = {128,0,  79,186,144,  122,185,64,    76,59,      128,0,0,   220,120};

	uint32_t adc_pres = (uint32_t) (((uint32_t) buff[2] * 4096) | ((uint32_t) buff[3] * 16) | ((uint32_t) buff[4] / 16));
	uint32_t adc_temp = (uint32_t) (((uint32_t) buff[5] * 4096) | ((uint32_t) buff[6] * 16) | ((uint32_t) buff[7] / 16));
	uint16_t adc_hum = (uint16_t) (((uint32_t) buff[8] * 256) | (uint32_t) buff[9]);
	uint16_t adc_gas_res = (uint16_t) ((uint32_t) buff[13] * 4 | (((uint32_t) buff[14]) / 64));
	uint8_t gas_range = buff[14] & BME680_GAS_RANGE_MSK;

	printf("%d\n",calc_temperature(adc_temp, &gas_sensor));
	printf("%d\n",calc_pressure(adc_pres, &gas_sensor));
}
