---
name: auto-backup
displayName: Auto Backup
version: 1.0.1
description: 自动备份 OpenClaw 配置文件，支持本地存储、版本管理、一键恢复。包含完整的 Python 脚本和定时任务配置。
license: MIT-0
acceptLicenseTerms: true
tags: backup, automation, config, scheduled-tasks
---

# Auto Backup 技能

自动备份 OpenClaw 配置文件，保护配置安全。

## 📦 安装

```bash
# 克隆技能
git clone https://github.com/williamwg2025/openclaw-auto-backup.git auto-backup
cd auto-backup

# 添加执行权限
chmod +x scripts/*.py
```

## 🔧 配置

### 备份路径
- **备份存储位置：** `~/.openclaw/backups/`
- **备份格式：** `.tar.gz` 压缩包
- **命名规则：** `backup-YYYYMMDD-HHMMSS.tar.gz`

### 备份内容
备份以下配置文件：
- `~/.openclaw/openclaw.json` - 主配置文件
- `~/.openclaw/workspace/*.md` - 工作区文档
- `~/.openclaw/workspace/skills/` - 技能目录（可选）

## 📖 使用

### 手动备份
```bash
cd auto-backup
python3 scripts/backup.py --note "配置更新"
```

### 查看备份列表
```bash
python3 scripts/list.py
```

### 恢复备份
```bash
python3 scripts/restore.py --version backup-20260310-195545
```

### 清理旧备份
```bash
python3 scripts/cleanup.py --keep 10  # 保留最近 10 个
```

## ⏰ 定时任务

### OpenClaw 内置 Cron
技能配置了 OpenClaw 内置定时任务：
- **频率：** 每天凌晨 2:00
- **任务 ID：** `ffbe8fd5-85c0-4261-b8ab-57ed9dc54cf4`
- **查看状态：** `openclaw cron list`

### 系统 Crontab（可选）
如需使用系统 cron：
```bash
crontab -e
# 添加：0 2 * * * cd ~/.openclaw/workspace/skills/auto-backup && python3 scripts/backup.py --note 定时备份
```

## 🔒 安全说明

- **本地存储：** 备份仅存储在本地 `~/.openclaw/backups/`
- **无加密：** 当前版本不加密备份（敏感信息请自行加密）
- **权限：** 需要读取 `~/.openclaw/` 目录权限
- **无网络：** 备份过程不联网，不上传任何数据

## 📁 文件结构

```
auto-backup/
├── SKILL.md          # 技能说明
├── README.md         # 详细文档
├── config/
│   └── backup-config.json  # 备份配置
└── scripts/
    ├── backup.py     # 备份脚本
    ├── list.py       # 列表脚本
    ├── restore.py    # 恢复脚本
    └── cleanup.py    # 清理脚本
```

## 📄 许可证

MIT-0

---

**作者：** @williamwg2025  
**版本：** 1.0.1  
**GitHub：** https://github.com/williamwg2025/openclaw-auto-backup
