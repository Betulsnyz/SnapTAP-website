import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image

app = Flask(__name__)
CORS(app)

# Kabul edilen dosya uzantıları
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Maksimum dosya boyutu (byte cinsinden) - 5 MB olarak ayarlandı
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

# Modeli yükle
model_path = os.path.join(os.path.dirname(__file__), '..', 'ai', 'vgg16_finetuned.h5')
model = load_model(model_path)

# Sınıf isimlerini tanımla
class_names = ['siirt', 'kırmızı']  # Bu sınıfları modeline göre güncelleyebilirsin

# Dosya uzantısının kontrol edilmesi
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Dosya yüklenmedi!'}), 400

    file = request.files['file']

    # Dosya adı kontrolü ve geçerli uzantı kontrolü
    if file.filename == '':
        return jsonify({'error': 'Dosya seçilmedi!'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Geçersiz dosya türü! Sadece png, jpg, jpeg uzantılı dosyalar yüklenebilir.'}), 400

    # Dosya boyutunu kontrol et
    file.seek(0, os.SEEK_END)  # Dosyanın sonuna git
    file_length = file.tell()  # Dosyanın boyutunu al
    if file_length > MAX_FILE_SIZE:
        return jsonify({'error': 'Dosya boyutu çok büyük! Maksimum 5 MB olabilir.'}), 400

    file.seek(0)  # Dosya pozisyonunu sıfırla, böylece okuma tekrar başlayabilir

    # Resmi işleyelim
    img = Image.open(file)
    img = img.resize((128, 128))  # Modelin beklediği boyuta göre yeniden boyutlandır
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalizasyon

    # Model ile tahmin yapalım
    predictions = model.predict(img_array)
    predicted_probability = predictions[0][0]

    threshold = 0.5  # Eşik değeri
    predicted_class = 0 if predicted_probability > threshold else 1

    print("Tahmin edilen sınıf indeksi:", predicted_class)
    print("Modelin tahmin sonuçları:", predictions)

    # Sınıf ismini geri döndürelim
    predicted_class_name = class_names[predicted_class]

    # Sınıf ismini belirleyelim
    if predicted_class < len(class_names):
        predicted_class_name = class_names[predicted_class]
    else:
        predicted_class_name = "Unknown"

    return jsonify({'class': predicted_class_name})

if __name__ == '__main__':
    app.run(debug=True)
