# infra-automation

A modular Python-based tool that **simulates infrastructure provisioning and service configuration**.  
Built as the foundation for a DevOps automation project — future iterations will replace the mock layer with real AWS resources managed by Terraform.

---

## Project Structure

```
infra-automation/
├── configs/          # Generated instance configs (instances.json)
├── logs/             # Runtime logs (provisioning.log)
├── scripts/          # Bash setup scripts
│   ├── setup_base.sh
│   ├── setup_nginx.sh
│   └── setup_mysql.sh
├── src/              # Python source modules
│   ├── __init__.py
│   ├── input_handler.py   # Interactive CLI & JSON persistence
│   ├── logger.py          # Centralised logging
│   ├── machine.py         # Machine dataclass
│   ├── provisioner.py     # Subprocess runner + mock provisioner
│   └── validator.py       # Input validation (pydantic / manual)
├── infra_simulator.py     # Entry point
├── requirements.txt
└── README.md
```

---

## Setup

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/infra-automation.git
cd infra-automation

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Usage

### Interactive mode (define new machines)
```bash
python infra_simulator.py
```

You will be prompted for each machine's details:

```
Supported operating systems: Amazon Linux, Centos, Debian, Fedora, Ubuntu
Type 'done' as the machine name when finished.

Machine name (or 'done' to finish): web-server
  OS [amazon linux, centos, debian, fedora, ubuntu]: Ubuntu
  vCPUs (1-64): 2
  RAM in GB (1-512): 4
  Services to install (comma-separated, e.g. nginx,mysql) or leave blank: nginx
  ✓  Machine 'web-server' added.
```

Configs are saved to `configs/instances.json` and logs are written to `logs/provisioning.log`.

### Re-provision from saved config
```bash
python infra_simulator.py --load
```

---

## Supported Services

| Service | Script |
|---------|--------|
| nginx   | `scripts/setup_nginx.sh` |
| mysql   | `scripts/setup_mysql.sh` |

Add more by creating `scripts/setup_<service>.sh` and following the existing pattern.

---

## Logging

All activity is logged to **`logs/provisioning.log`** and echoed to stdout.

```
2025-01-15 10:32:01  [INFO    ]  === Provisioning started: web-server ===
2025-01-15 10:32:01  [INFO    ]  [web-server] Base setup script started.
2025-01-15 10:32:02  [INFO    ]  [web-server] Nginx installed (mock).
2025-01-15 10:32:03  [INFO    ]  === Provisioning complete: web-server ===
```

---

## Future Enhancements

- Replace mock provisioning with real **AWS EC2** instances via `boto3`
- Manage infrastructure state with **Terraform**
- Add Docker container provisioning support
- Extend validation with more complex rules (e.g. OS ↔ service compatibility)
- CI/CD pipeline with GitHub Actions
