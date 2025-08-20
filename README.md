## คำแนะนำการใช้งานภาษาไทย (Thai Usage Guide)

### การติดตั้งและเริ่มต้นใช้งาน

#### 1. เปิดใช้งาน Virtual Environment
```bash
# ใน PowerShell
.\.venv\Scripts\Activate.ps1

# ใน Command Prompt
.venv\Scripts\activate.bat
```

#### 2. ติดตั้ง dependencies
```bash
pip install -r requirements.txt
```

#### 3. ตั้งค่า API Key
```bash
# Windows PowerShell
$env:OPENROUTER_API_KEY="api_key_ของคุณ"

# Windows Command Prompt
set OPENROUTER_API_KEY=api_key_ของคุณ
```

#### 4. รันโปรแกรม
```bash
# วิธีที่ใช้: รันด้วย Python
python nlp_chatbot.py
```

### คำสั่งพื้นฐาน
- `/help` - แสดงคำสั่งทั้งหมด
- `/clear` - ล้างประวัติการสนทนา
- `/save [ชื่อไฟล์]` - บันทึกการสนทนา
- `/load <ชื่อไฟล์>` - โหลดการสนทนา
- `/quit` - ออกจากโปรแกรม

### ตัวอย่างคำถาม NLP ภาษาไทย
- "Sentiment analysis คืออะไร?"
- "อธิบายเรื่อง Named Entity Recognition"
- "BERT กับ GPT ต่างกันอย่างไร?"
- "วิธีทำ text classification"
- "ช่วยอธิบาย machine translation"

### การแก้ไขปัญหาที่พบบ่อย

#### ไม่สามารถเปิด Virtual Environment ได้
```powershell
# ถ้าใช้ PowerShell และมีปัญหา execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### API Key ไม่ทำงาน
- ตรวจสอบ API key ที่ OpenRouter
- ตรวจสอบว่าตั้งค่า environment variable ถูกต้อง

#### วิธีออกจาก Virtual Environment
```bash
deactivate
```

## License

This project is open source and available under the MIT License.
