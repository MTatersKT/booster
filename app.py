
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import fitz  # PyMuPDF
from PIL import Image
import io
from datetime import datetime
import numpy as np

st.title("Reimbursement Form - Sports Booster Organization")

amount = st.text_input("Amount")
purpose = st.text_area("Purpose of Reimbursement")
date = st.date_input("Date", value=datetime.today())

st.markdown("### Signature (use touchscreen or mouse)")
canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 0.0)",
    stroke_width=2,
    stroke_color="#000000",
    background_color="#FFFFFF",
    height=150,
    width=400,
    drawing_mode="freedraw",
    key="canvas",
)

receipts = st.file_uploader("Upload Receipts (camera supported)", accept_multiple_files=True, type=["png", "jpg", "jpeg"])

if st.button("Generate PDF"):
    pdf = fitz.open("scan.pdf")
    page = pdf[0]

    page.insert_text((100, 150), f"Amount: {amount}", fontsize=12)
    page.insert_text((100, 170), f"Purpose: {purpose}", fontsize=12)
    page.insert_text((100, 190), f"Date: {date.strftime('%Y-%m-%d')}", fontsize=12)

    if canvas_result.image_data is not None:
        sig_img = Image.fromarray(canvas_result.image_data.astype('uint8'))
        sig_buf = io.BytesIO()
        sig_img.save(sig_buf, format="PNG")
        sig_buf.seek(0)
        rect = fitz.Rect(100, 500, 300, 550)
        page.insert_image(rect, stream=sig_buf.read())

    for receipt in receipts:
        image = Image.open(receipt)
        img_buf = io.BytesIO()
        image.save(img_buf, format='PNG')
        img_buf.seek(0)
        img_pdf = fitz.open(stream=img_buf.read(), filetype="png")
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
