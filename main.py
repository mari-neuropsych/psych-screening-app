import streamlit as st
import csv
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
from io import BytesIO

st.title("Patient Psychological Screening")

# -----------------------
# البيانات الأساسية
# -----------------------
patient_name = st.text_input("Patient Name")
age = st.text_input("Age")
tumor_type = st.text_input("Tumor Type")

# -----------------------
# الأسئلة
# -----------------------
bai_questions = ["1. تنميل أو وخز", "2. الشعور بالحرارة", "..."]  # أكمل باقي الأسئلة
phq9_questions = ["1. فقدان الاهتمام أو المتعة في الأنشطة اليومية", "..."]
isi_questions = ["1. صعوبة في النوم عند الذهاب إلى السرير", "..."]

bai_choices = {"0":0, "1":1, "2":2, "3":3}
phq9_choices = {"0":0, "1":1, "2":2, "3":3}
isi_choices = {"0":0, "1":1, "2":2, "3":3, "4":4}

# -----------------------
# session_state لتخزين الإجابات
# -----------------------
if "bai_answers" not in st.session_state:
    st.session_state.bai_answers = [""] * len(bai_questions)
if "phq9_answers" not in st.session_state:
    st.session_state.phq9_answers = [""] * len(phq9_questions)
if "isi_answers" not in st.session_state:
    st.session_state.isi_answers = [""] * len(isi_questions)

# -----------------------
# عرض الأسئلة
# -----------------------
st.subheader("BAI Questions")
for i, q in enumerate(bai_questions):
    st.session_state.bai_answers[i] = st.text_input(q, st.session_state.bai_answers[i], key=f"bai_{i}")

st.subheader("PHQ-9 Questions")
for i, q in enumerate(phq9_questions):
    st.session_state.phq9_answers[i] = st.text_input(q, st.session_state.phq9_answers[i], key=f"phq9_{i}")

st.subheader("ISI Questions")
for i, q in enumerate(isi_questions):
    st.session_state.isi_answers[i] = st.text_input(q, st.session_state.isi_answers[i], key=f"isi_{i}")

# -----------------------
# Submit
# -----------------------
if st.button("Submit"):
    try:
        bai_score = sum([bai_choices[a] for a in st.session_state.bai_answers])
        phq9_score = sum([phq9_choices[a] for a in st.session_state.phq9_answers])
        isi_score = sum([isi_choices[a] for a in st.session_state.isi_answers])
    except KeyError:
        st.error("Please enter valid numbers for all questions.")
        st.stop()

    # تحديد المستويات (نفس الكود الأصلي)
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

    bai_result = bai_level(bai_score)
    phq9_result = phq9_level(phq9_score)
    isi_result = isi_level(isi_score)

    # حفظ CSV (زي الكود الأصلي)
    with open("patients_data.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([patient_name, age, tumor_type,
                         bai_score, bai_result,
                         phq9_score, phq9_result,
                         isi_score, isi_result,
                         datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    st.success("Results saved successfully!")

    # إنشاء PDF (زي الكود الأصلي تمامًا)
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("Patient Report – Psychological Screening", styles["Title"]))
    story.append(Spacer(1,12))
    story.append(Paragraph(f"Patient Name: {patient_name}", styles["Normal"]))
    story.append(Paragraph(f"Age: {age}", styles["Normal"]))
    story.append(Paragraph(f"Tumor Type: {tumor_type}", styles["Normal"]))
    # ... أكمل باقي الكود زي ما هو
    doc.build(story)
    buffer.seek(0)

    st.download_button(
        label="Download PDF Report",
        data=buffer,
        file_name=f"{patient_name}_report.pdf",
        mime="application/pdf"
    )
