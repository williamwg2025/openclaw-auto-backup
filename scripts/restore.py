#!/usr/bin/env python3
"""
Auto Backup - Restore Script
恢复备份的配置文件

Usage: python3 restore.py --version backup-20260310-195545 [--dry-run]
"""

import json
import os
import shutil
import sys
import tarfile
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE = Path.home() / ".openclaw" / "workspace"
BACKUP_DIR = Path.home() / ".openclaw" / "backups"
CONFIG_FILE = SCRIPT_DIR / "../config/backup-config.json"

class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    RED = '\033[0;31m'
    NC = '\033[0m'
    BOLD = '\033[1m'

def log_info(msg): print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}")
def log_success(msg): print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {msg}")
def log_warning(msg): print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {msg}")
def log_error(msg): print(f"{Colors.RED}[ERROR]{Colors.NC} {msg}")

def load_config():
    """加载配置文件"""
    if not CONFIG_FILE.exists():
        log_error(f"配置文件不存在：{CONFIG_FILE}")
        sys.exit(1)
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def list_backups():
    """列出所有备份"""
    if not BACKUP_DIR.exists():
        return []
    
    backups = []
    for f in BACKUP_DIR.glob("backup-*.tar.gz"):
        stat = f.stat()
        backups.append({
            'name': f.name,
            'path': f,
            'size': stat.st_size,
            'mtime': datetime.fromtimestamp(stat.st_mtime)
        })
    
    return sorted(backups, key=lambda x: x['mtime'], reverse=True)

def restore_backup(version: str, dry_run: bool = False):
    """恢复指定版本的备份"""
    backup_file = BACKUP_DIR / version
    
    # 验证备份文件
    if not backup_file.exists():
        log_error(f"备份文件不存在：{backup_file}")
        log_info("可用备份：")
        backups = list_backups()
        for b in backups[:10]:
            print(f"  - {b['name']} ({b['mtime'].strftime('%Y-%m-%d %H:%M')})")
        sys.exit(1)
    
    if not tarfile.is_tarfile(backup_file):
        log_error(f"无效的备份文件：{backup_file}")
        sys.exit(1)
    
    log_info(f"准备恢复备份：{version}")
    
    if dry_run:
        log_warning("[模拟运行] 不实际恢复")
        with tarfile.open(backup_file, 'r:gz') as tar:
            members = tar.getnames()
            log_info(f"备份包含 {len(members)} 个文件：")
            for m in members[:20]:
                print(f"  - {m}")
            if len(members) > 20:
                print(f"  ... 还有 {len(members) - 20} 个文件")
        return
    
    # 创建临时目录
    temp_dir = BACKUP_DIR / f".restore-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # 解压备份
        log_info("解压备份文件...")
        with tarfile.open(backup_file, 'r:gz') as tar:
            tar.extractall(path=temp_dir)
        
        # 读取清单
        manifest_file = temp_dir / "backup-manifest.json"
        if not manifest_file.exists():
            log_error("备份清单不存在")
            sys.exit(1)
        
        with open(manifest_file, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        # 恢复文件
        log_info(f"恢复 {len(manifest['files'])} 个文件...")
        restored = 0
        
        for file_info in manifest['files']:
            src = temp_dir / file_info['name']
            dst = WORKSPACE / file_info['name']
            
            if src.exists():
                # 备份当前版本
                if dst.exists():
                    backup_current = dst.with_suffix(f".backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
                    shutil.copy2(dst, backup_current)
                    log_info(f"已备份当前版本：{backup_current.name}")
                
                # 恢复文件
                shutil.copy2(src, dst)
                log_success(f"已恢复：{file_info['name']}")
                restored += 1
            else:
                log_warning(f"文件不存在，跳过：{file_info['name']}")
        
        log_success(f"恢复完成！共恢复 {restored}/{len(manifest['files'])} 个文件")
        log_warning("建议重启 OpenClaw 网关以应用恢复的配置")
        
    except Exception as e:
        log_error(f"恢复失败：{e}")
        raise
    finally:
        # 清理临时目录
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
            log_info("已清理临时文件")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='恢复 Auto Backup 备份')
    parser.add_argument('--version', required=True, help='要恢复的备份版本 (如：backup-20260310-195545)')
    parser.add_argument('--dry-run', action='store_true', help='模拟运行，不实际恢复')
    parser.add_argument('--list', action='store_true', help='列出所有可用备份')
    
    args = parser.parse_args()
    
    if args.list:
        log_info("可用备份：")
        backups = list_backups()
        if not backups:
            log_warning("没有找到备份")
            return
        
        for i, b in enumerate(backups, 1):
            size_kb = b['size'] / 1024
            mtime = b['mtime'].strftime('%Y-%m-%d %H:%M')
            marker = " ← 当前选择" if b['name'] == args.version else ""
            print(f"{i:2d}. {b['name']:<40} {size_kb:>8.1f} KB  {mtime}{marker}")
        return
    
    restore_backup(args.version, args.dry_run)

if __name__ == "__main__":
    main()
