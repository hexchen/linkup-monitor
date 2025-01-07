#!/usr/bin/env python3

from linkup import linkup
import time
from prometheus_client import start_http_server, Gauge
import sys
import yaml

glucoseGauge = Gauge('glucose_measurement', 'glucose measurement in mmol/L')

# todo containerize
# todo deploy to raspi4

if __name__ == '__main__':
    # Start up the server to expose the prometheus metrics
    start_http_server(8000)
    
    with open('linkup_config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    llu = linkup(config)
    llu.fetch_and_set_token()
    
    print("get patient id")
    patient_id = llu.get_patient_id()

    print("fetch GCM data")
    try:
        while True:
            gm = llu.get_gcm_data(patient_id)
            glucoseGauge.set(gm['Value'])
            print(f"Value: {gm['Value']} mmol/L ({gm['Timestamp']})")
            time.sleep(60)
    except KeyboardInterrupt:
        print("\nbye")
        sys.exit(0)
