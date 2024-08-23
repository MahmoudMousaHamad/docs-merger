import io
import os
import shutil
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from docx2pdf import convert
from natsort import natsorted
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Calibri font
pdfmetrics.registerFont(TTFont('Calibri', './fonts/calibri.ttf'))

def merge_pdfs(pdfs, output):
    pdf_writer = PdfWriter()

    for pdf in pdfs:
        try:
            pdf_reader = PdfReader(pdf)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pdf_writer.add_page(page)
        except:
            print(f"Error reading {pdf}, skipping.")

    with open(output, 'wb') as out:
        pdf_writer.write(out)

def add_page_numbers(input_pdf, output_pdf):
    with open(input_pdf, "rb") as f:
        existing_pdf = PdfReader(f)
        output = PdfWriter()
        num_pages = len(existing_pdf.pages)

        for i in range(num_pages):
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            can.setFont("Calibri", 12)
            can.drawString(500, 10, f"{i + 1}")
            can.save()

            packet.seek(0)
            new_pdf = PdfReader(packet)
            page = existing_pdf.pages[i]
            page.merge_page(new_pdf.pages[0])
            output.add_page(page)

        with open(output_pdf, "wb") as outputStream:
            output.write(outputStream)

def docx_to_pdf(docx_path):
    pdf_path = docx_path.replace('.docx', '.pdf')
    convert(docx_path, pdf_path)
    return pdf_path

def main(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.pdf') or f.endswith('.docx')]
    sorted_files = natsorted(files)

    pdfs = []
    generated_pdfs = []

    for file in sorted_files:
        file_path = os.path.join(directory, file)
        if file.endswith('.docx'):
            pdf_path = docx_to_pdf(file_path)
            pdfs.append(pdf_path)
            generated_pdfs.append(pdf_path)
        elif file.endswith('.pdf'):
            pdfs.append(file_path)

    # Create result folder
    result_dir = os.path.join(directory, "result")
    os.makedirs(result_dir, exist_ok=True)

    # Merged PDF file path
    merged_pdf_name = f"merged_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    merged_pdf_path = os.path.join(result_dir, merged_pdf_name)
    
    # Final PDF file path with page numbers
    final_pdf_name = f"final_merged_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    final_pdf_path = os.path.join(result_dir, final_pdf_name)

    merge_pdfs(pdfs, merged_pdf_path)
    add_page_numbers(merged_pdf_path, final_pdf_path)

    print(f"Merged PDF with page numbers saved as {final_pdf_path}")

    # Clean up intermediate files: Only remove generated PDFs and the merged intermediate file
    for pdf in generated_pdfs:
        if os.path.exists(pdf):
            os.remove(pdf)
    if os.path.exists(merged_pdf_path):
        os.remove(merged_pdf_path)

if __name__ == "__main__":
    directories = ["./letters"]
    for directory in directories: 
        main(directory)
