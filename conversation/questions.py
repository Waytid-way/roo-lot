"""
Roo-Lot Chatbot - Question Configuration

IMPORTANT: Features must match the model documented in Report-ML-Project-Roo-Lot.md Chapter 3.1

Model Features (DO NOT CHANGE without retraining):
- household_size: int (1-10)
- has_ac: bool (0 or 1)  ⚠️ BOOLEAN, not hours!
- month: int (1-12)

Model Output:
- energy_consumption_kwh: float (total only, no breakdown)

Last Updated: 2026-02-13 21:30 ICT
Version: 2.0.0 - Python 3.11 Compatible
"""

QUESTIONS = [
    {
        "id": "household_size",
        "question": "สวัสดีครับ! เพื่อช่วยประเมินค่าไฟ 💡 บ้านของคุณมีสมาชิกกี่คนครับ?",
        "field": "household_size",
        "type": "number",
        "min": 1,
        "max": 10,
        "unit": "คน",
        "placeholder": "เช่น 3",
        "quick_replies": ["1", "2", "3", "4", "5"],
        "help_text": "Model เทรนด้วยข้อมูล 1-6 คน (>6 อาจคลาดเคลื่อน)"
    },
    {
        "id": "has_ac",
        "question": "❄️ บ้านของคุณมีเครื่องปรับอากาศไหมครับ?",
        "field": "has_ac",
        "type": "choice",
        "options": ["มี", "ไม่มี"],
        "quick_replies": ["มี", "ไม่มี"],
        "help_text": "Model ประมาณการแบบทั่วไป (ไม่ได้ใช้ชั่วโมงแม่นยำ)"
    },
    {
        "id": "month",
        "question": "คำถามสุดท้าย! คุณอยากทราบค่าไฟของเดือนไหนครับ? (เลือกเดือนเพื่อดูผลตามฤดูกาล 📅)",
        "field": "month",
        "type": "month_selector", 
        "quick_replies": ["มกราคม", "เมษายน", "กรกฎาคม", "ตุลาคม"]  # Represents different seasons
    }
]
