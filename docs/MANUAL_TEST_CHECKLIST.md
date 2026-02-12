# 🧪 Manual Testing Checklist for Roo-Lot

**Goal:** Verify the application's functionality, usability, and stability before deployment.

### 1. Setup & Launch
- [ ] Open terminal in `roo-lot/` directory.
- [ ] Run command: `streamlit run app_chatbot.py`
- [ ] App should open in browser at `http://localhost:8501` (or similar).
- [ ] **Check:** Does the landing page render correctly? (Logo, Headline, "Start" button)

### 2. Happy Path (Full Conversation Flow)
**Objective:** Ensure a user can complete a prediction successfully.

- [ ] Click **"เริ่มวิเคราะห์เลย ➤"** button.
- [ ] **Q1 Room Size:** Enter `30` -> Press Enter.
- [ ] **Q2 AC Hours:** Enter `8` -> Press Enter.
- [ ] **Q3 Fans:** Enter `2` -> Press Enter.
- [ ] **Q4 Lights:** Enter `4` -> Press Enter.
- [ ] **Q5 Computers:** Enter `1` -> Press Enter.
- [ ] **Q6 Other Appliances:** Enter `0` -> Press Enter.
- [ ] **Result Page:**
    - [ ] Check if "ค่าไฟโดยประมาณ" is displayed (e.g., ~1,500 THB).
    - [ ] Check if the gauge chart renders.
    - [ ] Check if the "Cost Breakdown" (donut chart) renders.
    - [ ] Check if the "Save Result" button works (if implemented) or just verify it looks correct.

### 3. Edge Cases & Validation
**Objective:** Ensure the app handles invalid inputs gracefully.

- [ ] **Reset the App:** Refresh the browser or use the sidebar "Reset" button (if available).
- [ ] **Invalid Number:** In "Room Size", try typing `abc` or `hello`.
    - [ ] **Check:** Does the app show an error message like "กรุณากรอกเฉพาะตัวเลขเท่านั้น"?
- [ ] **Out of Range (Min):** In "Room Size", enter `5` (Expect min to be 10 or similar).
    - [ ] **Check:** Does it warn about minimum value?
- [ ] **Out of Range (Max):** In "AC Hours", enter `25`.
    - [ ] **Check:** Does it warn "must be between 0 and 24"?

### 4. UI/UX & Responsiveness
**Objective:** Ensure the app looks good on different screens.

- [ ] **Mobile View:**
    - [ ] Open Developer Tools (F12) -> Toggle Device Toolbar (Ctrl+Shift+M).
    - [ ] Select "iPhone SE" or "Pixel 7".
    - [ ] **Check:** Is the text readable? Do buttons fit on the screen?
    - [ ] **Check:** Does the chat interface scroll correctly?
- [ ] **Dark Mode:**
    - [ ] Ensure the app looks consistent in Dark Mode (since we forced dark theme in CSS).
    - [ ] **Check:** Are input fields visible against the background?

### 5. Deployment Health Check
**Objective:** Verify critical components exist.

- [ ] Check if `models/lasso_model.pkl` exists.
- [ ] Check if `models/preprocessor.pkl` (or scaler) exists.

---
**Status:**
- [ ] 1. Setup & Launch
- [ ] 2. Happy Path
- [ ] 3. Edge Cases
- [ ] 4. UI/UX
- [ ] 5. Health Check

**Notes:**
- If you find any bugs, please log them in `docs/BUGS.md`.
