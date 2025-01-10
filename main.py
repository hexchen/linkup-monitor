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


glucoseGauge = Gauge('glucose_measurement', 'glucose measurement in mmol/L')

if __name__ == '__main__':
    # Start up the server to expose the prometheus metrics
    start_http_server(8000)
    
    with open('linkup_config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    llu = linkup(config)
    llu.fetch_and_set_token()
    
    logging.debug("get patient id")
    patient_id = llu.get_patient_id()

    logging.info("fetch GCM data")
    try:
        while True:
            gm = llu.get_gcm_data(patient_id)
            glucoseGauge.set(gm['Value'])
            logging.info(f"Value: {gm['Value']} {gm['Unit']} ({gm['Timestamp']})")
            time.sleep(60)
    except KeyboardInterrupt:
        logging.debug("\nexit")
        sys.exit(0)
