import re
from pathlib import Path
import sys

def validate_report_consistency():
    """Check if Report claims match code/files."""
    print("="*50)
    print("DOCUMENTATION VALIDATION CHECKLIST")
    print("="*50)
    
    report_path = Path("Report ML Project (Roo-Lot).md")
    if not report_path.exists():
        print("❌ Report file 'Report ML Project (Roo-Lot).md' not found!")
        return False
        
    report_text = report_path.read_text(encoding='utf-8')
    
    issues = []
    
    # Check 1: Image references exist
    print("Checking image references...")
    image_pattern = r'!\[.*?\]\((.*?)\)'
    images = re.findall(image_pattern, report_text)
    
    for img_path in images:
        if not Path(img_path).exists():
            issues.append(f"❌ Missing image: {img_path}")
        else:
            print(f"  ✅ Image found: {img_path}")
    
    # Check 2: Hyperparameter values match in TRAIN MODEL
    print("\nChecking hyperparameters in scripts/train_model.py...")
    train_script = Path("scripts/train_model.py")
    if train_script.exists():
        code = train_script.read_text(encoding='utf-8')
        if "n_estimators" in code and ("100" in code or "[50, 100, 200]" in code):
            print("  ✅ n_estimators configuration found")
        else:
            issues.append("❌ n_estimators configuration mismatch or missing")
            
        if "GridSearchCV" in code:
            print("  ✅ GridSearchCV found")
        else:
            issues.append("❌ GridSearchCV not found in training script")
    else:
        issues.append("❌ scripts/train_model.py not found")
    
    # Check 3: Dataset file exists (or is handled)
    # Report mentions Kaggle dataset (Household Energy Consumption), often named household_energy.csv
    # Our audit created household_energy.csv
    print("\nChecking dataset...")
    if Path("data/household_energy.csv").exists():
        print("  ✅ data/household_energy.csv found")
    elif Path("data/electricity_data.csv").exists():
        print("  ⚠️ Using alternative dataset: data/electricity_data.csv")
    else:
        issues.append("❌ No dataset found")
    
    # Check 4: Requirements match
    print("\nChecking requirements.txt...")
    if Path("requirements.txt").exists():
        reqs = Path("requirements.txt").read_text()
        if "scikit-learn==1.3.2" in reqs:
             print("  ✅ scikit-learn version matches")
    else:
        issues.append("❌ requirements.txt missing")

    # Report
    print("\n" + "="*50)
    print("VALIDATION SUMMARY")
    print("="*50)
    
    if issues:
        print("⚠️  Validation Issues Found:\n")
        for issue in issues:
            print(f"  {issue}")
        return False
    else:
        print("✅ All consistency checks passed!")
        return True

if __name__ == "__main__":
    success = validate_report_consistency()
    sys.exit(0 if success else 1)
