import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

# ----------------------------------------
# 1. Налаштування сторінки
# ----------------------------------------
st.set_page_config(
    page_title="Program Evaluation Dashboard",
    page_icon="✅",
    layout="wide"
)

st.title("📊 Система оцінки програм (MEAL/Protection/Legal Aid)")

# ----------------------------------------
# 2. Інтеграція з Google Sheets
# ----------------------------------------

def init_google_sheet():
    """
    Повертає об'єкт робочої таблиці, якщо інтеграція налаштована.
    Якщо ні – повертає None.
    """
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets",
                 "https://www.googleapis.com/auth/drive"]

        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "google_credentials.json",
            scope
        )

        client = gspread.authorize(creds)
        sheet = client.open("ProgramEvaluationDB").sheet1
        return sheet

    except Exception as e:
        st.warning("⚠️ Google Sheets не підключено. Створіть файл google_credentials.json та таблицю ProgramEvaluationDB.")
        return None


sheet = init_google_sheet()


# ----------------------------------------
# 3. Ввід даних
# ----------------------------------------
st.header("🗂️ Введення даних програми")

col1, col2 = st.columns(2)

with col1:
    beneficiaries = st.number_input("Скільки бенефіціарів охоплено?", min_value=0)
    closed_cases = st.number_input("Скільки кейсів успішно закрито?", min_value=0)
    total_cases = st.number_input("Скільки кейсів відкрито загалом?", min_value=1)
    staff = st.number_input("Скільки співробітників працювало?", min_value=1)

with col2:
    resources_spent = st.number_input("Скільки коштів витрачено (USD)?", min_value=0.0)
    community_activities = st.number_input("Кількість community-based заходів", min_value=0)
    successful_interventions = st.number_input("Скільки інтервенцій успішно завершено?", min_value=0)
    program_name = st.text_input("Назва програми")


# ----------------------------------------
# 4. Розрахунок KPI
# ----------------------------------------
if st.button("✅ Розрахувати оцінку"):
    # захист від ділення на нуль
    if total_cases == 0:
        total_cases = 1

    if staff == 0:
        staff = 1

    case_closure_rate = closed_cases / total_cases  # 0-1
    intervention_success_rate = successful_interventions / max(successful_interventions, 1)
    cost_per_beneficiary = resources_spent / max(beneficiaries, 1)
    staff_load = beneficiaries / staff
    efficiency_score = (case_closure_rate + intervention_success_rate) / 2

    # робимо адекватні відсотки
    case_closure_pct = round(case_closure_rate * 100, 2)
    intervention_pct = round(intervention_success_rate * 100, 2)
    efficiency_pct = round(efficiency_score * 100, 2)

    # impact score – 1–5
    impact_score = round(
        (beneficiaries / 50) +
        (community_activities / 10) +
        (successful_interventions / 10),
        2
    )
    impact_score = min(max(impact_score, 1), 5)

    # ----------------------------------------
    # 5. Відображення KPI
    # ----------------------------------------
    st.header("📈 Результати оцінки")

    colA, colB, colC = st.columns(3)
    colA.metric("✅ Закриті кейси (%)", f"{case_closure_pct}%")
    colB.metric("💡 Успіх інтервенцій (%)", f"{intervention_pct}%")
    colC.metric("📊 Ефективність програми", f"{efficiency_pct}%")

    colD, colE = st.columns(2)
    colD.metric("💰 Вартість на бенефіціара", f"${round(cost_per_beneficiary, 2)}")
    colE.metric("⚖️ Навантаження на персонал", f"{round(staff_load, 2)} beneficiaries/worker")

    st.metric("🌟 Impact Score (1–5)", impact_score)

    # ----------------------------------------
    # 6. Графік
    # ----------------------------------------
    st.subheader("📉 Візуалізація ефективності")

    fig, ax = plt.subplots()
    ax.bar(
        ["Закриті кейси", "Успішні інтервенції", "Ефективність"],
        [case_closure_pct, intervention_pct, efficiency_pct]
    )
    ax.set_ylabel("Відсоток (%)")
    st.pyplot(fig)


    # ----------------------------------------
    # 7. Summary
    # ----------------------------------------
    st.subheader("📝 Аналітичний висновок")

    summary = f"""
    Загальна оцінка програми **"{program_name}"** демонструє наступний стан:

    - Рівень закриття кейсів становить **{case_closure_pct}%**. 
      Це свідчить про {'високу' if case_closure_pct > 70 else 'середню' if case_closure_pct > 40 else 'низьку'} ефективність роботи кейс-менеджменту.

    - Успішність інтервенцій складає **{intervention_pct}%**, що {'вказує на стабільні результати' if intervention_pct > 60 else 'вимагає покращення процесів координації та ескалації'}.

    - Загальна ефективність програми оцінюється на рівні **{efficiency_pct}%** – 
      це інтегрований індикатор, який відображає баланс результатів та підходів.

    - Impact Score дорівнює **{impact_score}** за шкалою 1–5. 
      Це показник загального впливу, який враховує охоплення, активність community-based механізмів та якість інтервенцій.

    Рекомендації:
    """

    st.write(summary)

    # ----------------------------------------
    # 8. Автоматичні рекомендації
    # ----------------------------------------
    recommendations = []

    if cost_per_beneficiary > 100:
        recommendations.append("💸 Оптимізуйте витрати та логістику.")
    if case_closure_rate < 0.6:
        recommendations.append("🔧 Перевірте SOP та прискорте процесінг кейсів.")
    if intervention_success_rate < 0.6:
        recommendations.append("📉 Покращіть якість координації інтервенцій.")
    if staff_load > 80:
        recommendations.append("👥 Збільшити персонал або автоматизувати рутинні процеси.")
    if impact_score < 3:
        recommendations.append("🚨 Розширити охоплення або підсилити community-based activities.")

    if not recommendations:
        recommendations.append("✅ Програма демонструє стабільні результати. Можна масштабувати.")

    for rec in recommendations:
        st.write(rec)

    # ----------------------------------------
    # 9. Збереження в Google Sheets
    # ----------------------------------------
    if sheet:
        sheet.append_row([
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            program_name,
            beneficiaries,
            closed_cases,
            total_cases,
            staff,
            resources_spent,
            community_activities,
            successful_interventions,
            case_closure_pct,
            intervention_pct,
            efficiency_pct,
            cost_per_beneficiary,
            staff_load,
            impact_score
        ])
        st.success("✅ Дані збережено у Google Sheets.")

    # ----------------------------------------
    # 10. Генерація PDF
    # ----------------------------------------
    st.subheader("📄 Експорт у PDF")

    def generate_pdf():
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        content = []

        content.append(Paragraph(f"Program Evaluation Report - {program_name}", styles["Title"]))
        content.append(Spacer(1, 12))

        fields = [
            f"Закриті кейси: {case_closure_pct}%",
            f"Успішні інтервенції: {intervention_pct}%",
            f"Ефективність програми: {efficiency_pct}%",
            f"Вартість на бенефіціара: ${round(cost_per_beneficiary, 2)}",
            f"Навантаження на персонал: {round(staff_load, 2)} beneficiaries/worker",
            f"Impact Score: {impact_score}/5",
        ]

        for f in fields:
            content.append(Paragraph(f, styles["Normal"]))
            content.append(Spacer(1, 6))

        content.append(Paragraph("Рекомендації:", styles["Heading2"]))
        for rec in recommendations:
            content.append(Paragraph(rec, styles["Normal"]))
            content.append(Spacer(1, 6))

        doc.build(content)
        buffer.seek(0)
        return buffer

    pdf_buffer = generate_pdf()
    st.download_button(
        label="⬇️ Завантажити PDF",
        data=pdf_buffer,
        file_name="report.pdf",
        mime="application/pdf"
    )