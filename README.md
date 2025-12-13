📡 Arista Config Hub

<div align="center">

https://img.shields.io/github/actions/workflow/status/aristaproject/aristaproject/update-test-configs.yml?style=for-the-badge&label=Auto-Update
https://img.shields.io/github/last-commit/aristaproject/aristaproject?style=for-the-badge&color=blue
https://img.shields.io/badge/Configs-1000%2B-success?style=for-the-badge
https://img.shields.io/badge/License-MIT-green?style=for-the-badge

Professional Proxy Config Aggregator & Speed Tester

#quick-start
#configurations
#tested-configurations
#live-statistics

</div>

🌟 Features

<table>
<tr>
<td width="50%">

🔄 Auto Collection

· Hourly Updates from 8+ trusted sources
· Smart Deduplication with MD5 hashing
· Protocol Categorization (VMess, VLess, Trojan, etc.)
· Validation & Sanitization of all configs

</td>
<td width="50%">

⚡ Smart Testing

· Speed Test Integration with latency check
· Best 5 Configs automatic selection
· Clash-Compatible YAML output
· Real-time Performance monitoring

</td>
</tr>
<tr>
<td>

📁 Organized Storage

· Category Folders for each protocol
· Tested Configs separate directory
· Backup System with timestamps
· Multiple Formats (TXT, YAML)

</td>
<td>

🚀 Easy Integration

· One-Click Import for Clash
· Raw Configs for any client
· API-Ready structure
· GitHub Actions automation

</td>
</tr>
</table>

🚀 Quick Start

For Clash Users:

```yaml
# In Clash: Configuration → Import from URL
https://raw.githubusercontent.com/aristaproject/aristaproject/main/tested/best_configs.yml
```

For Manual Use:

```bash
# Get all VMess configs
curl -s https://raw.githubusercontent.com/aristaproject/aristaproject/main/vmess/configs.txt

# Get best tested configs
curl -s https://raw.githubusercontent.com/aristaproject/aristaproject/main/tested/best_configs.txt
```

📁 Directory Structure

```
arista-config-hub/
├── 📂 vmess/           # VMess configurations
├── 📂 vless/           # VLess configurations  
├── 📂 trojan/          # Trojan configurations
├── 📂 ss/              # Shadowsocks configurations
├── 📂 hysteria2/       # Hysteria 2.0 configurations
├── 📂 hysteria/        # Hysteria configurations
├── 📂 tuic/            # TUIC configurations
├── 📂 wireguard/       # WireGuard configurations
├── 📂 other/           # Other protocols
├── 📂 tested/          # 🏆 Tested & optimized configs
│   ├── best_configs.txt
│   └── best_configs.yml    # ⚡ For Clash
├── 📂 all/             # All configurations combined
├── 📂 .github/workflows/
│   ├── update-test-configs.yml      # Hourly updates
│   └── daily-full-test.yml          # Daily complete test
├── 📂 utils/speedtest/ # Speed testing tools
└── update_configs.py   # Main processing script
```

⚡ Tested Configurations

Latest Speed-Tested Configs:

```bash
# Best low-latency configs (updated hourly)
📁 tested/best_configs.yml    # For Clash
📁 tested/best_configs.txt    # Raw configs
```

Features:

· ✅ Latency < 5000ms verified
· ✅ Automatic speed testing
· ✅ Top 5 performers selected
· ✅ Ready for production use

📊 Live Statistics

Protocol Total Configs Tested Status Last Update
VMess Processing... ✅ Active Just now
VLess Processing... ✅ Active Just now
Trojan Processing... ✅ Active Just now
Shadowsocks Processing... ✅ Active Just now
Hysteria2 Processing... ⏳ Collecting Just now
TUIC Processing... ⏳ Collecting Just now

Last Full Test: 2025-12-13 01:45 UTC

🔧 How It Works

Workflow Timeline:

```
⏰ Every 1 Hour:
1. Fetch configs from 8+ sources
2. Validate & categorize by protocol
3. Speed test top configs
4. Select best 5 performers
5. Update repositories automatically

⏰ Daily (2:00 UTC):
1. Comprehensive speed testing
2. Update statistics & reports
3. Cleanup old backups
```

Automation Features:

· Self-updating repository
· Error recovery mechanisms
· Backup retention (7 days)
· Status reporting to README

📡 Supported Protocols

<div align="center">

Protocol Status Features
VMess ✅ Full Support WS/TCP, Reality, TLS
VLess ✅ Full Support XTLS, Reality, Vision
Trojan ✅ Full Support TLS 1.3, WS
Shadowsocks ✅ Full Support AEAD ciphers
Hysteria2 ✅ Full Support QUIC, Brutal
Hysteria ✅ Full Support UDP, Obfs
TUIC ✅ Full Support v5, Reality
WireGuard ✅ Full Support Latest spec

</div>

🛠️ For Developers

Local Setup:

```bash
# Clone repository
git clone https://github.com/aristaproject/aristaproject.git
cd aristaproject

# Install dependencies
pip install requests pyyaml

# Run manually
python update_configs.py
```

API Usage:

```python
import requests

# Get latest configs
response = requests.get(
    "https://raw.githubusercontent.com/aristaproject/aristaproject/main/all/configs.txt"
)
configs = response.text.split('\n')
```

Add New Source:

Edit SOURCES list in update_configs.py:

```python
SOURCES = [
    "https://your-new-source.com/configs.txt",
    # ... existing sources
]
```

🤝 Contributing

We welcome contributions! Here's how you can help:

1. Add Sources: Submit PR with new config sources
2. Improve Testing: Enhance speed test algorithms
3. Add Protocols: Support for new proxy protocols
4. Bug Reports: Open issues for any problems

Contribution Guidelines:

· Ensure config sources are public and free
· Test all changes before submitting PR
· Follow existing code style
· Update documentation accordingly

📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

🔗 Links & Resources

· 📚 Documentation: This README
· 🐛 Issue Tracker: GitHub Issues
· 🔄 Live Updates: GitHub Actions
· 📊 Statistics: STATUS.md file

⚠️ Disclaimer

This project is for educational and research purposes only. Users are responsible for:

· Compliance with local laws and regulations
· Proper usage of proxy services
· Security of their own connections
· Ethical use of provided configurations

---

<div align="center">

Maintained with ❤️ by Arista Project

Last Updated: 2025-12-13 01:45 UTC

https://api.star-history.com/svg?repos=aristaproject/aristaproject&type=Date

</div>
