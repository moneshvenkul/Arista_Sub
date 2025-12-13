import requests
import json
import re
import hashlib
import base64
from datetime import datetime
import os
import subprocess
import tempfile
import yaml
import concurrent.futures
import time

SOURCES = [
    "https://raw.githubusercontent.com/Mosifree/-FREE2CONFIG/refs/heads/main/Reality",
    "https://cdn.jsdelivr.net/gh/Rayan-Config/C-Sub@main/configs/proxy.txt",
    "https://cdn.jsdelivr.net/gh/MahsaNetConfigTopic/config@main/xray_final.txt",
    "https://cdn.jsdelivr.net/gh/4n0nymou3/multi-proxy-config-fetcher@main/configs/proxy_configs.txt",
    "https://cdn.jsdelivr.net/gh/miladtahanian/V2RayCFGDumper@main/config.txt",
    "https://cdn.jsdelivr.net/gh/parvinxs/Submahsanetxsparvin@main/Sub.mahsa.xsparvin",
    "https://raw.githubusercontent.com/parvinxs/Fssociety/refs/heads/main/Fssociety.sub",
    "https://raw.githubusercontent.com/Firmfox/Proxify/refs/heads/main/v2ray_configs/seperated_by_protocol/other.txt"
]

def get_configs_from_url(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, timeout=15, headers=headers)
        response.raise_for_status()
        return response.text
    except:
        return ""

def extract_configs(content):
    patterns = [
        r'(vmess://[A-Za-z0-9+/=]+)',
        r'(vless://[^\s]+)',
        r'(trojan://[^\s]+)',
        r'(ss://[A-Za-z0-9+/=]+)',
        r'(ss://[A-Za-z0-9\-._~]+#?[^\s]*)',
        r'(hysteria2://[^\s]+)',
        r'(hysteria://[^\s]+)',
        r'(hy2://[^\s]+)',
        r'(tuic://[^\s]+)',
        r'(wg\+?[^:]*://[^\s]+)'
    ]
    configs = []
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        configs.extend(matches)
    return configs

def decode_base64_if_needed(config):
    if config.startswith('vmess://'):
        try:
            base64_part = config[8:]
            if len(base64_part) % 4 != 0:
                base64_part += '=' * (4 - len(base64_part) % 4)
            decoded = base64.b64decode(base64_part).decode('utf-8')
            return json.loads(decoded)
        except:
            return None
    elif config.startswith('ss://'):
        try:
            if '#' in config:
                parts = config.split('#')
                encoded = parts[0][5:]
                if len(encoded) % 4 != 0:
                    encoded += '=' * (4 - len(encoded) % 4)
                decoded = base64.b64decode(encoded).decode('utf-8')
                return f"ss://{decoded}#{parts[1]}"
        except:
            pass
    return config

def validate_config(config):
    if isinstance(config, str):
        if config.startswith('vmess://'):
            decoded = decode_base64_if_needed(config)
            if not decoded or not isinstance(decoded, dict):
                return False
            required_keys = ['v', 'ps', 'add', 'port', 'id', 'aid']
            if not all(key in decoded for key in required_keys):
                return False
            if not isinstance(decoded['port'], int) or decoded['port'] < 1 or decoded['port'] > 65535:
                return False
            if len(decoded['id']) != 36:
                return False
        elif config.startswith('vless://'):
            if '?' not in config or '#' not in config:
                return False
        elif config.startswith('trojan://'):
            if '@' not in config or '#' not in config:
                return False
        elif config.startswith('ss://'):
            if '@' not in config and ':' not in config.split('#')[0][5:]:
                return False
    return True

def generate_new_tag(config, new_tag="ARISTA🔥"):
    if isinstance(config, dict) and 'ps' in config:
        config['ps'] = new_tag
        return config
    elif isinstance(config, str):
        if '#' in config:
            base, old_tag = config.split('#', 1)
            return f"{base}#{new_tag}"
        else:
            return f"{config}#{new_tag}"
    return config

def encode_to_base64(config):
    if isinstance(config, dict):
        json_str = json.dumps(config, separators=(',', ':'))
        return 'vmess://' + base64.b64encode(json_str.encode()).decode()
    return config

def categorize_configs(configs):
    categories = {
        'vmess': [],
        'vless': [],
        'trojan': [],
        'ss': [],
        'hysteria2': [],
        'hysteria': [],
        'tuic': [],
        'wireguard': [],
        'other': []
    }
    
    for config in configs:
        if isinstance(config, str):
            if config.startswith('vmess://'):
                categories['vmess'].append(config)
            elif config.startswith('vless://'):
                categories['vless'].append(config)
            elif config.startswith('trojan://'):
                categories['trojan'].append(config)
            elif config.startswith('ss://'):
                categories['ss'].append(config)
            elif config.startswith('hysteria2://') or config.startswith('hy2://'):
                categories['hysteria2'].append(config)
            elif config.startswith('hysteria://'):
                categories['hysteria'].append(config)
            elif config.startswith('tuic://'):
                categories['tuic'].append(config)
            elif config.startswith('wg'):
                categories['wireguard'].append(config)
            else:
                categories['other'].append(config)
    return categories

def deduplicate_configs(configs):
    unique_configs = []
    seen_hashes = set()
    for config in configs:
        if isinstance(config, str):
            config_hash = hashlib.md5(config.encode()).hexdigest()
            if config_hash not in seen_hashes:
                seen_hashes.add(config_hash)
                unique_configs.append(config)
    return unique_configs

def create_directories():
    directories = ['vmess', 'vless', 'trojan', 'ss', 'hysteria2', 'hysteria', 'tuic', 'wireguard', 'other', 'all', 'tested']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

def save_categorized_configs(categories):
    create_directories()
    total_configs = 0
    
    for category, configs in categories.items():
        if configs:
            file_path = f"{category}/configs.txt"
            content = f"# Category: {category}\n"
            content += f"# Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            content += f"# Count: {len(configs)}\n\n"
            content += "\n".join(configs)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            total_configs += len(configs)
    
    all_configs = []
    for configs in categories.values():
        all_configs.extend(configs)
    
    if all_configs:
        file_path = "all/configs.txt"
        content = f"# All Configurations\n"
        content += f"# Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        content += f"# Total Count: {len(all_configs)}\n\n"
        content += "\n".join(all_configs)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return total_configs

def convert_to_yaml(configs):
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
            tmp.write("\n".join(configs))
            tmp_path = tmp.name
        
        result = subprocess.run(['./subconverter/subconverter', '--url', tmp_path, '--template', 'template.yml', '--output', 'temp_output.yml'], 
                              capture_output=True, text=True, timeout=30)
        
        if os.path.exists('temp_output.yml'):
            with open('temp_output.yml', 'r') as f:
                yaml_content = yaml.safe_load(f)
            os.remove('temp_output.yml')
            os.remove(tmp_path)
            return yaml_content
    except:
        pass
    return None

def speedtest_single_config(config, index, total):
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
            tmp.write(config)
            tmp_path = tmp.name
        
        output_file = f"speedtest_result_{index}.json"
        result = subprocess.run(['./utils/speedtest/speedtest', '--config', tmp_path, '--output', output_file, '--timeout', '10'], 
                              capture_output=True, text=True, timeout=15)
        
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                result_data = json.load(f)
            os.remove(output_file)
            os.remove(tmp_path)
            
            if result_data.get('success', False):
                return {
                    'config': config,
                    'latency': result_data.get('latency', 9999),
                    'download': result_data.get('download', 0),
                    'upload': result_data.get('upload', 0)
                }
    except:
        pass
    
    os.remove(tmp_path) if os.path.exists(tmp_path) else None
    return None

def speedtest_configs(configs, max_workers=5, test_count=10):
    if len(configs) == 0:
        return []
    
    tested_configs = []
    test_sample = configs[:min(test_count, len(configs))]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for i, config in enumerate(test_sample):
            futures.append(executor.submit(speedtest_single_config, config, i, len(test_sample)))
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result and result['latency'] < 5000:
                tested_configs.append(result)
    
    tested_configs.sort(key=lambda x: x['latency'])
    return tested_configs[:5]

def save_tested_configs(tested_configs):
    if not tested_configs:
        return
    
    create_directories()
    
    best_configs = []
    summary_lines = []
    
    summary_lines.append("# Best Tested Configurations")
    summary_lines.append(f"# Tested: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    summary_lines.append("# Latency < 5000ms")
    summary_lines.append("")
    
    for i, data in enumerate(tested_configs):
        config = data['config']
        latency = data['latency']
        download = data.get('download', 0)
        upload = data.get('upload', 0)
        
        best_configs.append(config)
        
        summary_lines.append(f"# Config {i+1}:")
        summary_lines.append(f"# Latency: {latency}ms")
        if download > 0:
            summary_lines.append(f"# Download: {download:.2f} Mbps")
        if upload > 0:
            summary_lines.append(f"# Upload: {upload:.2f} Mbps")
        summary_lines.append(config)
        summary_lines.append("")
    
    file_path = "tested/best_configs.txt"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(summary_lines))
    
    yaml_content = convert_to_yaml(best_configs)
    if yaml_content:
        yaml_path = "tested/best_configs.yml"
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(yaml_content, f, default_flow_style=False, allow_unicode=True)
    
    return len(tested_configs)

def process_configs():
    all_configs = []
    
    for i, url in enumerate(SOURCES):
        content = get_configs_from_url(url)
        if content:
            configs = extract_configs(content)
            all_configs.extend(configs)
    
    processed_configs = []
    for config in all_configs:
        if config.startswith('vmess://'):
            decoded = decode_base64_if_needed(config)
            if decoded and isinstance(decoded, dict):
                if validate_config(decoded):
                    new_config = generate_new_tag(decoded)
                    encoded = encode_to_base64(new_config)
                    processed_configs.append(encoded)
            else:
                if validate_config(config):
                    processed_configs.append(config)
        else:
            if validate_config(config):
                new_config = generate_new_tag(config)
                processed_configs.append(new_config)
    
    unique_configs = deduplicate_configs(processed_configs)
    categories = categorize_configs(unique_configs)
    total_count = save_categorized_configs(categories)
    
    tested_count = 0
    best_configs = []
    for category, configs in categories.items():
        if configs and category in ['vmess', 'vless', 'trojan', 'ss']:
            tested = speedtest_configs(configs)
            best_configs.extend(tested)
    
    if best_configs:
        tested_count = save_tested_configs(best_configs)
    
    return categories, total_count, tested_count

def install_subconverter():
    if not os.path.exists('subconverter'):
        try:
            subprocess.run(['wget', '-O', 'subconverter.tar.gz', 
                          'https://github.com/tindy2013/subconverter/releases/download/v0.7.2/subconverter_linux64.tar.gz'], 
                         check=True)
            subprocess.run(['tar', '-zxvf', 'subconverter.tar.gz', '-C', '.'], check=True)
            subprocess.run(['chmod', '+x', './subconverter/subconverter'], check=True)
        except:
            pass

def install_speedtest():
    if not os.path.exists('utils/speedtest'):
        os.makedirs('utils/speedtest', exist_ok=True)
        try:
            subprocess.run(['wget', '-O', 'utils/speedtest/speedtest',
                          'https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-x86_64.tgz'], 
                         check=True)
            subprocess.run(['tar', '-xzf', 'utils/speedtest/speedtest', '-C', 'utils/speedtest'], check=True)
        except:
            pass

def main():
    print("Arista Config Fetcher & Tester")
    
    try:
        install_subconverter()
        install_speedtest()
        
        categories, total_count, tested_count = process_configs()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"configs_backup_{timestamp}.txt", 'w', encoding='utf-8') as f:
            f.write(f"# Backup: {timestamp}\n")
            f.write(f"# Total Configs: {total_count}\n")
            f.write(f"# Tested Configs: {tested_count}\n\n")
            for category, configs in categories.items():
                if configs:
                    f.write(f"\n# === {category.upper()} === #\n")
                    f.write("\n".join(configs))
                    f.write("\n")
        
        print(f"SUCCESS: Processed {total_count} configurations")
        print(f"SUCCESS: Tested and saved {tested_count} best configurations")
        print("Categories created:")
        for category, configs in categories.items():
            if configs:
                print(f"  {category}: {len(configs)} configs")
        
        if tested_count > 0:
            print(f"\nBest tested configs saved in: tested/best_configs.txt")
            print(f"YAML version saved in: tested/best_configs.yml")
                
    except Exception as e:
        print(f"ERROR: {e}")
        raise

if __name__ == "__main__":
    main()
