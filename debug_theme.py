# debug_theme.py
import os
from pathlib import Path

print("🔍 Debugging Theme Configuration\n")

# 1. หา config files ทั้งหมด
print("📁 Searching for config files...")
config_files = []
for root, dirs, files in os.walk('.'):
    # Skip venv and .git
    if 'venv' in root or '.git' in root:
        continue
    for file in files:
        if file.endswith('.toml'):
            full_path = os.path.join(root, file)
            config_files.append(full_path)
            print(f"  ✓ Found: {full_path}")

print(f"\n📊 Total config files found: {len(config_files)}\n")

# 2. เช็คเนื้อหาของแต่ละไฟล์
print("📄 Checking file contents...\n")
for config_file in config_files:
    print(f"{'='*60}")
    print(f"File: {config_file}")
    print(f"{'='*60}")
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
            print(content)
            
            # เช็คว่ามี [theme.sidebar] หรือไม่
            if '[theme.sidebar]' in content.lower():
                print("\n⚠️  WARNING: This file contains [theme.sidebar] section!")
                
            # เช็คว่ามี empty string หรือไม่
            if '= ""' in content or "= ''" in content:
                print("\n🚨 ERROR: This file contains empty strings!")
                
    except Exception as e:
        print(f"Error reading file: {e}")
    print(f"\n")

# 3. เช็ค Python files ที่อาจสร้าง theme
print(f"\n{'='*60}")
print("🐍 Checking Python files that might generate themes...")
print(f"{'='*60}\n")

python_files = ['utils/theme_manager.py', 'utils/theme_system.py', 'app_chatbot.py']
for py_file in python_files:
    if os.path.exists(py_file):
        print(f"\n📝 File: {py_file}")
        with open(py_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'sidebar' in content.lower() and 'theme' in content.lower():
                print("⚠️  This file contains theme/sidebar code!")
                # แสดงบรรทัดที่เกี่ยวข้อง
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    if 'sidebar' in line.lower() and ('theme' in line.lower() or 'color' in line.lower() or 'widget' in line.lower()):
                        print(f"  Line {i}: {line.strip()}")

print("\n✅ Debug complete!")
