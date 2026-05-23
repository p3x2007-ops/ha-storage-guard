DOMAIN = "storage_guard"
PLATFORMS = ["sensor", "binary_sensor", "switch", "number", "select"]

CONF_GLANCES_ENTITY = "glances_disk_entity"

# Defaults
DEFAULT_MODE = "manual"
DEFAULT_ALERT_THRESHOLD = 80
DEFAULT_PURGE_KEEP_DAYS = 7
DEFAULT_BACKUP_KEEP_COUNT = 3
DEFAULT_CRITICAL_THRESHOLD = 95

# Modes
MODE_MANUAL = "manual"
MODE_SEMI_AUTO = "semi_auto"
MODE_FULL_AUTO = "full_auto"
MODES = [MODE_MANUAL, MODE_SEMI_AUTO, MODE_FULL_AUTO]

# Update intervals (seconds)
UPDATE_INTERVAL_DISK = 60
UPDATE_INTERVAL_DB = 300
UPDATE_INTERVAL_BACKUPS = 600
UPDATE_INTERVAL_LOGS = 300
UPDATE_INTERVAL_TOP_ENTITIES = 3600

# Switch keys
SWITCH_AUTO_PURGE_DB = "auto_purge_db"
SWITCH_AUTO_CLEAN_BACKUPS = "auto_clean_backups"
SWITCH_AUTO_CLEAN_LOGS = "auto_clean_logs"
SWITCH_AUTO_EXCLUDE_ENTITIES = "auto_exclude_entities"
SWITCH_NOTIFY_THRESHOLD = "notify_threshold"
SWITCH_NOTIFY_ACTION = "notify_action"
SWITCH_NOTIFY_WEEKLY = "notify_weekly"
SWITCH_NOTIFY_CRITICAL = "notify_critical"

SWITCHES = {
    SWITCH_AUTO_PURGE_DB: False,
    SWITCH_AUTO_CLEAN_BACKUPS: False,
    SWITCH_AUTO_CLEAN_LOGS: False,
    SWITCH_AUTO_EXCLUDE_ENTITIES: False,
    SWITCH_NOTIFY_THRESHOLD: True,
    SWITCH_NOTIFY_ACTION: True,
    SWITCH_NOTIFY_WEEKLY: False,
    SWITCH_NOTIFY_CRITICAL: True,
}

# Service names
SERVICE_PURGE_DATABASE = "purge_database"
SERVICE_CLEAN_BACKUPS = "clean_backups"
SERVICE_CLEAN_LOGS = "clean_logs"
SERVICE_EXCLUDE_ENTITY = "exclude_entity"
SERVICE_INCLUDE_ENTITY = "include_entity"
SERVICE_RUN_ANALYSIS = "run_analysis"
SERVICE_RUN_CLEANUP = "run_cleanup"

# Coordinator data keys
DATA_DISK_TOTAL = "disk_total"
DATA_DISK_USED = "disk_used"
DATA_DISK_FREE = "disk_free"
DATA_DISK_PERCENT = "disk_percent"
DATA_DB_SIZE = "db_size"
DATA_BACKUP_COUNT = "backup_count"
DATA_BACKUP_SIZE = "backup_size"
DATA_LOG_SIZE = "log_size"
DATA_TOP_ENTITIES = "top_entities"
DATA_LAST_ACTION = "last_action"
DATA_SPACE_RECLAIMABLE = "space_reclaimable"
