import fitz

def sign_pdf(input_path, output_path):
    doc = fitz.open(input_path)
    page = doc[0]

    page.insert_text(
        (50, 50),
        "Signed ✔",
        fontsize=14,
        color=(0, 0, 1)
    )

    doc.save(output_path)
