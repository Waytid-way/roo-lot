# fix_sidebar_theme.py
import os
import re
from pathlib import Path

def fix_config_file(config_path):
    """แก้ไข config.toml โดยลบ [theme.sidebar] section ที่มี empty strings"""
    
    print(f"\n📁 Checking: {config_path}")
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # เช็คว่ามี [theme.sidebar] section หรือไม่
        if '[theme.sidebar]' not in content:
            print("  ✓ No [theme.sidebar] section found - OK")
            return False
        
        # แสดงเนื้อหา original
        print("\n  📄 Original content:")
        print("  " + "\n  ".join(content.split('\n')[:20]))
        
        # ลบ [theme.sidebar] section ที่มี empty strings
        # Pattern: จับตั้งแต่ [theme.sidebar] จนถึง section ถัดไป หรือจบไฟล์
        pattern = r'\[theme\.sidebar\][^\[]*?(?=\[|\Z)'
        
        # ตรวจสอบว่า section มี empty strings หรือไม่
        sidebar_section = re.search(pattern, content, re.DOTALL)
        if sidebar_section:
            section_text = sidebar_section.group(0)
            if '= ""' in section_text or "= ''" in section_text:
                print("\n  ⚠️  Found [theme.sidebar] with empty strings!")
                
                # Backup original file
                backup_path = str(config_path) + '.backup'
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                print(f"  📦 Backup created: {backup_path}")
                
                # ลบ section
                content = re.sub(pattern, '', content, flags=re.DOTALL)
                
                # ลบบรรทัดว่างซ้ำ
                content = re.sub(r'\n{3,}', '\n\n', content)
                
                # เขียนไฟล์ใหม่
                with open(config_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print("  ✅ Fixed! [theme.sidebar] section removed")
                print("\n  📄 New content:")
                print("  " + "\n  ".join(content.split('\n')[:20]))
                return True
            else:
                print("  ℹ️  [theme.sidebar] exists but has valid values - OK")
                return False
        
        return False
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

# ค้นหาและแก้ไข config files
print("🔍 Searching for Streamlit config files...\n")

fixed_count = 0
search_paths = [
    Path('.streamlit'),  # โปรเจกต์ปัจจุบัน
    Path.home() / '.streamlit',  # User home directory
]

for search_path in search_paths:
    if search_path.exists():
        for config_file in search_path.rglob('*.toml'):
            if fix_config_file(config_file):
                fixed_count += 1

print(f"\n{'='*60}")
print(f"✅ Summary: Fixed {fixed_count} file(s)")
print(f"{'='*60}")

if fixed_count > 0:
    print("\n⚠️  IMPORTANT: You MUST restart Streamlit for changes to take effect!")
    print("   1. Press Ctrl+C to stop the server")
    print("   2. Clear browser cache (Ctrl+Shift+Delete)")
    print("   3. Run: streamlit run app_chatbot.py")
    print("\n💡 If errors persist, try clearing browser local storage:")
    print("   1. Open Developer Tools (F12)")
    print("   2. Go to Application/Storage tab")
    print("   3. Click 'Local Storage' → Your app URL")
    print("   4. Right-click → Clear")
else:
    print("\n🔍 No issues found in config files.")
    print("   The problem might be in browser's cached theme.")
    print("   Try: Hard refresh (Ctrl+Shift+R) or clear browser cache")
