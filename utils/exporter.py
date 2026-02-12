"""
Roo-Lot Chatbot - Report Exporter
"""

import io
from fpdf import FPDF
import pandas as pd
from datetime import datetime

class PDFReport(FPDF):
    def header(self):
        # Logo placeholder
        self.set_font('Arial', 'B', 15)
        self.cell(80)
        self.cell(30, 10, 'Roo-Lot AI Report', 0, 0, 'C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf_report(prediction_data: dict) -> bytes:
    """
    Generate PDF report from prediction data
    
    Args:
        prediction_data: Dictionary containing prediction results and inputs
        
    Returns:
        bytes: PDF file content
    """
    pdf = PDFReport()
    pdf.add_page()
    
    # Title
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(0, 10, 'Electricity Bill Prediction', 0, 1, 'C')
    pdf.ln(10)
    
    # Date
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1, 'R')
    pdf.ln(10)
    
    # Prediction Result
    amount = prediction_data.get('amount', 0)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Prediction Result', 0, 1, 'L')
    pdf.set_font('Arial', '', 14)
    pdf.cell(0, 10, f"Estimated Bill: {amount:.2f} THB", 0, 1, 'L')
    pdf.ln(5)
    
    # Inputs Summary
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Input Parameters', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    
    inputs = prediction_data.get('details', {})
    for key, value in inputs.items():
        label = key.replace('_', ' ').title()
        pdf.cell(0, 8, f"{label}: {value}", 0, 1, 'L')
        
    pdf.ln(10)
        
    # Cost Breakdown
    if 'breakdown' in prediction_data:
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Cost Breakdown', 0, 1, 'L')
        pdf.set_font('Arial', '', 12)
        
        breakdown = prediction_data['breakdown']
        pdf.cell(0, 8, f"AC Cost: {breakdown.get('ac_cost', 0):.2f} THB", 0, 1, 'L')
        pdf.cell(0, 8, f"Appliances: {breakdown.get('appliances_cost', 0):.2f} THB", 0, 1, 'L')
        pdf.cell(0, 8, f"Base Fee: {breakdown.get('base_fee', 0):.2f} THB", 0, 1, 'L')

    # Output to buffer
    # FPDF output to string (latin-1) then encode to bytes, 
    # OR use output(dest='S').encode('latin-1') 
    # For newer FPDF2, output() returns bytes directly if dest not set or 'S' might be different.
    # Assuming standard py-fpdf or fpdf2 behavior compatible way:
    
    try:
        return pdf.output(dest='S').encode('latin-1')
    except:
        # Fallback for some versions
        return pdf.output(dest='S').encode('latin-1') 

    # Note: FPDF 1.7.2 output(dest='S') returns string.
