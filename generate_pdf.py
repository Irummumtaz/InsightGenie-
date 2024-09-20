from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)  # Bold font for header
        self.cell(0, 10, 'Data Analysis Report', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)  # Italic font for footer
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf_report(query_history, output_filename, plots_dir):
    pdf = PDF()
    pdf.add_page()
    
    for query, response, img_path in query_history:
        pdf.set_font("Arial", "", 12)  # Regular Arial font, size 12
        pdf.multi_cell(0, 10, f"Query: {query}")
        pdf.set_font("Arial", "", 12)  # Regular Arial font, size 12 for response
        pdf.multi_cell(0, 10, f"Response: {response}")
        pdf.ln(10)

        if img_path:
            pdf.image(img_path, x=10, w=180)  # Include image if applicable
            pdf.ln(10)

    pdf.output(output_filename)
