# 🎨 Roo-Lot v4.0 - Modern Multi-Theme Dashboard

## 📋 Overview

Version 4.0 is a complete UI/UX overhaul of the Roo-Lot electricity bill predictor, featuring a **React-inspired design system** with **3 beautiful themes** and a modern, card-based layout.

### ✨ Key Features

- 🎨 **3 Premium Themes**: Dark, Muji (Minimalist Japanese), Minimal (Clean White)
- 🌍 **Bilingual Support**: Thai & English with instant switching
- 📱 **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- ⚡ **Modern UI Components**: Cards, gauges, badges, and smooth animations
- 🎯 **React-Inspired Layout**: 5/12 + 7/12 column grid system
- 🚀 **Performance Optimized**: Form batching, cached model loading

---

## 🏗️ Architecture

### File Structure

```
roo-lot/
├── app_v4_modern_dashboard.py      # Main application (NEW)
├── utils/
│   ├── theme_system.py             # Theme engine with 3 themes (NEW)
│   ├── charts.py                   # Gauge & chart components (NEW)
│   └── theme_manager.py            # Legacy (kept for v3 compatibility)
├── models/
│   └── model_v2_next_month.pkl     # ML model
└── data/
    └── ...
```

### Component Hierarchy

```
app_v4_modern_dashboard.py
├── Theme System (theme_system.py)
│   ├── Dark Theme (Cyan accent)
│   ├── Muji Theme (Terracotta accent)
│   └── Minimal Theme (Green accent)
├── Charts (charts.py)
│   ├── Modern Gauge Chart
│   ├── Simple Arc Gauge (SVG alternative)
│   ├── Mini Sparkline
│   └── Status Indicator
└── UI Components
    ├── Sidebar Navigation
    ├── Input Form Card (Left Column)
    ├── Result Card with Gauge (Right Column - Top)
    └── History Table (Right Column - Bottom)
```

---

## 🎨 Theme System

### Theme Definitions

#### 1. **Dark Theme** 🌙
- **Primary Color**: Cyan (#06b6d4)
- **Background**: Rich blacks (#0a0a0a, #121212)
- **Best For**: Night usage, reducing eye strain
- **Mood**: Professional, modern, tech-focused

#### 2. **Muji Theme** ☕
- **Primary Color**: Terracotta (#C77B58)
- **Background**: Warm beige/cream (#F5F1E8, #EAE4D9)
- **Best For**: Daytime usage, natural aesthetics
- **Mood**: Calm, minimalist, Japanese-inspired

#### 3. **Minimal Theme** 🌿
- **Primary Color**: Green (#2E7D32)
- **Background**: Clean white (#FFFFFF, #F8F9FA)
- **Best For**: High contrast, accessibility
- **Mood**: Fresh, clean, eco-friendly

### How Themes Work

```python
# In theme_system.py
THEMES = {
    'dark': { 'colors': { ... } },
    'muji': { 'colors': { ... } },
    'minimal': { 'colors': { ... } }
}

def generate_css(theme_name: str) -> str:
    """Generates complete CSS with CSS variables"""
    theme = THEMES[theme_name]
    # Injects :root { --bg-primary: ...; --accent-primary: ...; }
    return css_string
```

**CSS Variables** are used throughout, allowing instant theme switching:
```css
:root {
    --bg-primary: #0a0a0a;
    --accent-primary: #06b6d4;
    --text-heading: #ffffff;
}

.card {
    background: var(--bg-card);
    color: var(--text-heading);
}
```

---

## 📐 Layout System

### React Grid Implementation

Following the React code's `grid-cols-12` system:

```
┌─────────────────────────────────────────────────────┐
│  SIDEBAR (240px)  │  LEFT (5/12)   │  RIGHT (7/12)  │
│                   │                │                 │
│  • Logo           │  INPUT FORM    │  RESULT CARD   │
│  • Navigation     │  • Date/Time   │  • Gauge       │
│  • Theme Switch   │  • Units       │  • Status      │
│  • Lang Toggle    │  • People      │                │
│  • User Profile   │  • Factors     │  HISTORY TABLE │
│                   │  • [Predict]   │  • Recent runs │
│                   │                │  • Export      │
└─────────────────────────────────────────────────────┘
```

**Streamlit Implementation:**
```python
col_left, col_right = st.columns([5, 7], gap="large")

with col_left:
    # Input Form Card
    render_input_form()

with col_right:
    # Result Card
    render_result_card()
    # History Card
    render_history_table()
```

---

## 🎯 Key UI Components

### 1. **Modern Gauge Chart**

Located in `utils/charts.py`:

```python
def create_modern_gauge(value, theme_colors, lang='th'):
    """
    Creates a Plotly gauge with:
    - Color-coded ranges (Low/Moderate/High)
    - Theme-aware colors
    - Smooth animations
    """
```

**Features:**
- Dynamic color based on value (Green < 500, Orange < 1000, Red > 1000)
- Matches theme's accent colors
- Bilingual unit labels

### 2. **Card System**

Every major section is wrapped in a `.card`:

```python
st.markdown('<div class="card">', unsafe_allow_html=True)
# Content here
st.markdown('</div>', unsafe_allow_html=True)
```

**Card Features:**
- Hover shadow effects
- Rounded corners (16px radius)
- Proper spacing and padding
- Theme-aware borders

### 3. **Status Badges**

```python
.status-badge.success { 
    background: rgba(16, 185, 129, 0.1);
    color: var(--success);
    border: 1px solid var(--success);
}
```

**Types:**
- Success (Green) - Normal usage
- Warning (Orange) - Moderate usage
- Error (Red) - High usage
- Info (Blue) - Special events

### 4. **History Table**

Custom HTML table (not `st.dataframe`) for full styling control:

```html
<table class="history-table">
    <thead>...</thead>
    <tbody>
        <tr>
            <td class="timestamp">2026-02-12 08:00</td>
            <td><span class="status-badge">Yes</span></td>
            <td>845.5</td>
            <td><span class="status-badge success">Normal</span></td>
        </tr>
    </tbody>
</table>
```

---

## 🔧 Technical Implementation

### Session State Management

```python
# Initialize in main()
if 'language' not in st.session_state:
    st.session_state.language = 'th'

if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

if 'prediction' not in st.session_state:
    st.session_state.prediction = None
```

### Theme Switching Flow

```
User clicks theme button (e.g., ☕)
    ↓
st.session_state.theme = 'muji'
    ↓
st.rerun()
    ↓
generate_css('muji') called
    ↓
New CSS injected with --accent-primary: #C77B58
    ↓
All components update instantly
```

### Form Optimization

Using `st.form` to batch updates:

```python
with st.form("prediction_form"):
    current_unit = st.number_input(...)
    lag1_unit = st.number_input(...)
    # ... more inputs
    
    predict_clicked = st.form_submit_button()
```

**Benefits:**
- Prevents rerun on every input change
- Better UX with single "Predict" action
- Reduces API calls/model runs

---

## 🌍 Localization

### Translation System

```python
TRANSLATIONS = {
    'en': {
        'appTitle': "Roo-Lot",
        'headerTitle': "Electricity Bill Predictor",
        # ... 40+ keys
    },
    'th': {
        'appTitle': "รู้หลอด",
        'headerTitle': "ทำนายค่าไฟฟ้า",
        # ... 40+ keys
    }
}

# Usage
T = TRANSLATIONS[lang]
st.markdown(T['headerTitle'])
```

### Language Toggle

Located in sidebar:
- 🇹🇭 ไทย button
- 🇺🇸 EN button
- Active state with `type="primary"`
- Instant switch with `st.rerun()`

---

## 🚀 Running the Application

### Quick Start

```bash
# Navigate to project directory
cd roo-lot

# Activate virtual environment (if using)
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Run v4 app
streamlit run app_v4_modern_dashboard.py
```

### First Time Setup

```bash
# Install dependencies
pip install streamlit pandas numpy joblib plotly scikit-learn

# Ensure model exists
ls models/model_v2_next_month.pkl

# Run
streamlit run app_v4_modern_dashboard.py
```

---

## 🎮 User Guide

### Switching Themes

1. Look at the **sidebar** (left panel)
2. Find the "THEME" section
3. Click on theme icons:
   - 🌙 = Dark
   - ☕ = Muji
   - 🌿 = Minimal
4. App refreshes instantly with new theme

### Making Predictions

1. **Input Parameters** (left card):
   - Select date and time
   - Enter current month units (kWh)
   - Enter previous month units
   - Set number of people
   - Choose target month
   - Toggle school break if applicable

2. **Click "Run Prediction"** (เริ่มการทำนาย)

3. **View Results** (right top card):
   - Large number shows predicted units
   - Gauge chart visualizes the value
   - Status badge shows usage category
   - Confidence indicator shows accuracy

4. **Check History** (right bottom card):
   - Recent predictions listed
   - Export to CSV available

---

## 📊 Comparison: v3 vs v4

| Feature | v3 (Dark Dashboard) | v4 (Modern Multi-Theme) |
|---------|---------------------|-------------------------|
| **Themes** | 1 (Dark only) | 3 (Dark, Muji, Minimal) |
| **Layout** | 3-column (Sidebar, Main, Preview) | React-inspired (5/12 + 7/12) |
| **Input Style** | Basic Streamlit widgets | Form-wrapped with styled containers |
| **Gauge** | Fixed colors | Theme-adaptive colors |
| **History** | Likely `st.dataframe` | Custom HTML table with badges |
| **Icons** | Emojis | Emojis (keeping it light) |
| **Navigation** | Basic sidebar items | Styled nav items with active state |
| **Responsiveness** | Standard | Optimized with breakpoints |
| **CSS Variables** | Hardcoded colors | CSS variables for theming |

### Migration Path

Keeping **v3** for compatibility:
- `app_v3_dark_dashboard.py` → Single dark theme, stable
- `app_v4_modern_dashboard.py` → Multi-theme, modern UI

Users can choose which version to run based on needs.

---

## 🎨 Design Philosophy

### Ported from React

The original React code provided clear design patterns:

1. **Component-Based**: Each UI section is a function
2. **Theme System**: CSS variables for dynamic theming
3. **Card Layout**: Everything in bordered, shadowed cards
4. **Status Colors**: Semantic color-coding (success/warning/error)
5. **Typography**: Clear hierarchy with size/weight variations

### Streamlit Adaptations

Some React features require workarounds:

| React Feature | Streamlit Solution |
|---------------|-------------------|
| `useState` hooks | `st.session_state` |
| `onClick` handlers | `st.button` with `if` checks |
| CSS-in-JS | CSS string with `st.markdown(..., unsafe_allow_html=True)` |
| Conditional rendering | Python `if/else` blocks |
| Form validation | Custom `validate_unit_input()` function |

---

## 🔮 Future Enhancements

### Potential v4.1 Features

1. **More Themes**:
   - Dracula
   - Nord
   - Solarized

2. **Theme Customizer**:
   - Let users adjust accent colors
   - Save custom themes to JSON

3. **Advanced Charts**:
   - Historical trend sparklines
   - Month-over-month comparison bars
   - Usage heatmap calendar

4. **Real History**:
   - Store predictions in database
   - Show actual history from user's data

5. **Export Options**:
   - PDF reports
   - Email predictions
   - API endpoints

---

## 🐛 Troubleshooting

### Theme Not Changing

**Issue**: Theme buttons clicked but UI stays the same

**Solution**:
```python
# Check session_state in sidebar:
st.write(st.session_state.theme)  # Debug line

# Ensure st.rerun() is called after changing theme
```

### Gauge Not Displaying

**Issue**: Blank space where gauge should be

**Possible causes**:
1. Plotly not installed: `pip install plotly`
2. Theme colors missing: Check `theme_system.py` has `gauge_base` and `gauge_fill`
3. Value is None: Check prediction logic

### Model Not Found

**Issue**: "Model not found" error on start

**Solution**:
```bash
# Check model exists
ls roo-lot/models/model_v2_next_month.pkl

# Retrain if missing
python scripts/retrain_v2.py
```

### CSS Not Applying

**Issue**: Colors look wrong or default Streamlit style

**Solution**:
```python
# Ensure CSS is generated and injected
css = generate_css(theme)
st.markdown(css, unsafe_allow_html=True)

# Check CSS variables in browser DevTools
# Should see :root { --bg-primary: ... }
```

---

## 📝 Code Examples

### Adding a New Theme

1. Edit `utils/theme_system.py`:

```python
THEMES = {
    # ... existing themes ...
    
    'nord': {
        'name': 'Nord',
        'icon': '❄️',
        'colors': {
            'bg_primary': '#2E3440',
            'bg_secondary': '#3B4252',
            'bg_card': '#3B4252',
            'bg_input': '#434C5E',
            'accent_primary': '#88C0D0',
            'accent_hover': '#8FBCBB',
            'text_heading': '#ECEFF4',
            'text_primary': '#D8DEE9',
            'text_muted': '#4C566A',
            # ... complete all keys ...
        }
    }
}
```

2. Theme button appears automatically in sidebar (reads from `get_available_themes()`)

### Customizing Gauge Colors

Edit `utils/charts.py`:

```python
def create_modern_gauge(...):
    # Change thresholds
    if display_value < 300:  # Lower threshold
        bar_color = theme_colors.get('success', '#10b981')
    elif display_value < 800:  # New mid threshold
        bar_color = theme_colors.get('warning', '#f59e0b')
    else:
        bar_color = theme_colors.get('error', '#ef4444')
```

### Adding a New Translation

Edit `app_v4_modern_dashboard.py`:

```python
TRANSLATIONS = {
    'en': {
        # ... existing keys ...
        'newFeature': "New Feature Text",
    },
    'th': {
        # ... existing keys ...
        'newFeature': "ข้อความคุณสมบัติใหม่",
    }
}

# Usage in UI
st.markdown(T['newFeature'])
```

---

## 🏆 Credits

- **Design Inspiration**: React Dashboard UI (provided by user)
- **Theme Colors**: Tailwind CSS palette
- **Architecture**: Streamlit best practices + React component patterns
- **Development**: Roo-Lot Team
- **Version**: 4.0.0 (February 2026)

---

## 📄 License

This project belongs to the AIE322 course, Roo-Lot development team.

---

## 🔗 Quick Links

- **Run v4**: `streamlit run app_v4_modern_dashboard.py`
- **Run v3** (legacy): `streamlit run app_v3_dark_dashboard.py`
- **Theme System**: `utils/theme_system.py`
- **Charts**: `utils/charts.py`
- **Model**: `models/model_v2_next_month.pkl`

---

**Happy Theming! 🎨✨**
