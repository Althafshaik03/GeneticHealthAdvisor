from fpdf import FPDF
import datetime

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Genetic Health Advisor Report", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", align="C")

    def add_section(self, title, content):
        self.set_font("Arial", "B", 12)
        self.multi_cell(0, 10, f"{title}", border="B")
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 8, content)
        self.ln(5)

def generate_disease_pdf(title, disease_info: str) -> bytes:
    pdf = PDFReport()
    pdf.add_page()
    pdf.add_section("Section: Disease Match", title)
    pdf.add_section("Details", disease_info)
    return pdf.output(dest="S").encode("latin1")
