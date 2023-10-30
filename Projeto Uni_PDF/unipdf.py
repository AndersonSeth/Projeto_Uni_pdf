import os
from flask import Flask, request, render_template, redirect, url_for, send_file
from PyPDF2 import PdfReader, PdfMerger

app = Flask(__name__, template_folder='templates')

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("Recebendo requisição POST")
        arquivos_carregados = request.files.getlist('file')

        if arquivos_carregados:
            pdf_merger = PdfMerger()

            for arquivo in arquivos_carregados:
                if arquivo and arquivo.filename.endswith('.pdf'):
                    pdf_merger.append(PdfReader(arquivo))
                    print(f"Arquivo adicionado: {arquivo.filename}")

            output_pdf_path = os.path.join(OUTPUT_FOLDER, 'PDF_unificado.pdf')
            pdf_merger.write(output_pdf_path)

            print(f"Arquivo mesclado criado: PDF_unificado.pdf")
            return redirect(url_for('download', filename='PDF_unificado.pdf'))
        else:
            return render_template('index.html', error_message='Nenhum arquivo foi encontrado.')

    return render_template('index.html')

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(OUTPUT_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
