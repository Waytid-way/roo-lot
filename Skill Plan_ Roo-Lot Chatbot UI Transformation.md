# 🎯 Skill Plan: Roo-Lot Chatbot UI Transformation

ผมได้วิเคราะห์โครงการ [Roo-Lot](https://github.com/Waytid-way/roo-lot) และความสามารถของ Google Antigravity IDE แล้ว มาวางแผนการสร้าง Skill แบบ High Effort กันครับ

## 📋 Executive Summary

เป้าหมายคือเปลี่ยน Roo-Lot จาก Streamlit form-based UI เป็น **Conversational Chatbot Interface** ที่มี smooth micro-animations โดยคง ML pipeline เดิม (Lasso Regression Model, R² = 99.23%) แต่เปลี่ยนวิธีการ interact ทั้งหมด

## 🏗️ Architecture Overview

### Current State Analysis

- **Tech Stack:** Streamlit + Scikit-learn + Plotly
- **Current UI:** Traditional form inputs (sliders, number inputs)
- **Interaction Pattern:** Single-page form submission
- **Model:** Lasso Regression (.pkl file)


### Target State Design

- **New UI Pattern:** Multi-turn conversational interface
- **State Management:** Session-based chat history
- **Animation Layer:** Custom CSS + Streamlit components
- **Response Format:** Progressive disclosure with card-based results


## 🎨 Detailed UI/UX Specification

### 1. Landing Page (Hero Screen)

```
Component Hierarchy:
├── Full-screen container (gradient background)
├── Center-aligned content
│   ├── Logo/Icon (animated on load)
│   ├── Headline: "ทำนายค่าไฟฟ้าด้วย AI"
│   ├── Subheadline: "รู้อะไร ไม่เท่ารู้หลอด"
│   └── CTA Button
│       ├── Style: White bg, black text, rounded-lg
│       ├── Text: "ลองใช้รู้หลอดเลย (ฟรีนะ)"
│       └── Hover: Scale animation (1.0 → 1.05)
```

**Animation Sequence:**

- Fade in logo (300ms)
- Slide up headline (400ms, delay: 100ms)
- Fade in button (300ms, delay: 200ms)
- Pulse animation on button (infinite, subtle)


### 2. Chat Interface

#### Sidebar (Left Panel - 280px width)

```
Structure:
├── New Chat Button
│   ├── Icon: "+" 
│   ├── Text: "New Chat"
│   ├── Style: Full-width, rounded, hover lift
│   └── Action: Reset conversation state
├── Chat History (Scrollable)
│   ├── Bento-style cards (stacked)
│   ├── Each card shows:
│   │   ├── Timestamp
│   │   ├── Preview (first question)
│   │   └── Predicted bill (if completed)
│   └── Hover: Background highlight + lift
└── Settings Button (Bottom-fixed)
    ├── Icon: Gear/Settings
    ├── Text: "ตั้งค่า"
    └── Action: Open settings modal
```

**Sidebar Animations:**

- Slide in from left (300ms, ease-out)
- History items: Staggered fade-in (50ms delay each)
- Settings button: Fade in (400ms)


#### Main Chat Area

```
Layout:
├── Header Bar
│   ├── Bot Avatar (circular, 40px)
│   ├── Bot Name: "Roo-Lot Assistant"
│   └── Status indicator (online/typing)
├── Messages Container (Scrollable)
│   ├── Bot Messages (left-aligned)
│   │   ├── Avatar (30px)
│   │   ├── Message bubble (rounded-2xl, bg-gray-100)
│   │   └── Timestamp
│   ├── User Messages (right-aligned)
│   │   ├── Message bubble (rounded-2xl, bg-blue-500, text-white)
│   │   └── Timestamp
│   └── Result Card (when prediction ready)
│       ├── Dark card (black bg, rounded-lg)
│       ├── Preview content:
│       │   ├── "ค่าไฟเดือนหน้า"
│       │   ├── Predicted amount (large text)
│       │   ├── Range: "±XX บาท"
│       │   └── CTA: "กดเพื่อดูผลลัพธ์เชิงลึก"
│       └── Click → Expand to full analysis
└── Input Bar (Bottom-fixed)
    ├── Text input (rounded-full)
    ├── Send button (icon)
    └── Typing indicator (when bot is "thinking")
```

**Message Animations:**

- New message: Slide up + fade in (300ms)
- Bot typing: 3-dot pulse animation
- Result card: Scale in (400ms, spring easing)
- Card expansion: Smooth height transition (500ms)


### 3. Conversation Flow

**Question Sequence (6 questions):**

1. "สวัสดีครับ! ผมจะช่วยคุณทำนายค่าไฟฟ้า 🔮 เริ่มกันเลยนะครับ ห้องของคุณใหญ่กี่ตารางเมตรครับ?"
2. "ดีครับ! แล้วคุณเปิดแอร์กี่ชั่วโมงต่อวันครับ?"
3. "เข้าใจแล้ว มีพัดลมกี่ตัวในห้องครับ?"
4. "โอเคครับ แล้วหลอดไฟในห้องมีกี่ดวงครับ?"
5. "ครบแล้วเกือบหมด! มีคอมพิวเตอร์/โน้ตบุ๊คกี่เครื่องครับ?"
6. "คำถามสุดท้าย! มีเครื่องใช้ไฟฟ้าอื่นๆ รวมกี่ชิ้นครับ? (เช่น ตู้เย็น, ไมโครเวฟ)"

**Input Validation:**

- Real-time validation (non-negative numbers)
- Error messages (gentle, inline)
- Suggestion chips (quick replies with common values)


### 4. Results Display

#### Initial Card (Collapsed State)

```css
Card Style:
- Background: #000000
- Border-radius: 16px
- Padding: 24px
- Box-shadow: 0 8px 24px rgba(0,0,0,0.15)
- Cursor: pointer
- Transition: all 0.3s ease

Content:
├── Icon: ⚡ (animated pulse)
├── "ค่าไฟเดือนหน้า"
├── Amount: "XXX บาท" (gradient text, large)
├── Range: "คลาดเคลื่อน ±YY บาท" (smaller)
└── CTA: "กดเพื่อดูผลลัพธ์เชิงลึก" (with arrow →)
```


#### Expanded Card (Detailed View)

```
Sections (vertical scroll):
├── Summary
│   ├── Predicted amount
│   └── Confidence range
├── Model Performance
│   ├── R² Score: 99.23%
│   ├── MAE: ~43.63 บาท
│   └── RMSE: ~58.41 บาท
├── Cost Breakdown (Plotly chart)
│   ├── AC cost
│   ├── Appliances cost
│   └── Base fee
├── Usage Insights
│   ├── Comparison to average
│   └── Saving suggestions
└── Actions
    ├── "ดาวน์โหลดรายงาน" (PDF)
    └── "แชร์ผลลัพธ์" (Share link)
```

**Expansion Animation:**

- Height: Auto-expand (600ms, ease-out)
- Content: Staggered fade-in (sections appear sequentially)
- Chart: Animate bars/lines (800ms)


### 5. Follow-up Interaction

After showing results, bot sends:

```
"ลองทำนายอีกรอบมั้ยครับ? 🤔"

[Buttons]
├── "ลองอีกครั้ง" → Reset conversation
└── "ปรับค่าเดิม" → Pre-fill previous values
```


## 🛠️ Technical Implementation Plan

### Phase 1: Foundation (Week 1)

**Objective:** Setup conversational state management

**Tasks:**

1. **Create new file:** `app_chatbot.py`
2. **Implement conversation state:**

```python
# Session state structure
st.session_state = {
    'conversation_stage': 0,  # 0-6 (landing → result)
    'messages': [],  # [{role, content, timestamp}]
    'user_inputs': {},  # Collected form data
    'chat_history': [],  # Previous conversations
    'current_prediction': None,
    'show_detailed_results': False
}
```

3. **Build conversation engine:**

```python
class ConversationManager:
    QUESTIONS = [...]  # 6 questions
    FIELD_MAPPING = {
        0: 'room_size',
        1: 'ac_hours',
        2: 'fans',
        3: 'lights',
        4: 'computers',
        5: 'other_appliances'
    }
    
    def advance_conversation(self, user_input):
        # Validate input
        # Store in session state
        # Generate next question
        # Trigger prediction if complete
```

4. **Integrate existing ML model:**

```python
def predict_bill(user_inputs):
    # Load model from models/lasso_model.pkl
    # Transform inputs with scaler
    # Generate prediction + confidence interval
    # Return formatted result
```


**Deliverables:**

- Working conversation flow (text-only)
- Prediction integration
- State persistence


### Phase 2: UI Components (Week 2)

**Objective:** Build styled components with Streamlit + CSS

**Component Library:**

1. **Landing Page Component:**

```python
def render_landing_page():
    st.markdown("""
        <style>
        .hero-container {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .cta-button {
            background: white;
            color: black;
            border-radius: 9999px;
            padding: 16px 48px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .cta-button:hover {
            transform: scale(1.05);
            box-shadow: 0 12px 32px rgba(0,0,0,0.2);
        }
        </style>
    """, unsafe_allow_html=True)
    
    if st.button("ลองใช้รู้หลอดเลย (ฟรีนะ)", key="cta"):
        st.session_state.conversation_stage = 1
        st.rerun()
```

2. **Chat Message Component:**

```python
def render_message(role, content, timestamp):
    alignment = "flex-end" if role == "user" else "flex-start"
    bg_color = "#3B82F6" if role == "user" else "#F3F4F6"
    text_color = "white" if role == "user" else "black"
    
    st.markdown(f"""
        <div style="display: flex; justify-content: {alignment}; margin: 12px 0;">
            <div style="
                background: {bg_color};
                color: {text_color};
                border-radius: 20px;
                padding: 12px 20px;
                max-width: 70%;
                animation: slideUp 0.3s ease-out;
            ">
                {content}
            </div>
        </div>
    """, unsafe_allow_html=True)
```

3. **Result Card Component:**

```python
def render_result_card(prediction_data):
    expanded = st.session_state.show_detailed_results
    
    st.markdown(f"""
        <div onclick="expandCard()" style="
            background: #000;
            color: white;
            border-radius: 16px;
            padding: 24px;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 20px 0;
        ">
            <div style="font-size: 14px; opacity: 0.8;">ค่าไฟเดือนหน้า</div>
            <div style="font-size: 48px; font-weight: bold; margin: 8px 0;">
                {prediction_data['amount']} บาท
            </div>
            <div style="font-size: 14px; opacity: 0.7;">
                คลาดเคลื่อน ±{prediction_data['range']} บาท
            </div>
            <div style="margin-top: 16px; font-size: 14px;">
                กดเพื่อดูผลลัพธ์เชิงลึก →
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if expanded:
        render_detailed_analysis(prediction_data)
```

4. **Sidebar Component:**

```python
def render_sidebar():
    with st.sidebar:
        # New Chat Button
        if st.button("➕ New Chat", use_container_width=True):
            reset_conversation()
        
        st.markdown("---")
        
        # Chat History
        st.subheader("ประวัติแชท")
        for idx, chat in enumerate(st.session_state.chat_history):
            with st.container():
                st.markdown(f"""
                    <div style="
                        background: #F9FAFB;
                        border-radius: 12px;
                        padding: 12px;
                        margin: 8px 0;
                        cursor: pointer;
                    ">
                        <div style="font-size: 12px; opacity: 0.6;">
                            {chat['timestamp']}
                        </div>
                        <div style="font-weight: 600; margin: 4px 0;">
                            {chat['predicted_bill']} บาท
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        # Settings Button (bottom)
        st.markdown("---")
        if st.button("⚙️ ตั้งค่า", use_container_width=True):
            show_settings_modal()
```


**Deliverables:**

- All UI components styled
- Responsive layout
- Cross-browser compatibility


### Phase 3: Animation Layer (Week 3)

**Objective:** Add smooth micro-animations

**Animation Library:**

1. **CSS Keyframes:**

```css
@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

@keyframes scaleIn {
    from {
        opacity: 0;
        transform: scale(0.9);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}
```

2. **Typing Indicator:**

```python
def render_typing_indicator():
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 8px; padding: 12px;">
            <div class="dot" style="
                width: 8px;
                height: 8px;
                background: #9CA3AF;
                border-radius: 50%;
                animation: pulse 1.4s ease-in-out infinite;
            "></div>
            <div class="dot" style="
                animation-delay: 0.2s;
            "></div>
            <div class="dot" style="
                animation-delay: 0.4s;
            "></div>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(1)  # Simulate thinking time
```

3. **Smooth Scrolling:**

```javascript
// Inject via st.components.v1.html
const scrollToBottom = () => {
    const chatContainer = document.querySelector('.chat-container');
    chatContainer.scrollTo({
        top: chatContainer.scrollHeight,
        behavior: 'smooth'
    });
};

// Auto-scroll on new message
window.addEventListener('newMessage', scrollToBottom);
```

4. **Page Transitions:**

```python
def transition_to_chat():
    # Fade out landing
    st.markdown("""
        <style>
        .hero-container {
            animation: fadeOut 0.3s ease-out forwards;
        }
        </style>
    """, unsafe_allow_html=True)
    
    time.sleep(0.3)
    st.session_state.conversation_stage = 1
    st.rerun()
```


**Deliverables:**

- All animations implemented
- Smooth transitions between states
- Performance optimized (60fps target)


### Phase 4: Advanced Features (Week 4)

**Objective:** Polish and add extra functionality

**Features:**

1. **Chart Animations (Plotly):**

```python
import plotly.graph_objects as go

def create_animated_cost_breakdown(data):
    fig = go.Figure()
    
    # Add bars with animation
    fig.add_trace(go.Bar(
        x=['แอร์', 'เครื่องใช้ไฟฟ้า', 'ค่าพื้นฐาน'],
        y=[data['ac_cost'], data['appliances_cost'], data['base_fee']],
        marker=dict(
            color=['#3B82F6', '#10B981', '#F59E0B'],
        ),
        text=[f"{v:.0f} บาท" for v in [...]],
        textposition='auto',
    ))
    
    # Animation config
    fig.update_layout(
        transition={'duration': 800, 'easing': 'cubic-in-out'},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    return fig
```

2. **Quick Reply Chips:**

```python
def render_quick_replies(suggestions):
    cols = st.columns(len(suggestions))
    for idx, suggestion in enumerate(suggestions):
        with cols[idx]:
            if st.button(suggestion, key=f"quick_{idx}"):
                handle_user_input(suggestion)

# Example usage for room size question:
render_quick_replies(['20 ตร.ม.', '30 ตร.ม.', '40 ตร.ม.'])
```

3. **Input Validation with Feedback:**

```python
def validate_input(value, field_type):
    rules = {
        'room_size': (10, 100, "ตร.ม."),
        'ac_hours': (0, 24, "ชั่วโมง"),
        'fans': (0, 10, "ตัว"),
        # ... more rules
    }
    
    min_val, max_val, unit = rules[field_type]
    
    if not (min_val <= value <= max_val):
        st.error(f"⚠️ กรุณากรอกค่าระหว่าง {min_val}-{max_val} {unit}")
        return False
    
    st.success("✅ ข้อมูลถูกต้อง")
    return True
```

4. **Persistence (Browser LocalStorage):**

```python
import streamlit.components.v1 as components

def save_to_local_storage(key, value):
    components.html(f"""
        <script>
            localStorage.setItem('{key}', JSON.stringify({value}));
        </script>
    """, height=0)

def load_from_local_storage(key):
    # Retrieve chat history on app reload
    pass
```

5. **Export Results:**

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf_report(prediction_data):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Add content
    c.drawString(100, 750, "Roo-Lot Prediction Report")
    c.drawString(100, 730, f"ค่าไฟทำนาย: {prediction_data['amount']} บาท")
    # ... more content
    
    c.save()
    buffer.seek(0)
    
    st.download_button(
        label="📥 ดาวน์โหลดรายงาน PDF",
        data=buffer,
        file_name=f"roolot_report_{timestamp}.pdf",
        mime="application/pdf"
    )
```


**Deliverables:**

- Animated charts
- Input validation
- Data persistence
- Export functionality


## 📦 Final Project Structure

```
roo-lot/
├── app.py                          # Original form-based UI (keep for reference)
├── app_chatbot.py                  # NEW: Chatbot interface (main entry)
├── components/                     # NEW: Reusable UI components
│   ├── __init__.py
│   ├── landing.py                  # Landing page component
│   ├── chat_message.py             # Message bubble component
│   ├── result_card.py              # Result display card
│   ├── sidebar.py                  # Sidebar with history
│   └── animations.py               # Animation utilities
├── conversation/                   # NEW: Conversation logic
│   ├── __init__.py
│   ├── manager.py                  # ConversationManager class
│   ├── questions.py                # Question templates
│   └── validator.py                # Input validation
├── assets/                         # NEW: Static assets
│   ├── styles.css                  # Global styles
│   ├── animations.css              # Animation keyframes
│   └── bot_avatar.png              # Bot profile image
├── utils/                          # NEW: Utility functions
│   ├── __init__.py
│   ├── storage.py                  # LocalStorage wrapper
│   └── pdf_generator.py            # Report generation
├── models/                         # (Existing) ML models
│   └── lasso_model.pkl
├── data/                           # (Existing) Datasets
├── scripts/                        # (Existing) Training scripts
└── requirements.txt                # Updated dependencies
```


## 📝 Updated Dependencies

```txt
# Existing
streamlit==1.28.0
scikit-learn==1.3.0
pandas
numpy
plotly

# NEW for chatbot UI
streamlit-chat==0.1.1           # Chat UI components
streamlit-extras==0.3.0         # Additional components
pillow                          # Image processing
reportlab                       # PDF generation
python-dateutil                 # Timestamp handling
```


## 🎯 Success Metrics

| Metric | Target | Measurement |
| :-- | :-- | :-- |
| Animation smoothness | 60 FPS | Chrome DevTools Performance |
| Page load time | < 2s | Lighthouse |
| Conversation completion rate | > 80% | Analytics |
| User satisfaction | > 4.5/5 | Feedback form |
| Mobile responsiveness | 100% | Responsive design test |

## ⚠️ Challenges \& Solutions

### Challenge 1: Streamlit Rerun Behavior

**Issue:** Streamlit reruns entire script on interaction, causing animation flicker

**Solution:**

- Use `st.session_state` extensively to preserve animation states
- Implement CSS animations (runs in browser, not affected by reruns)
- Add `key` parameters to prevent unnecessary component recreations


### Challenge 2: Limited Animation Control

**Issue:** Streamlit has limited native animation support

**Solutions:**

- Inject custom CSS via `st.markdown(unsafe_allow_html=True)`
- Use `st.components.v1.html()` for complex JavaScript animations
- Leverage Plotly's built-in animation capabilities for charts


### Challenge 3: State Management Complexity

**Issue:** Multi-turn conversation requires careful state tracking

**Solution:**

- Create `ConversationManager` class with clear state machine
- Use immutable data patterns (copy state, don't mutate)
- Implement state snapshots for "undo" functionality


### Challenge 4: Real-time Input Validation

**Issue:** Need to validate without full form submission

**Solution:**

- Use `st.text_input()` with `on_change` callback
- Implement debounced validation (wait 500ms after typing stops)
- Show inline validation messages


## 🚀 Deployment Considerations

### Streamlit Cloud

```toml
# .streamlit/config.toml
[theme]
primaryColor="#3B82F6"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#F3F4F6"
textColor="#111827"
font="sans serif"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true
```


### Performance Optimization

1. **Lazy load components:** Only render visible messages
2. **Cache ML model:** `@st.cache_resource` for model loading
3. **Minimize reruns:** Use targeted `st.rerun()` instead of full page
4. **Compress assets:** Optimize images and CSS

## 📊 Timeline Summary

| Phase | Duration | Deliverables | Risk Level |
| :-- | :-- | :-- | :-- |
| Phase 1: Foundation | 1 week | Conversation engine, ML integration | Low |
| Phase 2: UI Components | 1 week | All styled components | Medium |
| Phase 3: Animations | 1 week | Smooth micro-animations | High |
| Phase 4: Polish | 1 week | Advanced features, testing | Medium |

**Total:** 4 weeks (High Effort)

## 🎬 Next Steps

1. **Create Antigravity Skill file** (`.ag/skills/chatbot-ui.md`)
2. **Initialize new branch:** `feature/chatbot-interface`
3. **Start Phase 1:** Build conversation manager
4. **Iterate with user testing** after each phase