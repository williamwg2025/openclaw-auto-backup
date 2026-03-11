#!/usr/bin/env python3
"""
Auto Backup Script
Usage: python3 backup.py [--note "备注信息"]
"""

import json
import os
import shutil
import sys
import tarfile
from datetime import datetime
from pathlib import Path

class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    RED = '\033[0;31m'
    NC = '\033[0m'
    BOLD = '\033[1m'

SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "../config/backup-config.json"
OPENCLAW_HOME = Path.home() / ".openclaw"

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*50}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text:^50}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*50}{Colors.NC}\n")

def log_info(msg): print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}")
def log_success(msg): print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {msg}")
def log_warning(msg): print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {msg}")
def log_error(msg): print(f"{Colors.RED}[ERROR]{Colors.NC} {msg}")

def load_config():
    if not CONFIG_FILE.exists():
        log_error(f"配置文件不存在：{CONFIG_FILE}")
        sys.exit(1)
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_backup_dir(backup_dir: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = backup_dir / f"backup-{timestamp}"
    backup_path.mkdir(parents=True, exist_ok=True)
    return backup_path

def backup_files(watch_files: list, backup_path: Path, exclude_patterns: list) -> list:
    backed_up = []
    for file_pattern in watch_files:
        import glob
        files = glob.glob(file_pattern) if '*' in file_pattern else [file_pattern]
        for file_path_str in files:
            file_path = Path(file_path_str)
            if not file_path.exists():
                log_warning(f"文件不存在，跳过：{file_path}")
                continue
            excluded = any(pattern in str(file_path) for pattern in exclude_patterns)
            if excluded:
                continue
            try:
                if file_path.is_file():
                    rel_path = file_path.relative_to(OPENCLAW_HOME) if str(file_path).startswith(str(OPENCLAW_HOME)) else file_path.name
                    dest_path = backup_path / rel_path
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file_path, dest_path)
                    backed_up.append(str(file_path))
                    log_info(f"已备份：{file_path.name}")
                elif file_path.is_dir():
                    rel_path = file_path.relative_to(OPENCLAW_HOME) if str(file_path).startswith(str(OPENCLAW_HOME)) else file_path.name
                    dest_path = backup_path / rel_path
                    if dest_path.exists():
                        shutil.rmtree(dest_path)
                    shutil.copytree(file_path, dest_path)
                    backed_up.append(str(file_path))
                    log_info(f"已备份目录：{file_path.name}")
            except Exception as e:
                log_error(f"备份失败 {file_path}: {e}")
    return backed_up

def create_manifest(backup_path: Path, backed_up_files: list, note: str):
    manifest = {
        "version": "1.0",
        "timestamp": datetime.now().isoformat(),
        "note": note,
        "files": backed_up_files,
        "fileCount": len(backed_up_files),
        "totalSize": sum(Path(f).stat().st_size for f in backed_up_files if Path(f).exists())
    }
    manifest_path = backup_path / "manifest.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    return manifest

def compress_backup(backup_path: Path):
    tar_path = backup_path.with_suffix('.tar.gz')
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(backup_path, arcname=backup_path.name)
    shutil.rmtree(backup_path)
    return tar_path

def main():
    import argparse
    parser = argparse.ArgumentParser(description='备份 OpenClaw 配置文件')
    parser.add_argument('--note', type=str, default='手动备份', help='备份备注')
    args = parser.parse_args()
    
    print_header("📦 Auto Backup")
    config = load_config()
    
    if not config.get('enabled', True):
        log_warning("自动备份已禁用")
        return
    
    backup_dir = Path(config.get('backupDir', str(OPENCLAW_HOME / "backups")))
    watch_files = config.get('watchFiles', [])
    exclude_patterns = config.get('excludePatterns', [])
    compression = config.get('compression', True)
    
    log_info(f"备份目录：{backup_dir}")
    log_info(f"监听文件：{len(watch_files)} 个")
    
    backup_path = create_backup_dir(backup_dir)
    log_info(f"创建备份目录：{backup_path.name}")
    
    backed_up = backup_files(watch_files, backup_path, exclude_patterns)
    
    if not backed_up:
        log_warning("没有文件被备份")
        shutil.rmtree(backup_path)
        return
    
    manifest = create_manifest(backup_path, backed_up, args.note)
    log_info(f"创建备份清单：{manifest['fileCount']} 个文件")
    
    if compression:
        log_info("压缩备份中...")
        final_path = compress_backup(backup_path)
        log_success(f"备份完成：{final_path.name}")
    else:
        final_path = backup_path
        log_success(f"备份完成：{backup_path.name}")
    
    print_header("✅ 备份完成")
    print(f"备份位置：{Colors.CYAN}{final_path}{Colors.NC}")
    print(f"文件数量：{Colors.BOLD}{manifest['fileCount']}{Colors.NC}")
    print(f"总大小：{Colors.BOLD}{manifest['totalSize'] / 1024:.2f} KB{Colors.NC}")
    print(f"备注：{Colors.YELLOW}{args.note}{Colors.NC}")

if __name__ == '__main__':
    main()
