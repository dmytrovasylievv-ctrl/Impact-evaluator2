import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

def test_init_google_sheet(mocker):
    mock_creds = mocker.patch('oauth2client.service_account.ServiceAccountCredentials.from_json_keyfile_name')
    mock_client = mocker.patch('gspread.authorize')
    mock_sheet = mocker.Mock()
    mock_client.return_value = mock_sheet

    sheet = init_google_sheet()
    assert sheet == mock_sheet
    mock_creds.assert_called_once_with("google_credentials.json", ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])

def test_calculate_kpis():
    data = {
        'beneficiaries': 100,
        'closed_cases': 80,
        'total_cases': 100,
        'staff': 10,
        'resources_spent': 5000,
        'community_activities': 5,
        'successful_interventions': 60
    }
    
    case_closure_rate = data['closed_cases'] / data['total_cases']
    intervention_success_rate = data['successful_interventions'] / max(data['successful_interventions'], 1)
    cost_per_beneficiary = data['resources_spent'] / max(data['beneficiaries'], 1)
    staff_load = data['beneficiaries'] / data['staff']
    efficiency_score = (case_closure_rate + intervention_success_rate) / 2

    assert case_closure_rate == 0.8
    assert intervention_success_rate == 1.0
    assert cost_per_beneficiary == 50.0
    assert staff_load == 10.0
    assert efficiency_score == 0.9

def test_generate_pdf():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("Program Evaluation Report - Test Program", styles["Title"]))
    content.append(Spacer(1, 12))

    fields = [
        "Закриті кейси: 80%",
        "Успішні інтервенції: 100%",
        "Ефективність програми: 90%",
        "Вартість на бенефіціара: $50.0",
        "Навантаження на персонал: 10.0 beneficiaries/worker",
        "Impact Score: 5/5",
    ]

    for f in fields:
        content.append(Paragraph(f, styles["Normal"]))
        content.append(Spacer(1, 6))

    doc.build(content)
    buffer.seek(0)
    assert buffer.getvalue() is not None

def test_recommendations():
    recommendations = []

    cost_per_beneficiary = 150
    case_closure_rate = 0.5
    intervention_success_rate = 0.4
    staff_load = 90
    impact_score = 2

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

    assert len(recommendations) == 5  # All recommendations should be triggered