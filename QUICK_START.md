# Roo-Lot v2.0.0 - Quick Start Guide

## Getting Started

### 1. Start the Application
```bash
cd c:\Users\com\Documents\AIE322\RooLord\roo-lot
python -m streamlit run app.py
```

The app will open at: **http://localhost:8502**

---

## Theme Switching

### Three Themes Available:

1. **Muji (M)** - Warm minimalist Japanese style
   - Warm beige background
   - Terracotta accents
   - Perfect for: Calm, focused work

2. **Minimal (Mi)** - Clean professional design
   - Pure white background
   - Green accents
   - Perfect for: Professional presentations

3. **Dark (D)** - Eye-friendly dark mode
   - Dark charcoal background
   - Cyan accents
   - Perfect for: Night work, reduced eye strain

### How to Switch:
- **Method 1:** Click theme buttons in sidebar (M, Mi, D)
- **Method 2:** Press keyboard shortcuts: `1`, `2`, or `3`
- Themes persist across browser refreshes

---

## Making a Prediction

### Step 1: Enter Usage Details

**Current Month Unit (kWh):**
- Enter units used this month (0-2000)
- Example: 150

**Number of People:**
- How many people in household (1-10)
- Example: 2

**Previous Month Unit (kWh):**
- Units used last month
- Tip: If unsure, use same as current month

**Target Month:**
- Month to predict
- Default: Next month

**School Break:**
- Are you in school break period?
- Affects usage patterns

### Step 2: Submit
Click **"Predict Next Month Bill"** button

### Step 3: View Results

You'll see:
- **Predicted Bill** in THB (large number)
- **Input Units** metric
- **Usage Change** percentage
- **Estimated Rate/Unit**
- **Usage Category** (Low/Moderate/High)
- Contextual insights

### Step 4: Export (Optional)
Click **"Download Prediction Results (CSV)"** to save

---

## Features Overview

### Input Validation
- Automatically checks for unusual values
- Warns if usage changed >300%
- Helpful error messages

### Prediction History
- View last 5 predictions in sidebar
- Shows time, units, and bill
- Click "Clear History" to reset

### Keyboard Shortcuts
- `1` - Switch to Muji theme
- `2` - Switch to Minimal theme
- `3` - Switch to Dark theme
- `Ctrl+Enter` - Submit form (in form field)

### Responsive Design
- Works on desktop and mobile
- Touch-friendly buttons (44px minimum)
- Automatic layout adjustment

---

## Tips for Accurate Predictions

1. **Use Actual Data:** Enter real usage numbers for best results
2. **Check Previous Month:** More accurate with historical data
3. **Consider Seasonality:** Summer/winter usage may differ
4. **School Breaks Matter:** Usage patterns change during breaks
5. **Review Warnings:** Pay attention to validation messages

---

## Troubleshooting

### Model Not Found Error
```
WARNING: Model not found!
Please run: python scripts/retrain_v2.py
```

**Solution:** Train the model first
```bash
python scripts/retrain_v2.py
```

### Theme Not Changing
- Try hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
- Clear browser cache
- Check browser console for errors (F12)

### Prediction Seems Wrong
- Verify input values are correct
- Check if validation warnings appeared
- Review usage category (Low/Moderate/High)
- Consider if month has different patterns

---

## Testing the Application

### Run All Tests
```bash
python -m pytest tests/ -v
```

Expected: **31 passed, 2 skipped**

### Run with Coverage
```bash
python -m pytest tests/ --cov=. --cov-report=html
```

View coverage report: `htmlcov/index.html`

---

## File Structure

```
roo-lot/
├── app.py                          # Main application (v2.0.0)
├── utils/
│   ├── __init__.py
│   └── theme_manager.py            # Theme system
├── tests/
│   ├── __init__.py
│   ├── test_theme_manager.py       # Theme tests
│   └── test_app_integration.py     # App tests
├── .streamlit/
│   ├── config.toml                 # Default theme
│   └── themes/
│       ├── muji.toml               # Muji theme
│       ├── minimal.toml            # Minimal theme
│       └── dark.toml               # Dark theme
├── docs/
│   └── FRONTEND_UPGRADE_DEV_DOCS.md
├── CHANGELOG.md
├── IMPLEMENTATION_SUMMARY.md
└── requirements.txt
```

---

## What's New in v2.0.0

### Removed
- All emoji from codebase (12 instances)
- Hardcoded styling

### Added
- Multi-theme system (3 themes)
- Input validation
- Prediction history tracking
- CSV export
- Usage insights
- Enhanced error handling
- Performance monitoring
- Comprehensive tests (33 test cases)
- Complete documentation

### Improved
- Code quality (type hints, docstrings)
- Accessibility (WCAG 2.1 AA compliant)
- Mobile responsiveness
- User experience

---

## Support

**Documentation:**
- Development Guide: `docs/FRONTEND_UPGRADE_DEV_DOCS.md`
- Implementation Summary: `IMPLEMENTATION_SUMMARY.md`
- Changelog: `CHANGELOG.md`

**Testing:**
- Theme Manager Tests: `tests/test_theme_manager.py`
- App Integration Tests: `tests/test_app_integration.py`

**Version:** 2.0.0  
**Status:** Production Ready

---

## Quick Commands

```bash
# Start app
python -m streamlit run app.py

# Run tests
python -m pytest tests/ -v

# Install dependencies
pip install -r requirements.txt

# Train model
python scripts/retrain_v2.py
```

---

**Enjoy your upgraded Roo-Lot experience!**
