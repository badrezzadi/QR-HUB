from flask import Flask, render_template, request, send_file, url_for
import qrcode
import os
import time
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['QR_FOLDER'] = 'static/qr_codes'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['QR_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_path = None
    if request.method == 'POST':
        # أولاً نتحقق واش عندنا data نصية
        data = request.form.get('data')
        file = request.files.get('image')
        
        if data:
            # QR من نص
            filename = 'text_qr.png'
            path = os.path.join(app.config['QR_FOLDER'], filename)
            img = qrcode.make(data)
            img.save(path)
            qr_path = '/' + path + '?v=' + str(int(time.time()))
        
        elif file and file.filename != '':
            # QR من صورة مرفوعة
            filename = secure_filename(file.filename)
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(img_path)

            # كنولد QR فيه رابط الصورة
            image_url = url_for('static', filename='uploads/' + filename, _external=True)
            qr_filename = 'image_qr.png'
            qr_path_full = os.path.join(app.config['QR_FOLDER'], qr_filename)
            img = qrcode.make(image_url)
            img.save(qr_path_full)
            qr_path = '/' + qr_path_full + '?v=' + str(int(time.time()))

    return render_template('index.html', qr_path=qr_path)

@app.route('/download')
def download():
    path = os.path.join(app.config['QR_FOLDER'], 'text_qr.png')
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return "No QR code generated yet.", 404

if __name__ == '__main__':
    app.run(debug=True)
