# Auto Backup for OpenClaw

自动备份 OpenClaw 配置文件，保护配置安全。

[English Version](README.md)

---

## ✨ 功能特性

- 📦 **手动备份** - 随时备份配置
- ⏰ **定时备份** - 每天凌晨 2 点自动备份
- 📚 **版本管理** - 查看所有备份版本
- 🔄 **一键恢复** - 恢复到任意版本
- 🧹 **自动清理** - 保留最近 N 个备份

---

## 🚀 安装

```bash
cd /root/.openclaw/workspace/skills
git clone https://github.com/williamwg2025/openclaw-auto-backup.git auto-backup
chmod +x auto-backup/scripts/*.py
```

---

## 📖 使用

### 备份配置

```bash
# 手动备份
python3 auto-backup/scripts/backup.py

# 带备注备份
python3 auto-backup/scripts/backup.py --note "配置更新后"
```

### 查看备份

```bash
python3 auto-backup/scripts/list.py
```

### 恢复配置

```bash
# 恢复到指定版本
python3 auto-backup/scripts/restore.py --version backup-20260310-195545

# 恢复到上一个版本
python3 auto-backup/scripts/restore.py --offset -1
```

### 清理备份

```bash
# 保留最近 10 个
python3 auto-backup/scripts/cleanup.py --keep 10

# 删除超过 30 天的
python3 auto-backup/scripts/cleanup.py --older-than 30d
```

---

## ⏰ 定时任务

已配置每天凌晨 2 点自动备份。

查看定时任务：
```bash
openclaw cron list
```

---

## 📋 配置

备份配置：
`/root/.openclaw/workspace/skills/auto-backup/config/backup-config.json`

备份位置：
`/root/.openclaw/backups/`

---

## 🛠️ 脚本说明

| 脚本 | 功能 |
|------|------|
| `backup.py` | 备份配置 |
| `list.py` | 查看备份列表 |
| `restore.py` | 恢复配置 |
| `cleanup.py` | 清理旧备份 |

---

## 📄 许可证

MIT-0

---

**作者：** @williamwg2025  
**版本：** 1.0.0
