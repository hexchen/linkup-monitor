#!/usr/bin/env python3
# libre linkup client 

import requests 
import json
import hashlib

class linkup:
    
    def __init__(self, config):
        self.URL = 'https://api-de.libreview.io'
        self.HEADERS = {
            'accept': '*/*',
            'pragma': 'no-cache',
            'accept-encoding': 'gzip',
            'cache-control': 'no-cache',
            'connection': 'Keep-Alive',
            'content-type': 'application/json',
            'product': 'llu.android',
            'version': '4.12.0',
            'accept-language': 'de-DE,de;q=0.9',
            'account-id': config['auth']['account-id'] if config['auth']['account-id'] else '',
            'authorization': f"Bearer {config['auth']['token']}" if config['auth']['token'] else ''
        }
        self.AUTH = {
            'email': config['auth']['email'] if config['auth']['email'] else '',
            'password': config['auth']['password'] if config['auth']['password'] else ''
        }
        self.unit = config['measurement']['unit'] if config['measurement']['unit'] else 0

    def fetch_and_set_token(self):
        if self.HEADERS['authorization']:
            print("re-using token")
            return
        
        if not self.AUTH['email'] or not self.AUTH['password']:
            raise Exception("no credentials set")
        
        resp = requests.post(f"{self.URL}/llu/auth/login", json=self.AUTH, headers=self.HEADERS)
        resp.raise_for_status()
        
        data = resp.json()
        token = data['data']['authTicket']['token']
        self.HEADERS['authorization'] = f"Bearer {token}"
        
        user_id = data['data']['user']['id']
        account_id = hashlib.sha256()
        account_id.update(bytes(user_id, 'utf-8'))
        account_id = account_id.hexdigest()
        self.HEADERS['account-id'] = account_id


    def get_patient_id(self):
        resp = requests.get(f"{self.URL}/llu/connections", headers=self.HEADERS)
        resp.raise_for_status()
        
        patient_id = resp.json()['data'][0]['patientId']
        
        return patient_id

    def get_gcm_data(self, patient_id):
        resp = requests.get(f"{self.URL}/llu/connections/{patient_id}/graph", headers=self.HEADERS)
        resp.raise_for_status()
        
        gm = resp.json()['data']['connection']['glucoseMeasurement']
        return {
            'Value': gm['Value'] if self.unit == 0 else gm['ValueInMgPerDl'], 
            'Timestamp': gm['Timestamp'],
            'Unit': 'mmol/L' if self.unit == 0 else 'mg/dL',
            'isHigh': gm['isHigh'],
            'isLow': gm['isLow']
        }
        
        
        


