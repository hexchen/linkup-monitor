#!/usr/bin/env python3

from linkup import linkup
import time
from prometheus_client import start_http_server, Gauge
import sys
import yaml
import logging

logging.basicConfig(
    level=logging.INFO,
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
)

if __name__ == '__main__':
    
    with open('linkup_config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    unit = "mmol/L" if config['measurement']['unit'] == 0 else "mg/dL"
    glucoseGauge = Gauge('glucose_measurement', f'glucose measurement in {unit}')
    boundaryGauge = Gauge('glucose_measurement_out_of_boundaries', 'glucose measurement is high or low')
    
    llu = linkup(config)
    llu.fetch_and_set_token()
    
    logging.debug("get patient id")
    patient_id = llu.get_patient_id()
    
    # Start up the server to expose the prometheus metrics
    start_http_server(8000)

    logging.info("fetch GCM data")
    try:
        while True:
            gm = llu.get_gcm_data(patient_id)
            glucoseGauge.set(gm['Value'])
            boundaryGauge.set(1 if gm['isHigh'] else -1 if gm['isLow'] else 0)
            logging.info(f"Value: {gm['Value']} {gm['Unit']} ({gm['Timestamp']})")
            time.sleep(60)
    except KeyboardInterrupt:
        logging.debug("\nexit")
        sys.exit(0)
