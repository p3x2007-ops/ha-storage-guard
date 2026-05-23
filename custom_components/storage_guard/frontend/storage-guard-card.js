/**
 * StorageGuard Card — Premium storage management companion card
 * GitHub Dark / DevOps theme
 */

const CARD_VERSION = "1.0.0";

const STYLES = `
  :host {
    --sg-bg: #0d1117;
    --sg-surface: #161b22;
    --sg-elevated: #21262d;
    --sg-border: #30363d;
    --sg-text: #c9d1d9;
    --sg-text-muted: #8b949e;
    --sg-text-bright: #f0f6fc;
    --sg-blue: #58a6ff;
    --sg-blue-bg: rgba(31, 111, 235, 0.15);
    --sg-green: #3fb950;
    --sg-green-bg: rgba(63, 185, 80, 0.15);
    --sg-yellow: #d29922;
    --sg-yellow-bg: rgba(210, 153, 34, 0.15);
    --sg-red: #f85149;
    --sg-red-bg: rgba(248, 81, 73, 0.15);
  }
  .card {
    background: var(--sg-surface);
    border: 1px solid var(--sg-border);
    border-radius: 12px;
    padding: 16px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: var(--sg-text);
    font-size: 13px;
  }
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
  }
  .header-left {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .logo {
    width: 24px;
    height: 24px;
    background: linear-gradient(135deg, var(--sg-blue), #1f6feb);
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
  }
  .title {
    font-size: 15px;
    font-weight: 600;
    color: var(--sg-text-bright);
  }
  .badge {
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
  }
  .badge-nominal {
    background: var(--sg-green-bg);
    color: var(--sg-green);
  }
  .badge-warning {
    background: var(--sg-yellow-bg);
    color: var(--sg-yellow);
  }
  .badge-critical {
    background: var(--sg-red-bg);
    color: var(--sg-red);
  }
  .tabs {
    display: flex;
    gap: 2px;
    margin-bottom: 14px;
    background: var(--sg-bg);
    border-radius: 6px;
    padding: 2px;
  }
  .tab {
    flex: 1;
    text-align: center;
    padding: 6px 4px;
    border-radius: 5px;
    font-size: 10px;
    color: var(--sg-text-muted);
    cursor: pointer;
    transition: all 0.2s;
    user-select: none;
  }
  .tab:hover {
    color: var(--sg-text);
  }
  .tab.active {
    background: var(--sg-elevated);
    color: var(--sg-text-bright);
    font-weight: 600;
  }
  .panel {
    background: var(--sg-bg);
    border: 1px solid var(--sg-elevated);
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 10px;
  }
  .progress-container {
    margin-bottom: 12px;
  }
  .progress-header {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    margin-bottom: 6px;
  }
  .progress-bar {
    background: var(--sg-elevated);
    border-radius: 4px;
    height: 10px;
    overflow: hidden;
    position: relative;
  }
  .progress-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.5s ease;
  }
  .progress-marker {
    position: absolute;
    top: 0;
    width: 2px;
    height: 100%;
    background: var(--sg-red);
    opacity: 0.7;
  }
  .progress-labels {
    display: flex;
    justify-content: space-between;
    font-size: 9px;
    color: var(--sg-text-muted);
    margin-top: 4px;
  }
  .grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
  }
  .grid-3 {
    grid-template-columns: 1fr 1fr 1fr;
  }
  .stat-box {
    background: var(--sg-bg);
    border: 1px solid var(--sg-elevated);
    padding: 10px;
    border-radius: 6px;
    text-align: center;
  }
  .stat-label {
    color: var(--sg-text-muted);
    font-size: 10px;
    margin-bottom: 4px;
  }
  .stat-value {
    font-size: 16px;
    font-weight: 600;
    color: var(--sg-blue);
  }
  .stat-unit {
    font-size: 10px;
    color: var(--sg-text-muted);
    margin-left: 2px;
  }
  .info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px solid var(--sg-elevated);
    font-size: 11px;
  }
  .info-row:last-child {
    border-bottom: none;
  }
  .tag {
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 10px;
  }

  /* Config tab */
  .section {
    background: var(--sg-bg);
    border: 1px solid var(--sg-elevated);
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 10px;
  }
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
  }
  .section-title {
    font-size: 12px;
    font-weight: 600;
    color: var(--sg-text-bright);
  }
  .section-desc {
    font-size: 10px;
    color: var(--sg-text-muted);
    line-height: 1.5;
    margin-bottom: 10px;
  }
  .mode-buttons {
    display: flex;
    gap: 4px;
    margin-bottom: 8px;
  }
  .mode-btn {
    flex: 1;
    background: var(--sg-elevated);
    border: 1px solid var(--sg-border);
    border-radius: 6px;
    padding: 8px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
  }
  .mode-btn.active {
    background: var(--sg-blue-bg);
    border-color: var(--sg-blue);
  }
  .mode-btn .mode-icon {
    font-size: 16px;
    margin-bottom: 2px;
  }
  .mode-btn .mode-label {
    font-size: 10px;
    color: var(--sg-text-muted);
  }
  .mode-btn.active .mode-label {
    color: var(--sg-blue);
    font-weight: 600;
  }
  .mode-desc-box {
    background: var(--sg-blue-bg);
    border: 1px solid rgba(31, 111, 235, 0.3);
    border-radius: 6px;
    padding: 8px;
    font-size: 10px;
    color: var(--sg-text-muted);
    line-height: 1.5;
  }
  .slider-row {
    margin-bottom: 10px;
  }
  .slider-header {
    display: flex;
    justify-content: space-between;
    font-size: 10px;
    margin-bottom: 6px;
  }
  .slider-track {
    -webkit-appearance: none;
    width: 100%;
    height: 6px;
    border-radius: 3px;
    background: var(--sg-elevated);
    outline: none;
  }
  .slider-track::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: var(--sg-blue);
    border: 2px solid var(--sg-bg);
    cursor: pointer;
  }
  .toggle-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
  }
  .toggle-label {
    font-size: 11px;
    color: var(--sg-text);
  }
  .toggle {
    position: relative;
    width: 32px;
    height: 16px;
    background: var(--sg-elevated);
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.2s;
    border: 1px solid var(--sg-border);
  }
  .toggle.on {
    background: var(--sg-green);
    border-color: var(--sg-green);
  }
  .toggle-knob {
    position: absolute;
    top: 2px;
    left: 2px;
    width: 12px;
    height: 12px;
    background: var(--sg-text-muted);
    border-radius: 50%;
    transition: all 0.2s;
  }
  .toggle.on .toggle-knob {
    left: 18px;
    background: white;
  }
  .counter {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .counter-btn {
    background: var(--sg-bg);
    border: 1px solid var(--sg-border);
    color: var(--sg-text-muted);
    width: 24px;
    height: 24px;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 14px;
  }
  .counter-value {
    font-size: 16px;
    font-weight: 700;
    color: var(--sg-text-bright);
    min-width: 20px;
    text-align: center;
  }
  .estimation {
    padding: 6px 8px;
    border-radius: 4px;
    font-size: 10px;
    margin-top: 8px;
  }
  .estimation-positive {
    background: var(--sg-green-bg);
    color: var(--sg-green);
  }
  .estimation-warning {
    background: var(--sg-yellow-bg);
    color: var(--sg-yellow);
  }
  .info-toggle {
    color: var(--sg-text-muted);
    cursor: pointer;
    font-size: 14px;
  }
  .info-box {
    background: var(--sg-blue-bg);
    border: 1px solid rgba(31, 111, 235, 0.3);
    border-radius: 6px;
    padding: 8px;
    font-size: 10px;
    color: var(--sg-text-muted);
    line-height: 1.5;
    margin-top: 8px;
  }
  .info-box strong {
    color: var(--sg-red);
  }

  /* Logs tab */
  .log-entry {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px;
    border-bottom: 1px solid var(--sg-elevated);
    font-size: 11px;
  }
  .log-icon {
    font-size: 14px;
  }
  .log-time {
    color: var(--sg-text-muted);
    font-size: 10px;
    min-width: 50px;
  }
  .log-text {
    flex: 1;
    color: var(--sg-text);
  }
  .log-freed {
    color: var(--sg-green);
    font-size: 10px;
    font-weight: 600;
  }

  /* Actions tab */
  .action-btn {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--sg-bg);
    border: 1px solid var(--sg-elevated);
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 8px;
    cursor: pointer;
    transition: border-color 0.2s;
  }
  .action-btn:hover {
    border-color: var(--sg-blue);
  }
  .action-btn-left {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .action-btn-icon {
    font-size: 18px;
  }
  .action-btn-title {
    font-size: 12px;
    font-weight: 600;
    color: var(--sg-text-bright);
  }
  .action-btn-desc {
    font-size: 10px;
    color: var(--sg-text-muted);
  }
  .action-btn-impact {
    font-size: 11px;
    font-weight: 600;
    color: var(--sg-green);
  }
  .action-btn.destructive:hover {
    border-color: var(--sg-red);
  }
  .action-btn.destructive .action-btn-impact {
    color: var(--sg-yellow);
  }
  .full-cleanup-btn {
    display: block;
    width: 100%;
    padding: 12px;
    background: linear-gradient(135deg, var(--sg-blue), #1f6feb);
    border: none;
    border-radius: 8px;
    color: white;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    text-align: center;
    margin-top: 12px;
  }
  .full-cleanup-btn:hover {
    opacity: 0.9;
  }
  .hidden {
    display: none;
  }
`;

const MODE_DESCRIPTIONS = {
  manual: {
    en: "Monitoring and alerts only. All cleanup actions must be triggered manually via this card or service calls.",
    fr: "Surveillance et alertes uniquement. Toutes les actions de nettoyage doivent être déclenchées manuellement via cette carte ou des appels de services."
  },
  semi_auto: {
    en: "Automatically executes lightweight actions (DB purge, log cleanup) when threshold is exceeded. Requests confirmation before any destructive action (backup deletion). Notifies on every action.",
    fr: "Exécute automatiquement les actions légères (purge DB, nettoyage logs) quand le seuil est dépassé. Demande confirmation avant toute action destructive (suppression de backups). Notifie à chaque action."
  },
  full_auto: {
    en: "All enabled actions execute automatically in priority order when threshold is exceeded: logs → database → backups → entity exclusion. Stops when disk usage returns below threshold.",
    fr: "Toutes les actions activées s'exécutent automatiquement par ordre de priorité quand le seuil est dépassé : logs → base de données → sauvegardes → exclusion d'entités. S'arrête quand l'utilisation repasse sous le seuil."
  }
};

class StorageGuardCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._activeTab = "status";
    this._showInfo = {};
    this._entityMap = {};
  }

  set hass(hass) {
    this._hass = hass;
    this._buildEntityMap();
    this._render();
  }

  setConfig(config) {
    this._config = config;
  }

  getCardSize() {
    return 6;
  }

  static getStubConfig() {
    return {};
  }

  _buildEntityMap() {
    const map = {};
    const nameToKey = {
      "Disk Used Percent": "disk_used_percent",
      "Disk Used": "disk_used",
      "Disk Free": "disk_free",
      "Database Size": "database_size",
      "Backup Count": "backup_count",
      "Backup Size": "backup_size",
      "Log Size": "log_size",
      "Last Action": "last_action",
      "Space Reclaimable": "space_reclaimable",
      "Alert Threshold": "alert_threshold",
      "Purge Keep Days": "purge_keep_days",
      "Backup Keep Count": "backup_keep_count",
      "Mode": "mode",
      "Auto Purge Db": "auto_purge_db",
      "Auto Clean Backups": "auto_clean_backups",
      "Auto Clean Logs": "auto_clean_logs",
      "Auto Exclude Entities": "auto_exclude_entities",
      "Notify Threshold": "notify_threshold",
      "Notify Action": "notify_action",
      "Notify Weekly": "notify_weekly",
      "Notify Critical": "notify_critical",
      "Threshold Exceeded": "threshold_exceeded",
      "Critical": "critical",
    };
    for (const [eid, stateObj] of Object.entries(this._hass.states)) {
      if (!eid.includes("storageguard") && !eid.includes("storage_guard")) continue;
      const fname = stateObj.attributes?.friendly_name || "";
      if (!fname.startsWith("StorageGuard")) continue;
      const suffix = fname.replace("StorageGuard ", "").trim();
      const key = nameToKey[suffix];
      if (key) map[key] = eid;
    }
    this._entityMap = map;
  }

  _resolve(key) {
    return this._entityMap[key] || `sensor.storage_guard_${key}`;
  }

  _getState(key) {
    const eid = this._resolve(key);
    const state = this._hass?.states[eid];
    if (!state || state.state === "unknown" || state.state === "unavailable") {
      return null;
    }
    return state.state;
  }

  _getNumericState(key, fallback = 0) {
    const val = this._getState(key);
    return val !== null ? parseFloat(val) : fallback;
  }

  _getLang() {
    return this._hass?.language?.startsWith("fr") ? "fr" : "en";
  }

  _getStatusBadge(percent) {
    if (percent === null) return { class: "badge-nominal", text: "—" };
    if (percent > 95) return { class: "badge-critical", text: "CRITICAL" };
    const threshold = this._getNumericState("alert_threshold", 80);
    if (percent > threshold) return { class: "badge-warning", text: "WARNING" };
    return { class: "badge-nominal", text: "NOMINAL" };
  }

  _getProgressColor(percent) {
    if (percent > 90) return "var(--sg-red)";
    if (percent > 75) return "var(--sg-yellow)";
    return "var(--sg-green)";
  }

  _callService(domain, service, data = {}) {
    this._hass.callService(domain, service, data);
  }

  _setTab(tab) {
    this._activeTab = tab;
    this._render();
  }

  _toggleInfo(key) {
    this._showInfo[key] = !this._showInfo[key];
    this._render();
  }

  _render() {
    if (!this._hass) return;

    const diskPercent = this._getNumericState("disk_used_percent");
    const diskUsed = this._getNumericState("disk_used");
    const diskFree = this._getNumericState("disk_free");
    const dbSize = this._getNumericState("database_size");
    const backupCount = this._getNumericState("backup_count");
    const backupSize = this._getNumericState("backup_size");
    const logSize = this._getNumericState("log_size");
    const reclaimable = this._getNumericState("space_reclaimable");
    const lastAction = this._getState("last_action") || "None";
    const mode = this._getState("mode") || "manual";
    const threshold = this._getNumericState("alert_threshold", 80);
    const purgeDays = this._getNumericState("purge_keep_days", 7);
    const keepCount = this._getNumericState("backup_keep_count", 3);
    const diskTotal = diskUsed + diskFree;

    const status = this._getStatusBadge(diskPercent);
    const lang = this._getLang();

    let tabContent = "";
    if (this._activeTab === "status") {
      tabContent = this._renderStatus(diskPercent, diskUsed, diskFree, diskTotal, dbSize, backupCount, backupSize, logSize, reclaimable, lastAction, threshold, status);
    } else if (this._activeTab === "config") {
      tabContent = this._renderConfig(mode, threshold, purgeDays, keepCount, dbSize, backupCount, backupSize, logSize, lang);
    } else if (this._activeTab === "logs") {
      tabContent = this._renderLogs(lastAction);
    } else if (this._activeTab === "actions") {
      tabContent = this._renderActions(dbSize, backupCount, backupSize, logSize, purgeDays, keepCount);
    }

    this.shadowRoot.innerHTML = `
      <style>${STYLES}</style>
      <div class="card">
        <div class="header">
          <div class="header-left">
            <div class="logo">🛡️</div>
            <span class="title">StorageGuard</span>
          </div>
          <span class="badge ${status.class}">${status.text}</span>
        </div>
        <div class="tabs">
          <div class="tab ${this._activeTab === 'status' ? 'active' : ''}" id="tab-status">📊 Status</div>
          <div class="tab ${this._activeTab === 'config' ? 'active' : ''}" id="tab-config">⚙️ Config</div>
          <div class="tab ${this._activeTab === 'logs' ? 'active' : ''}" id="tab-logs">📋 Logs</div>
          <div class="tab ${this._activeTab === 'actions' ? 'active' : ''}" id="tab-actions">🔧 Actions</div>
        </div>
        ${tabContent}
      </div>
    `;

    // Attach tab listeners
    this.shadowRoot.getElementById("tab-status")?.addEventListener("click", () => this._setTab("status"));
    this.shadowRoot.getElementById("tab-config")?.addEventListener("click", () => this._setTab("config"));
    this.shadowRoot.getElementById("tab-logs")?.addEventListener("click", () => this._setTab("logs"));
    this.shadowRoot.getElementById("tab-actions")?.addEventListener("click", () => this._setTab("actions"));

    // Attach config listeners
    this._attachConfigListeners(mode, threshold, purgeDays, keepCount);
  }

  _renderStatus(diskPercent, diskUsed, diskFree, diskTotal, dbSize, backupCount, backupSize, logSize, reclaimable, lastAction, threshold) {
    const progressColor = this._getProgressColor(diskPercent);
    const markerPos = threshold;

    return `
      <div class="panel">
        <div class="progress-container">
          <div class="progress-header">
            <span style="color:var(--sg-text-muted)">💾 Disk Usage</span>
            <span style="color:var(--sg-text-bright)">${diskUsed.toFixed(1)} / ${diskTotal.toFixed(1)} GB</span>
          </div>
          <div class="progress-bar">
            <div class="progress-fill" style="width:${diskPercent}%; background: linear-gradient(90deg, var(--sg-green) 0%, var(--sg-yellow) 60%, var(--sg-red) 95%);"></div>
            <div class="progress-marker" style="left:${markerPos}%"></div>
          </div>
          <div class="progress-labels">
            <span>0%</span>
            <span style="color:var(--sg-red)">⚠ ${threshold}%</span>
            <span>100%</span>
          </div>
        </div>
      </div>
      <div class="grid grid-3" style="margin-bottom:10px">
        <div class="stat-box">
          <div class="stat-label">MariaDB</div>
          <div class="stat-value">${dbSize.toFixed(1)}<span class="stat-unit">GB</span></div>
        </div>
        <div class="stat-box">
          <div class="stat-label">Backups</div>
          <div class="stat-value">${backupCount}<span class="stat-unit">×${backupSize.toFixed(1)}GB</span></div>
        </div>
        <div class="stat-box">
          <div class="stat-label">Logs</div>
          <div class="stat-value">${logSize.toFixed(0)}<span class="stat-unit">MB</span></div>
        </div>
      </div>
      <div class="panel">
        <div class="info-row">
          <span style="color:var(--sg-text-muted)">Free space</span>
          <span style="color:var(--sg-text-bright)">${diskFree.toFixed(1)} GB</span>
        </div>
        <div class="info-row">
          <span style="color:var(--sg-text-muted)">Reclaimable</span>
          <span style="color:var(--sg-green)">~${reclaimable.toFixed(1)} GB</span>
        </div>
        <div class="info-row">
          <span style="color:var(--sg-text-muted)">Last action</span>
          <span style="color:var(--sg-text-bright)">${lastAction}</span>
        </div>
      </div>
    `;
  }

  _renderConfig(mode, threshold, purgeDays, keepCount, dbSize, backupCount, backupSize, logSize, lang) {
    const modeDesc = MODE_DESCRIPTIONS[mode]?.[lang] || MODE_DESCRIPTIONS[mode]?.en || "";

    const purgeEstimate = dbSize > 0 ? ((14 - purgeDays) / 14 * dbSize).toFixed(1) : "?";
    const backupEstimate = backupCount > keepCount && backupSize > 0
      ? ((backupSize / backupCount) * (backupCount - keepCount)).toFixed(1)
      : "0";

    const switches = [
      { key: "auto_purge_db", label: "Auto purge DB" },
      { key: "auto_clean_backups", label: "Auto clean backups" },
      { key: "auto_clean_logs", label: "Auto clean logs" },
      { key: "auto_exclude_entities", label: "Auto exclude entities" },
    ];

    const notifSwitches = [
      { key: "notify_threshold", label: "Threshold alert" },
      { key: "notify_action", label: "Action executed" },
      { key: "notify_weekly", label: "Weekly report" },
      { key: "notify_critical", label: "Critical (>95%)" },
    ];

    let switchesHtml = switches.map(s => {
      const isOn = this._getState(s.key) === "on";
      return `<div class="toggle-row">
        <span class="toggle-label">${s.label}</span>
        <div class="toggle ${isOn ? 'on' : ''}" data-switch="${s.key}"><div class="toggle-knob"></div></div>
      </div>`;
    }).join("");

    let notifHtml = notifSwitches.map(s => {
      const isOn = this._getState(s.key) === "on";
      return `<div class="toggle-row">
        <span class="toggle-label">${s.label}</span>
        <div class="toggle ${isOn ? 'on' : ''}" data-switch="${s.key}"><div class="toggle-knob"></div></div>
      </div>`;
    }).join("");

    return `
      <!-- Mode -->
      <div class="section">
        <div class="section-header">
          <span class="section-title">🎛️ Operation Mode</span>
        </div>
        <div class="mode-buttons">
          <div class="mode-btn ${mode === 'manual' ? 'active' : ''}" data-mode="manual">
            <div class="mode-icon">👁️</div>
            <div class="mode-label">Manual</div>
          </div>
          <div class="mode-btn ${mode === 'semi_auto' ? 'active' : ''}" data-mode="semi_auto">
            <div class="mode-icon">⚡</div>
            <div class="mode-label">Semi-Auto</div>
          </div>
          <div class="mode-btn ${mode === 'full_auto' ? 'active' : ''}" data-mode="full_auto">
            <div class="mode-icon">🤖</div>
            <div class="mode-label">Full-Auto</div>
          </div>
        </div>
        <div class="mode-desc-box">${modeDesc}</div>
      </div>

      <!-- Threshold -->
      <div class="section">
        <div class="section-header">
          <span class="section-title">⚠️ Alert Threshold</span>
          <span class="tag" style="background:var(--sg-yellow-bg);color:var(--sg-yellow)">${threshold}%</span>
        </div>
        <div class="section-desc">When disk usage exceeds this threshold, StorageGuard triggers configured actions based on the selected mode.</div>
        <input type="range" class="slider-track" min="50" max="95" step="5" value="${threshold}" id="threshold-slider">
        <div class="progress-labels"><span>50%</span><span>65%</span><span>80%</span><span>95%</span></div>
      </div>

      <!-- DB Purge -->
      <div class="section">
        <div class="section-header">
          <span class="section-title">🗄️ Database Purge</span>
          <span class="info-toggle" data-info="db">ⓘ</span>
        </div>
        ${this._showInfo.db ? `<div class="info-box">Reduces recorder retention to free space. History beyond the configured days will be <strong>permanently deleted</strong>. Current recorder retention: 14 days.</div>` : ''}
        <div class="slider-row">
          <div class="slider-header">
            <span style="color:var(--sg-text-muted)">Min retention on purge</span>
            <span style="color:var(--sg-text-bright)">${purgeDays} days</span>
          </div>
          <input type="range" class="slider-track" min="1" max="30" step="1" value="${purgeDays}" id="purge-slider">
        </div>
        <div class="estimation estimation-positive">💡 Estimated gain: ~${purgeEstimate} GB</div>
      </div>

      <!-- Backups -->
      <div class="section">
        <div class="section-header">
          <span class="section-title">💾 Backup Management</span>
          <span class="info-toggle" data-info="backup">ⓘ</span>
        </div>
        ${this._showInfo.backup ? `<div class="info-box">Removes oldest backups beyond the configured count. Deleted backups are <strong>unrecoverable</strong>. In Semi-Auto mode, confirmation is required before deletion.</div>` : ''}
        <div style="display:flex;justify-content:space-between;align-items:center;background:var(--sg-elevated);padding:8px 12px;border-radius:6px">
          <span style="color:var(--sg-text-muted);font-size:11px">Backups to keep</span>
          <div class="counter">
            <div class="counter-btn" id="backup-minus">−</div>
            <span class="counter-value">${keepCount}</span>
            <div class="counter-btn" id="backup-plus">+</div>
          </div>
        </div>
        ${backupCount > keepCount ? `<div class="estimation estimation-warning">📦 Would delete ${backupCount - keepCount} backup(s) (~${backupEstimate} GB)</div>` : ''}
      </div>

      <!-- Feature switches -->
      <div class="section">
        <div class="section-title" style="margin-bottom:8px">🔄 Auto Actions</div>
        ${switchesHtml}
      </div>

      <!-- Notifications -->
      <div class="section">
        <div class="section-title" style="margin-bottom:8px">🔔 Notifications</div>
        ${notifHtml}
      </div>
    `;
  }

  _renderLogs(lastAction) {
    return `
      <div class="panel">
        <div style="text-align:center;color:var(--sg-text-muted);padding:20px;font-size:11px">
          <div style="font-size:24px;margin-bottom:8px">📋</div>
          <div>Action history will appear here after StorageGuard performs cleanup actions.</div>
          <div style="margin-top:12px;color:var(--sg-text)">Last: ${lastAction}</div>
        </div>
      </div>
    `;
  }

  _renderActions(dbSize, backupCount, backupSize, logSize, purgeDays, keepCount) {
    const purgeEst = dbSize > 0 ? ((14 - purgeDays) / 14 * dbSize).toFixed(1) : "?";
    const backupEst = backupCount > keepCount && backupSize > 0
      ? ((backupSize / backupCount) * (backupCount - keepCount)).toFixed(1)
      : "0";

    return `
      <div class="action-btn" id="action-logs">
        <div class="action-btn-left">
          <span class="action-btn-icon">📝</span>
          <div>
            <div class="action-btn-title">Clean Logs</div>
            <div class="action-btn-desc">Truncate home-assistant.log</div>
          </div>
        </div>
        <span class="action-btn-impact">~${logSize.toFixed(0)} MB</span>
      </div>
      <div class="action-btn" id="action-purge">
        <div class="action-btn-left">
          <span class="action-btn-icon">🗄️</span>
          <div>
            <div class="action-btn-title">Purge Database</div>
            <div class="action-btn-desc">Reduce to ${purgeDays} day retention</div>
          </div>
        </div>
        <span class="action-btn-impact">~${purgeEst} GB</span>
      </div>
      <div class="action-btn destructive" id="action-backups">
        <div class="action-btn-left">
          <span class="action-btn-icon">💾</span>
          <div>
            <div class="action-btn-title">Clean Backups</div>
            <div class="action-btn-desc">Keep ${keepCount}, remove ${Math.max(0, backupCount - keepCount)} oldest</div>
          </div>
        </div>
        <span class="action-btn-impact">~${backupEst} GB</span>
      </div>
      <div class="action-btn" id="action-analysis">
        <div class="action-btn-left">
          <span class="action-btn-icon">🔍</span>
          <div>
            <div class="action-btn-title">Run Analysis</div>
            <div class="action-btn-desc">Identify top storage consumers</div>
          </div>
        </div>
        <span class="action-btn-impact">scan</span>
      </div>
      <button class="full-cleanup-btn" id="action-full">🛡️ Run Full Cleanup</button>
    `;
  }

  _attachConfigListeners(mode, threshold, purgeDays, keepCount) {
    // Mode buttons
    this.shadowRoot.querySelectorAll(".mode-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const newMode = btn.dataset.mode;
        this._callService("select", "select_option", {
          entity_id: this._resolve("mode"),
          option: newMode
        });
      });
    });

    // Threshold slider
    const thresholdSlider = this.shadowRoot.getElementById("threshold-slider");
    if (thresholdSlider) {
      thresholdSlider.addEventListener("change", (e) => {
        this._callService("number", "set_value", {
          entity_id: this._resolve("alert_threshold"),
          value: parseInt(e.target.value)
        });
      });
    }

    // Purge slider
    const purgeSlider = this.shadowRoot.getElementById("purge-slider");
    if (purgeSlider) {
      purgeSlider.addEventListener("change", (e) => {
        this._callService("number", "set_value", {
          entity_id: this._resolve("purge_keep_days"),
          value: parseInt(e.target.value)
        });
      });
    }

    // Backup counter
    this.shadowRoot.getElementById("backup-minus")?.addEventListener("click", () => {
      if (keepCount > 1) {
        this._callService("number", "set_value", {
          entity_id: this._resolve("backup_keep_count"),
          value: keepCount - 1
        });
      }
    });
    this.shadowRoot.getElementById("backup-plus")?.addEventListener("click", () => {
      if (keepCount < 10) {
        this._callService("number", "set_value", {
          entity_id: this._resolve("backup_keep_count"),
          value: keepCount + 1
        });
      }
    });

    // Toggle switches
    this.shadowRoot.querySelectorAll(".toggle").forEach(toggle => {
      toggle.addEventListener("click", () => {
        const key = toggle.dataset.switch;
        const entity_id = this._resolve(key);
        const isOn = toggle.classList.contains("on");
        this._callService("switch", isOn ? "turn_off" : "turn_on", { entity_id });
      });
    });

    // Info toggles
    this.shadowRoot.querySelectorAll(".info-toggle").forEach(btn => {
      btn.addEventListener("click", () => this._toggleInfo(btn.dataset.info));
    });

    // Action buttons
    this.shadowRoot.getElementById("action-logs")?.addEventListener("click", () => {
      this._callService("storage_guard", "clean_logs");
    });
    this.shadowRoot.getElementById("action-purge")?.addEventListener("click", () => {
      this._callService("storage_guard", "purge_database");
    });
    this.shadowRoot.getElementById("action-backups")?.addEventListener("click", () => {
      if (confirm("This will permanently delete old backups. Continue?")) {
        this._callService("storage_guard", "clean_backups");
      }
    });
    this.shadowRoot.getElementById("action-analysis")?.addEventListener("click", () => {
      this._callService("storage_guard", "run_analysis");
    });
    this.shadowRoot.getElementById("action-full")?.addEventListener("click", () => {
      if (confirm("Run full cleanup cycle? This will execute all enabled actions.")) {
        this._callService("storage_guard", "run_cleanup", { force: true });
      }
    });
  }
}

customElements.define("storage-guard-card", StorageGuardCard);

window.customCards = window.customCards || [];
window.customCards.push({
  type: "storage-guard-card",
  name: "StorageGuard",
  description: "Storage lifecycle management card for Home Assistant",
  preview: true,
});

console.info(`%c StorageGuard Card v${CARD_VERSION} `, "background: #1f6feb; color: white; font-weight: bold; border-radius: 4px; padding: 2px 6px;");
