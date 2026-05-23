# 🛡️ StorageGuard for Home Assistant

[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz)
[![HA Version](https://img.shields.io/badge/HA-2024.1%2B-blue.svg)](https://www.home-assistant.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Complete storage lifecycle management for Home Assistant OS.**

Monitor disk usage, database size, backups, and logs — then automatically clean up when thresholds are exceeded. All configurable from a premium dashboard card.

---

## Features

- **Real-time monitoring** — Disk usage, MariaDB/SQLite size, backup count & size, log file size
- **3 operation modes** — Manual, Semi-Auto, Full-Auto
- **Configurable thresholds** — Alert at any percentage, critical at 95%
- **Automatic cleanup actions** — Database purge, backup rotation, log cleanup, entity exclusion
- **Premium companion card** — 4-tab interface (Status / Config / Logs / Actions) with GitHub Dark theme
- **Impact estimation** — See how much space each action would free before executing
- **Smart entity analysis** — Identifies top storage-consuming entities in your recorder
- **Granular notifications** — Per-event notification controls
- **Multilingual** — English + French (community contributions welcome)
- **Privacy-first** — 100% local, no cloud, no external APIs

---

## Screenshots

<!-- TODO: Add screenshots after first working version -->

---

## Requirements

- Home Assistant OS or Supervised installation
- [Glances](https://www.home-assistant.io/integrations/glances/) integration configured
- HACS installed

---

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click the three dots menu → **Custom repositories**
3. Add this repository URL with category **Integration**
4. Search for "StorageGuard" and install
5. Restart Home Assistant
6. Go to **Settings → Integrations → Add Integration → StorageGuard**

### Manual

1. Copy `custom_components/storage_guard/` to your HA `config/custom_components/` directory
2. Restart Home Assistant
3. Go to **Settings → Integrations → Add Integration → StorageGuard**

---

## Configuration

StorageGuard is configured entirely through the UI — no YAML required.

### Setup Flow

The integration automatically detects:
- Glances disk sensors
- Installation type (HAOS/Supervised)
- Recorder backend (MariaDB/SQLite)

### Operation Modes

| Mode | Behavior |
|------|----------|
| **Manual** | Monitoring + alerts only. Actions triggered manually via card or services. |
| **Semi-Auto** | Light actions (DB purge, log cleanup) run automatically. Destructive actions (backup deletion) require confirmation via notification. |
| **Full-Auto** | All enabled actions execute automatically in priority order when threshold is exceeded. |

### Card

Add to any dashboard:

```yaml
type: custom:storage-guard-card
```

The card auto-discovers all StorageGuard entities — no additional configuration needed.

---

## Services

| Service | Description |
|---------|-------------|
| `storage_guard.purge_database` | Force recorder purge |
| `storage_guard.clean_backups` | Remove oldest backups |
| `storage_guard.clean_logs` | Truncate log files |
| `storage_guard.exclude_entity` | Exclude entity from recorder |
| `storage_guard.include_entity` | Re-include entity in recorder |
| `storage_guard.run_analysis` | Re-analyze top consuming entities |
| `storage_guard.run_cleanup` | Execute full cleanup cycle |

---

## FAQ

**Q: Does this work with SQLite?**
A: Yes, but with limited DB size reporting. MariaDB provides more detailed statistics.

**Q: Will it delete my data without asking?**
A: In Manual mode, never. In Semi-Auto, only non-destructive actions run automatically. In Full-Auto, all enabled actions run but you control which ones are enabled.

**Q: What happens if Glances is not configured?**
A: The integration will not set up. Glances is required for disk usage monitoring.

---

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a Pull Request

### Translations

Translation files are in `custom_components/storage_guard/translations/`. Copy `en.json` and translate to your language.

---

## License

MIT — see [LICENSE](LICENSE)
