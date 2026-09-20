from pypdf import PdfReader


def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF resume.
    """

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text.strip()


if __name__ == "__main__":

    file_path = "uploads/sample_resume.pdf"

    try:

        text = extract_text_from_pdf(file_path)

        print("\n===================================")
        print("       EXTRACTED RESUME TEXT")
        print("===================================\n")

        print(text)

    except Exception as e:

        print("Error:", e)