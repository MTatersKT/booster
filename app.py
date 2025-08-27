
import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
from datetime import datetime

st.title("Reimbursement Form - Sports Booster Organization")

amount = st.text_input("Amount")
purpose = st.text_area("Purpose of Reimbursement")
date = st.date_input("Date", value=datetime.today())
signature = st.text_input("Signature")
receipts = st.file_uploader("Upload Receipts", accept_multiple_files=True, type=["png", "jpg", "jpeg"])

if st.button("Generate PDF"):
    pdf = fitz.open()
    form_page = pdf.new_page()

    form_text = f"""
    Reimbursement Form - Nonprofit Sports Booster Organization

    Amount: {amount}
    Purpose: {purpose}
    Date: {date.strftime('%Y-%m-%d')}
    Signature: {signature}

    Attached Receipts:
    """
    form_page.insert_text((72, 72), form_text, fontsize=12)

    for receipt in receipts:
        image = Image.open(receipt)
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        img_pdf = fitz.open(stream=img_byte_arr, filetype="png")
        pdf.insert_pdf(img_pdf)
        img_pdf.close()

    pdf_bytes = pdf.write()
    pdf.close()

    st.download_button(
        label="Download Reimbursement PDF",
        data=pdf_bytes,
        file_name="reimbursement_form.pdf",
        mime="application/pdf"
    )
