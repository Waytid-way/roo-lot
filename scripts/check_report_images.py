"""
ตรวจสอบความสมบูรณ์ของรูปภาพใน Report
"""
import os
from PIL import Image
import sys

def check_image_integrity(image_path):
    """ตรวจสอบว่ารูปภาพสามารถเปิดและอ่านได้"""
    try:
        with Image.open(image_path) as img:
            img.verify()  # ตรวจสอบความถูกต้องของไฟล์
        
        # เปิดอีกครั้งเพื่อดูขนาด (verify() ทำให้ไฟล์ไม่สามารถใช้งานต่อได้)
        with Image.open(image_path) as img:
            width, height = img.size
            format_type = img.format
            
        return {
            'valid': True,
            'width': width,
            'height': height,
            'format': format_type,
            'size_kb': round(os.path.getsize(image_path) / 1024, 2)
        }
    except Exception as e:
        return {
            'valid': False,
            'error': str(e)
        }

def main():
    """ตรวจสอบรูปภาพทั้งหมดใน Report"""
    
    # รูปภาพที่ต้องตรวจสอบ
    required_images = {
        'EDA': [
            'outputs/eda/eda_target_distribution.png',
            'outputs/eda/eda_correlation.png',
            'outputs/eda/eda_feature_relationships.png'
        ],
        'Model Visualization': [
            'outputs/model_viz/actual_vs_predicted.png',
            'outputs/model_viz/residual_plot.png',
            'outputs/model_viz/residual_dist.png'
        ]
    }
    
    print("=" * 80)
    print("🔍 ตรวจสอบความสมบูรณ์ของรูปภาพใน Report")
    print("=" * 80)
    
    all_valid = True
    total_checked = 0
    
    for category, images in required_images.items():
        print(f"\n📂 {category}")
        print("-" * 80)
        
        for image_path in images:
            total_checked += 1
            filename = os.path.basename(image_path)
            
            if not os.path.exists(image_path):
                print(f"❌ {filename:<35} - ไม่พบไฟล์")
                all_valid = False
                continue
            
            result = check_image_integrity(image_path)
            
            if result['valid']:
                print(f"✅ {filename:<35} - {result['format']:<5} "
                      f"{result['width']}x{result['height']:<6} "
                      f"({result['size_kb']:.2f} KB)")
            else:
                print(f"❌ {filename:<35} - เสียหาย: {result['error']}")
                all_valid = False
    
    print("\n" + "=" * 80)
    if all_valid:
        print(f"✅ สำเร็จ! ตรวจสอบรูปภาพทั้งหมด {total_checked} รูป - ทุกรูปสมบูรณ์")
        print("=" * 80)
        return 0
    else:
        print(f"❌ พบปัญหา! กรุณาตรวจสอบรูปภาพที่มีปัญหา")
        print("=" * 80)
        return 1

if __name__ == "__main__":
    sys.exit(main())
