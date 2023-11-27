from flask import Flask, request, jsonify
import PyPDF2

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

def extract_text_from_pdf(file, password=None):
    # with open(pdf_file_path, 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)

        # Check if the PDF is encrypted
    if pdf_reader.is_encrypted:
            # Try to decrypt the PDF using the provided password
            if password:
                if pdf_reader.decrypt(password) != 1:
                    return None  # Incorrect password
            else:
                return None  # PDF is encrypted, but no password provided

        # Extract text from all pages
    text = ""
    for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()

    return text

@app.route('/extract-text', methods=['POST'])
def extract_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    password = request.form.get('password', '')  # Get the password from the request

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    extracted_text = extract_text_from_pdf(file, password)

    if extracted_text is not None:
        return jsonify({'text': extracted_text})
    else:
        return jsonify({'error': 'Failed to extract text. Incorrect password or encrypted PDF'})


# if __name__ == '__main__':
#     app.run(debug=True)
