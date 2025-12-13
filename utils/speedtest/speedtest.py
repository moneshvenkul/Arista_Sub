import json
import subprocess
import os
import tempfile

def test_config(config_file):
    try:
        result = subprocess.run(['speedtest', '--accept-license', '--accept-gdpr', 
                               '--format=json', '--progress=no'],
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return {
                'success': True,
                'latency': data.get('ping', {}).get('latency', 9999),
                'download': data.get('download', {}).get('bandwidth', 0) / 125000,
                'upload': data.get('upload', {}).get('bandwidth', 0) / 125000,
                'server': data.get('server', {}).get('name', 'Unknown')
            }
    except:
        pass
    
    return {'success': False, 'latency': 9999, 'download': 0, 'upload': 0}
