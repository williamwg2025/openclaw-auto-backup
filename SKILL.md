---
name: auto-backup
displayName: Auto Backup
version: 1.0.0
description: 自动备份 OpenClaw 配置文件，支持本地存储、版本管理、一键恢复。
license: MIT-0
acceptLicenseTerms: true
tags: backup, automation, config
---

# Auto Backup 技能

自动备份 OpenClaw 配置文件，保护配置安全。

## 功能

- ✅ 手动备份
- ✅ 定时备份
- ✅ 版本管理
- ✅ 一键恢复
- ✅ 自动清理

## 使用

```bash
# 备份
python3 scripts/backup.py --note "备注"

# 列表
python3 scripts/list.py

# 恢复
python3 scripts/restore.py --version backup-20260310-195545

# 清理
python3 scripts/cleanup.py --keep 10
```

## 定时任务

已配置每天凌晨 2 点自动备份。
