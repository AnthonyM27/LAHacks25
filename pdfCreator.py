from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class PDFGenerator:
    def __init__(self, filename="output.pdf", font="Helvetica", font_size=10, margin=40):
        self.filename = filename
        self.font = font
        self.font_size = font_size
        self.margin = margin
        self.width, self.height = letter

    def generate_pdf(self, text):
        # Create a PDF canvas
        c = canvas.Canvas(self.filename, pagesize=letter)
        
        # Set up font
        c.setFont(self.font, self.font_size)
        
        # Define the text object and position
        text_object = c.beginText(self.margin, self.height - self.margin)
        text_object.setFont(self.font, self.font_size)
        text_object.setTextOrigin(self.margin, self.height - self.margin)
        
        # Wrap and add the text to the PDF
        text_object.textLines(text)
        c.drawText(text_object)
        
        # Save the PDF file
        c.save()

