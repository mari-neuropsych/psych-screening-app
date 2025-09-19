import streamlit as st
import csv
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
import io

st.title("Psychological Screening Tool")

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
    if score <= 4: return "Minimal Depression"
    elif score <= 9: return "Mild Depression"
    elif score <= 14: return "Moderate Depression"
    else: return "Severe Depression"

def isi_level(score):
    if score <= 7: return "No clinically significant insomnia"
    elif score <= 14: return "Subthreshold insomnia"
    elif score <= 21: return "Moderate insomnia"
    else: return "Severe insomnia"

# -----------------------
# ملاحظات لكل اختبار
# -----------------------
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
    "Severe Depression": "Severe depressive symptoms, immediate professional evaluation recommended."
}

isi_notes_dict = {
    "No clinically significant insomnia": "No clinically significant insomnia.",
    "Subthreshold insomnia": "Mild sleep difficulties, monitor sleep hygiene.",
    "Moderate insomnia": "Moderate insomnia, consider intervention.",
    "Severe insomnia": "Severe insomnia, professional evaluation recommended."
}

# -----------------------
# إدخال بيانات المريض
# -----------------------
patient_name = st.text_input("Patient Name")
age = st.text_input("Age")
tumor_type = st.text_input("Tumor Type")

st.write("### أجب عن الأسئلة بالنسبة للأسبوعين الأخيرين")

# -----------------------
# عرض كل الأسئلة مرة واحدة
# -----------------------
bai_answers = [st.radio(f"{q} (BAI)", list(bai_choices.keys()), key=f"bai_{i}") for i,q in enumerate(bai_questions)]
phq9_answers = [st.radio(f"{q} (PHQ-9)", list(phq9_choices.keys()), key=f"phq9_{i}") for i,q in enumerate(phq9_questions)]
isi_answers = [st.radio(f"{q} (ISI)", list(isi_choices.keys()), key=f"isi_{i}") for i,q in enumerate(isi_questions)]

# -----------------------
# زر لحساب النتائج
# -----------------------
if st.button("احسب النتائج"):
    bai_score = sum([bai_choices[a] for a in bai_answers])
    phq9_score = sum([phq9_choices[a] for a in phq9_answers])
    isi_score = sum([isi_choices[a] for a in isi_answers])

    bai_result = bai_level(bai_score)
    phq9_result = phq9_level(phq9_score)
    isi_result = isi_level(isi_score)

    st.write(f"**BAI Score:** {bai_score}, Level: {bai_result}")
    st.write(f"**PHQ-9 Score:** {phq9_score}, Level: {phq9_result}")
    st.write(f"**ISI Score:** {isi_score}, Level: {isi_result}")

    # -----------------------
    # حفظ CSV
    # -----------------------
    with open("patients_data.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([patient_name, age, tumor_type,
                         bai_score, bai_result,
                         phq9_score, phq9_result,
                         isi_score, isi_result,
                         datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

    st.success("تم حفظ البيانات في CSV!")

    # -----------------------
    # إنشاء PDF
    # -----------------------
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
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
    story.append(Paragraph(f"- BAI (Anxiety): {bai_notes_dict[bai_result]}", styles["Normal"]))
    story.append(Paragraph(f"- PHQ-9 (Depression): {phq9_notes_dict[phq9_result]}", styles["Normal"]))
    story.append(Paragraph(f"- ISI (Insomnia): {isi_notes_dict[isi_result]}", styles["Normal"]))
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
    buffer.seek(0)

    st.download_button("Download PDF Report", buffer, file_name=f"{patient_name}_report.pdf")
    st.download_button("Download CSV Data", "patients_data.csv")
