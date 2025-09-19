import streamlit as st
import csv
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime

st.title("Psychological Screening App")

# -----------------------
# الأسئلة مترجمة للعربي
# -----------------------
bai_questions = [
    "1. تنميل أو وخز",
    "2. الشعور بالحرارة",
    "3. ارتجاف في الساقين",
    "4. عدم القدرة على الاسترخاء",
    "5. الخوف من حدوث أسوأ الأشياء",
    "6. دوخة أو دوار أو فقدان التوازن",
    "7. خفقان أو زيادة ضربات القلب",
    "8. عدم الثبات أو التمايل",
    "9. خوف من فقدان السيطرة",
    "10. رعشة في اليدين",
    "11. ارتجاف عام في الجسم",
    "12. خوف من الموت",
    "13. العصبية أو التوتر",
    "14. الشعور بالاختناق",
    "15. ارتعاش في الجسم",
    "16. الشعور بالخوف",
    "17. اضطراب أو انزعاج في المعدة",
    "18. الشعور بالإغماء أو فقدان الوعي",
    "19. احمرار الوجه",
    "20. التعرق (غير الناتج عن الحرارة)",
    "21. ضيق في الصدر"
]

phq9_questions = [
    "1. فقدان الاهتمام أو المتعة في الأنشطة اليومية",
    "2. الشعور بالحزن أو الاكتئاب أو اليأس",
    "3. صعوبة النوم أو النوم المفرط",
    "4. الشعور بالتعب أو انخفاض الطاقة",
    "5. فقدان الشهية أو الإفراط في الأكل",
    "6. الشعور بسوء تقدير الذات أو الشعور بالفشل",
    "7. صعوبة التركيز على الأمور اليومية",
    "8. البطء الحركي أو التهيج",
    "9. أفكار متكررة عن الموت أو إيذاء النفس"
]

isi_questions = [
    "1. صعوبة في النوم عند الذهاب إلى السرير",
    "2. صعوبة في البقاء نائمًا خلال الليل",
    "3. الاستيقاظ مبكرًا جدًا وعدم القدرة على العودة للنوم",
    "4. شعور بالرضا عن نوعية النوم",
    "5. مدى تأثير صعوبات النوم على الحياة اليومية",
    "6. مدى قلقك أو إزعاجك بسبب صعوبات النوم",
    "7. مدى تأثير مشاكل النوم على رفاهيتك العامة"
]

# -----------------------
# درجات كل اختبار
# -----------------------
bai_choices = {"0":0, "1":1, "2":2, "3":3}
phq9_choices = {"0":0, "1":1, "2":2, "3":3}
isi_choices = {"0":0, "1":1, "2":2, "3":3, "4":4}

# -----------------------
# مستويات النتائج
# -----------------------
def bai_level(score):
    if score <= 7: return "Minimal Anxiety"
    elif score <= 15: return "Mild Anxiety"
    elif score <= 25: return "Moderate Anxiety"
    else: return "Severe Anxiety"

def phq9_level(score):
    if score <= 4: 
        return "Minimal Depression"
    elif score <= 9: 
        return "Mild Depression"
    elif score <= 14: 
        return "Moderate Depression"
    elif score <= 19: 
        return "Moderately Severe Depression"
    else: 
        return "Severe Depression"

def isi_level(score):
    if score <= 7: return "No clinically significant insomnia"
    elif score <= 14: return "Subthreshold insomnia"
    elif score <= 21: return "Moderate insomnia"
    else: return "Severe insomnia"

# -----------------------
# إدخال بيانات المريض
# -----------------------
patient_name = st.text_input("Patient Name")
age = st.text_input("Age")
tumor_type = st.text_input("Tumor Type")

st.write("### أجب عن الأسئلة بالنسبة للأسبوعين الأخيرين")

# -----------------------
# دالة لجمع الإجابات مع عرض الخيارات
# -----------------------
def ask_questions(questions, choices, scale_text):
    total = 0
    answers = {}
    for q in questions:
        ans = st.radio(f"{q}", options=list(choices.keys()), format_func=lambda x: f"{x} = {scale_text[x]}")
        total += choices[ans]
        answers[q] = ans
    return total, answers

bai_scale_text = {"0":"أبداً", "1":"قليلاً", "2":"نصف الأيام", "3":"تقريبًا كل يوم"}
phq9_scale_text = {"0":"أبداً", "1":"عدة أيام", "2":"أكثر من نصف الأيام", "3":"تقريبًا كل يوم"}
isi_scale_text = {"0":"لا أبدًا", "1":"قليل", "2":"متوسط", "3":"كثير", "4":"شديد جدًا"}

if st.button("Submit"):
    bai_score, _ = ask_questions(bai_questions, bai_choices, bai_scale_text)
    phq9_score, _ = ask_questions(phq9_questions, phq9_choices, phq9_scale_text)
    isi_score, _ = ask_questions(isi_questions, isi_choices, isi_scale_text)

    bai_result = bai_level(bai_score)
    phq9_result = phq9_level(phq9_score)
    isi_result = isi_level(isi_score)

    # ملاحظات
    bai_notes_dict = {
        "Minimal Anxiety": "Symptoms are minimal, regular monitoring recommended.",
        "Mild Anxiety": "Mild anxiety detected, consider relaxation techniques.",
        "Moderate Anxiety": "Moderate anxiety, follow-up advised.",
        "Severe Anxiety": "Severe anxiety, urgent consultation recommended."
    }
    phq9_notes_dict = {
        "Minimal Depression": "Minimal depressive symptoms, monitor.",
        "Mild Depression": "Mild depressive symptoms, consider lifestyle changes.",
        "Moderate Depression": "Moderate depressive symptoms, follow-up suggested.",
        "Moderately Severe Depression": "Moderately severe depressive symptoms, prompt professional evaluation recommended.",
        "Severe Depression": "Severe depressive symptoms, immediate professional evaluation recommended."
    }
    isi_notes_dict = {
        "No clinically significant insomnia": "No clinically significant insomnia.",
        "Subthreshold insomnia": "Mild sleep difficulties, monitor sleep hygiene.",
        "Moderate insomnia": "Moderate insomnia, consider intervention.",
        "Severe insomnia": "Severe insomnia, professional evaluation recommended."
    }

    st.write("## Results")
    st.write(f"BAI Score: {bai_score}, Level: {bai_result}")
    st.write(f"PHQ-9 Score: {phq9_score}, Level: {phq9_result}")
    st.write(f"ISI Score: {isi_score}, Level: {isi_result}")

    st.write("### Notes")
    st.write(f"- BAI: {bai_notes_dict[bai_result]}")
    st.write(f"- PHQ-9: {phq9_notes_dict[phq9_result]}")
    st.write(f"- ISI: {isi_notes_dict[isi_result]}")

    # حفظ CSV
    with open("patients_data.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([patient_name, age, tumor_type,
                         bai_score, bai_result,
                         phq9_score, phq9_result,
                         isi_score, isi_result,
                         datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

    # إنشاء PDF
    pdf_filename = f"{patient_name}_report.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Patient Report – Psychological Screening", styles["Title"]))
    story.append(Spacer(1,12))
    story.append(Paragraph(f"Patient Name: {patient_name}", styles["Normal"]))
    story.append(Paragraph(f"Age: {age}", styles["Normal"]))
    story.append(Paragraph(f"Tumor Type: {tumor_type}", styles["Normal"]))
    story.append(Spacer(1,12))

    data = [
        ["Test Name", "Score", "Level"],
        ["Beck Anxiety Inventory (BAI)", bai_score, bai_result],
        ["Patient Health Questionnaire-9 (PHQ-9)", phq9_score, phq9_result],
        ["Insomnia Severity Index (ISI)", isi_score, isi_result]
    ]

    table = Table(data, hAlign='LEFT', colWidths=[200,100,200])
    table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0), colors.lightblue),
        ('TEXTCOLOR',(0,0),(-1,0), colors.white),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('GRID',(0,0),(-1,-1),1,colors.black)
    ]))
    story.append(table)
    story.append(Spacer(1,12))

    story.append(Paragraph("Notes per Test:", styles["Heading2"]))
    story.append(Paragraph(f"- BAI: {bai_notes_dict[bai_result]}", styles["Normal"]))
    story.append(Paragraph(f"- PHQ-9: {phq9_notes_dict[phq9_result]}", styles["Normal"]))
    story.append(Paragraph(f"- ISI: {isi_notes_dict[isi_result]}", styles["Normal"]))
    story.append(Spacer(1,12))

    story.append(Paragraph("General Notes:", styles["Heading2"]))
    general_notes = [
        "This is a preliminary report and does not represent a final medical diagnosis.",
        "Consultation with a mental health professional is advised for a comprehensive assessment."
    ]
    for note in general_notes:
        story.append(Paragraph(f"- {note}", styles["Normal"]))

    story.append(Spacer(1,12))
    story.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d')}", styles["Normal"]))

    doc.build(story)

    st.success(f"Report PDF and CSV generated: {pdf_filename} & patients_data.csv")
