#!/usr/bin/env python3

from linkup import linkup
import time
from prometheus_client import start_http_server, Gauge
from datetime import datetime
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
    glucoseGauge = Gauge('glucose_measurement', f'glucose measurement in {unit}', ['name'])
    glucoseTrend = Gauge('glucose_trend', 'glucose trend', ['name'])
    boundaryGauge = Gauge('glucose_measurement_out_of_boundaries', 'glucose measurement is high or low', ['name'])
    updatedGauge = Gauge('glucose_updated', 'last update received at', ['name'])
    
    llu = linkup(config)
    llu.fetch_and_set_token()

    patients = llu.get_patients()

    # Start up the server to expose the prometheus metrics
    start_http_server(8000)

    logging.info("fetch GCM data")
    try:
        while True:
            for patient in patients:
                gm = llu.get_gcm_data(patient['id'])
                glucoseGauge.labels(name=patient['name']).set(gm['Value'])
                boundaryGauge.labels(name=patient['name']).set(1 if gm['isHigh'] else -1 if gm['isLow'] else 0)
                timestamp = datetime.strptime(gm['Timestamp'], '%m/%d/%Y %I:%M:%S %p').timestamp()
                updatedGauge.labels(name=patient['name']).set(int(timestamp))
                glucoseTrend.labels(name=patient['name']).set(gm['Trend'])
                logging.info(f"Value ({patient['name']}): {gm['Value']} {gm['Unit']} ({gm['Timestamp']})")
            time.sleep(60)
    except KeyboardInterrupt:
        logging.debug("\nexit")
        sys.exit(0)
