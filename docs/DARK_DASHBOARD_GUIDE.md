# Roo-Lot v3.0.0 - Dark Professional Dashboard Guide

## ภาพรวม

Roo-Lot v3.0.0 เป็นการอัปเกรด UI สู่ **Dark Modern Professional Dashboard** ตามแบบ Invoice Management System ที่ดูสะอาดตา มืออาชีพ และใช้งานง่าย

### จุดเด่นของเวอร์ชันนี้

- **3-Column Layout**: Sidebar + Main Content + Live Preview
- **Dark Theme**: โทนสีดำสะอาดตา (#1A1A1A, #242424)
- **Orange Accent**: สีส้มเน้น (#F97316) สำหรับปุ่มและไฮไลท์
- **Real-time Preview**: ผลลัพธ์อัปเดตแบบเรียลไทม์ในแผงขวา
- **Bilingual Support**: รองรับทั้งไทยและอังกฤษ

---

## Design System

### Color Palette

```css
/* Backgrounds */
--bg-primary: #1A1A1A;      /* Main background */
--bg-secondary: #242424;    /* Sidebar, cards */
--bg-tertiary: #2D2D2D;     /* Input fields */
--bg-elevated: #333333;     /* Hover states */

/* Text */
--text-primary: #FFFFFF;      /* Headers */
--text-secondary: #A0A0A0;    /* Labels */
--text-tertiary: #707070;     /* Placeholders */

/* Accent */
--accent-primary: #F97316;    /* Orange brand */
--accent-hover: #FB923C;      /* Lighter orange */

/* Borders */
--border-subtle: #333333;
--border-focus: #F97316;
```

### Typography

- **Font Thai**: Prompt, Noto Sans Thai
- **Font English**: Inter, -apple-system
- **Title**: 28px, weight 600
- **Section**: 16px, weight 600
- **Body**: 14px, weight 400
- **Caption**: 13px, weight 400

### Spacing

- Section gap: 24px
- Card padding: 24px
- Input padding: 10px 14px
- Border radius: 8px (inputs), 12px (cards)

---

## Layout Structure

```
┌─────────────────────────────────────────────────────────────┐
│ [Sidebar: 240px] │ [Main Content]      │ [Preview: 400px]  │
│                  │                      │                    │
│  💡 รู้หลอด       │  Home / Invoice      │  Result            │
│  [Search...]     │                      │  ─────────────     │
│                  │  ทำนายค่าไฟเดือนหน้า  │                    │
│  MENU            │  ─────────────────── │  ฿1,250            │
│  • Dashboard     │                      │  [Moderate]        │
│  • Transactions  │  [Usage Details]     │                    │
│  • Wallet        │  ┌────────────────┐  │  Input: 150 kWh    │
│  ► Invoice       │  │ Current: [150] │  │  Change: +7.1%     │
│  • Budgeting     │  │ Previous: [140]│  │  Rate: 8.33 ฿      │
│  • Reports       │  │ People: [2]    │  │  Month: Feb        │
│                  │  │ Break: [Toggle]│  │                    │
│  [User Profile]  │  └────────────────┘  │  [Download CSV]    │
│                  │                      │                    │
│  🇹🇭 | 🇺🇸        │  [Predict Button]    │                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Components

### 1. Sidebar Navigation

```python
# Features:
- Logo with icon (💡)
- Search bar
- Navigation menu with active state
- Language toggle (segmented control)
- User profile card
```

### 2. Form Section

```python
# Features:
- Breadcrumbs navigation
- Section title + description
- 2-column input layout
- Number inputs with validation
- Selectbox for month
- Toggle switch for school break
- Primary CTA button (full-width)
```

### 3. Preview Panel

```python
# Features:
- Large amount display
- Status badge (color-coded)
- Metrics grid (4 items)
- Conditional notes
- CSV download button
- Empty state placeholder
```

---

## Usage

### เริ่มต้นใช้งาน

```bash
cd roo-lot
python -m streamlit run app_v3_dark_dashboard.py
```

### การทำนายค่าไฟ

1. กรอก **หน่วยไฟเดือนปัจจุบัน** (kWh)
2. กรอก **หน่วยไฟเดือนที่แล้ว** (kWh)
3. เลือก **จำนวนคน**ในบ้าน
4. เลือก **เดือนที่ต้องการทำนาย**
5. ตั้งค่า **ช่วงปิดเทอม** (ถ้ามี)
6. กดปุ่ม **"ทำนายค่าไฟ"**
7. ดูผลลัพธ์ในแผงขวา

### เปลี่ยนภาษา

- คลิกที่ toggle 🇹🇭 หรือ 🇺🇸 ใน Sidebar
- หรือใช้ `st.session_state.language = 'th'` หรือ `'en'`

---

## File Structure

```
roo-lot/
├── app_v3_dark_dashboard.py    # Main application
├── app.py                       # Previous version (v2.1)
├── docs/
│   ├── DARK_DASHBOARD_GUIDE.md  # This file
│   └── UI_GUIDE.md
├── models/
│   └── model_v2_next_month.pkl  # ML model
└── utils/
    └── theme_manager.py         # Theme utilities
```

---

## Customization

### เปลี่ยนสีหลัก (Accent Color)

แก้ไขใน CSS section:

```python
--accent-primary: #F97316;    # เปลี่ยนเป็นสีที่ต้องการ
--accent-hover: #FB923C;
```

### เพิ่มเมนูใน Sidebar

```python
menu_items = [
    ('📊', t['dashboard'], False),
    ('💳', t['transactions'], False),
    # เพิ่มเมนูใหม่ที่นี่
    ('🆕', 'New Menu', False),
]
```

### ปรับขนาด Layout

```python
# ใน main():
sidebar_col, main_col, preview_col = st.columns([1, 3, 2])
# ปรับสัดส่วนได้ตามต้องการ
```

---

## Technical Details

### Session State Variables

```python
st.session_state.language      # 'th' หรือ 'en'
st.session_state.prediction    # ผลการทำนาย (float)
st.session_state.prediction_inputs  # ข้อมูลที่กรอก (dict)
```

### Translation System

```python
TRANSLATIONS = {
    'th': {
        'key': 'ค่าไทย',
    },
    'en': {
        'key': 'English Value',
    }
}

# ใช้งาน:
t = TRANSLATIONS[lang]
label = t['key']
```

### Model Input Format

```python
input_data = pd.DataFrame({
    'current_unit': [150],    # หน่วยปัจจุบัน
    'is_break': [0],          # 0 หรือ 1
    'month': [2],             # 1-12
    'people': [2],            # จำนวนคน
    'lag1_unit': [140]        # หน่วยเดือนที่แล้ว
})
```

---

## Responsive Behavior

| Viewport | Sidebar | Preview Panel | Main Content |
|----------|---------|---------------|--------------|
| > 1200px | 240px   | 400px         | Flexible     |
| < 1200px | 240px   | Hidden        | Flexible     |
| < 768px  | Collapsed | Hidden      | Full-width   |

---

## Changelog

### v3.0.0 (2026-02-12)

- ✨ **New**: Dark Professional Dashboard UI
- ✨ **New**: 3-column layout with live preview
- ✨ **New**: Sidebar navigation with active states
- ✨ **New**: Language toggle in sidebar
- ✨ **New**: Status badges with color coding
- ✨ **New**: Real-time preview panel
- ♻️ **Refactor**: Separated components for maintainability
- 🎨 **Style**: Complete dark theme overhaul
- 📱 **Improve**: Better responsive behavior

---

## Screenshots

### Desktop View
![Desktop](screenshots/desktop.png)

### With Prediction
![Prediction](screenshots/prediction.png)

### Mobile View
![Mobile](screenshots/mobile.png)

---

## Credits

- **Design Reference**: Invoice Management Dashboard (Knockturnals Design)
- **Fonts**: Google Fonts (Inter, Prompt)
- **Icons**: Emoji native + custom SVG
- **Framework**: Streamlit 1.45+

---

## License

MIT License - Same as Roo-Lot original project
