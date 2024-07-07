from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import PyPDF2
import os
import shutil
import textwrap

base_dir = os.path.dirname(__file__)

class CreateDiary:
    def __init__(self):
        self.diary_page_directory = os.path.join(base_dir, 'data', 'diary_pages').replace('\\', '/')
        self.my_diary_directory = os.path.join(base_dir, 'data', 'my_diary').replace('\\', '/')
        self.my_diary_filename = 'my_diary.pdf'

    def create_pdf(self, filename, content):
        file_path = os.path.join(base_dir, 'data', 'diary_pages', filename).replace('\\', '/')
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter

        # Title
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width // 2, height - 50, "Your 2024 Diary!")

        # Content
        c.setFont("Helvetica", 12)
        y_position = height - 100
        margin = 50
        max_width = width - 2 * margin
        question = True

        for line in content.splitlines():
            if line.strip().endswith("?"):  # Check if the line ends with a question mark
                c.setFont("Helvetica-Bold", 12)  # Set bold font for questions
                question = True
            else:
                c.setFont("Helvetica", 12)  # Set regular font for answers
                if question:  # Add extra space before an answer
                    y_position -= 10
                    question = False

            # Wrap the text
            wrapped_lines = textwrap.wrap(line, width=100)

            for wrapped_line in wrapped_lines:
                c.drawString(margin, y_position, wrapped_line)
                y_position -= 15  # Adjust spacing between lines

            y_position -= 5  # General extra spacing between lines

        c.save()

        if self.is_folder_empty(self.my_diary_directory):
            self.copy_pdf_file(self.diary_page_directory, filename, self.my_diary_directory)
            self.rename_pdf_file(self.my_diary_directory, filename, self.my_diary_filename)
            print(f"The folder '{self.my_diary_directory}' is empty.")
        else:
            my_diary_path = os.path.join(self.my_diary_directory, self.my_diary_filename)
            new_page_path = os.path.join(self.diary_page_directory, filename)
            self.merge_pdfs(my_diary_path, new_page_path, my_diary_path)
            print(f"The folder '{my_diary_path}' is not empty.")
    def merge_pdfs(self,pdf1_path, pdf2_path, output_path):
        pdf_writer = PyPDF2.PdfWriter()

        # Open the first PDF
        pdf1 = PyPDF2.PdfReader(open(pdf1_path, "rb"))

        # Loop through each page and add it to the writer
        for page_num in range(len(pdf1.pages)):
            pdf_writer.add_page(pdf1.pages[page_num])

        # Open the second PDF
        pdf2 = PyPDF2.PdfReader(open(pdf2_path, "rb"))

        # Loop through each page and add it to the writer
        for page_num in range(len(pdf2.pages)):
            pdf_writer.add_page(pdf2.pages[page_num])

        # Write the merged PDF to the output file
        with open(output_path, "wb") as output_file:
            pdf_writer.write(output_file)

    def copy_pdf_file(self,source_directory, filename, target_directory):
        # Ensure the target directory exists
        os.makedirs(target_directory, exist_ok=True)

        # Form the full source and target file paths
        source_path = os.path.join(source_directory, filename)
        target_path = os.path.join(target_directory, filename)

        # Move the file
        shutil.copy(source_path, target_path)
        print(f"Moved '{filename}' from '{source_directory}' to '{target_directory}'")

    def is_folder_empty(self, directory):
        # List the entries in the directory
        entries = os.listdir(directory)

        # Check if the list is empty
        return len(entries) == 0
    def rename_pdf_file(self,directory, old_filename, new_filename):
        # Form the full paths for the old and new file names
        old_path = os.path.join(directory, old_filename)
        new_path = os.path.join(directory, new_filename)

        # Rename the file
        os.rename(old_path, new_path)
        print(f"Renamed '{old_filename}' to '{new_filename}' in '{directory}'")


def is_folder_empty(directory):
    # List the entries in the directory
    entries = os.listdir(directory)

    # Check if the list is empty
    return len(entries) == 0
