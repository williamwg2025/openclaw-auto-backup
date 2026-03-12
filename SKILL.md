---
name: auto-backup
displayName: Auto Backup
version: 1.0.3
description: 自动备份 OpenClaw 配置文件，支持本地存储、版本管理、一键恢复。包含完整的 Python 脚本（backup/list/restore/cleanup）和定时任务配置。已通过 ClawHub 安全审查（修复 ZipSlip 漏洞）。
license: MIT-0
acceptLicenseTerms: true
tags: backup, automation, config, scheduled-tasks, security-audited
---

# Auto Backup 技能

自动备份 OpenClaw 配置文件，保护配置安全。

## 📦 安装

本技能已包含所有脚本文件，无需外部克隆。

```bash
# 如果使用 ClawHub 安装（推荐）
npx clawhub install auto-backup

# 或手动添加执行权限
cd ~/.openclaw/workspace/skills/auto-backup
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

### 安全审计 ✅
**v1.0.3 已通过 ClawHub 安全审查**

**已修复的安全问题：**
- ✅ **ZipSlip 路径遍历漏洞** - restore.py 使用安全提取，验证所有路径
- ✅ **manifest 文件名不一致** - 统一使用 manifest.json
- ✅ **符号链接风险** - 跳过所有符号链接和硬链接

### 备份加密
⚠️ **当前版本不支持加密**。备份文件以明文存储。

**建议：**
- 敏感信息（API Key、密码等）不要放在配置文件中
- 可使用外部工具加密备份目录：
  ```bash
  # 使用 gpg 加密备份
  gpg -c ~/.openclaw/backups/backup-*.tar.gz
  ```

### 存储位置
- **本地存储：** 备份仅存储在 `~/.openclaw/backups/`
- **路径说明：** 使用 `~` 而非 `/root`，适配不同用户

### 权限
- **需要权限：** 读取 `~/.openclaw/` 目录
- **无需 root：** 以当前用户身份运行

### 网络
- **无网络：** 备份过程不联网，不上传任何数据
- **无外部依赖：** 不克隆外部仓库，所有脚本已包含

### 安全最佳实践
1. **定期验证备份** - 使用 `--dry-run` 测试恢复
2. **异地备份** - 定期复制备份到其他位置
3. **版本管理** - 保留多个历史版本
4. **权限控制** - 确保备份目录权限正确（`chmod 700`）

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
