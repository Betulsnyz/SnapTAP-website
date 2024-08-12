import os
import numpy as np
from sklearn.metrics import classification_report
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator


# Dosya yollarını belirtin
model_load_path = os.path.join(os.path.dirname(__file__),'vgg16_finetuned.h5')
test_data_load_path = os.path.join(os.path.dirname(__file__), 'test_data.npz')

# Modeli yükle
model = load_model(model_load_path)

# Test verilerini yükle
test_data = np.load(test_data_load_path)
X_test = test_data['X_test']
y_test = test_data['y_test']

# Data Augmentation tekniklerinin uygulanması
datagen = ImageDataGenerator(
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.2,
    horizontal_flip=True,
    shear_range=0.1
)
# deneme

# Modeli değerlendirin
test_generator = datagen.flow(X_test, y_test, batch_size=16, shuffle=False)
test_loss, test_acc = model.evaluate(test_generator, steps=len(test_generator))
print(f"Test Doğruluğu: {test_acc:.4f}")

# Tahminler
y_pred_probs = model.predict(test_generator, steps=len(test_generator))
y_pred = (y_pred_probs > 0.5).astype(int).flatten()

# Doğru ve yanlış tahminlerin sayısını gösterme
correct_predictions = np.sum(y_test == y_pred)
incorrect_predictions = len(y_test) - correct_predictions

print("Fine-Tuning Sonrası Classification Report:\n", classification_report(y_test, y_pred, target_names=['kırmızı', 'siirt']))
print(f"Doğru Tahmin Sayısı: {correct_predictions}")
print(f"Yanlış Tahmin Sayısı: {incorrect_predictions}")

# Yanlış tahmin edilen verileri göster
incorrect_indices = np.where(y_test != y_pred)[0]
for idx in incorrect_indices:
    actual_label = 'kırmızı' if y_test[idx] == 0 else 'siirt'
    predicted_label = 'kırmızı' if y_pred[idx] == 0 else 'siirt'
    print(f"Index {idx}: Gerçek Etiket = {actual_label}, Tahmin Edilen Etiket = {predicted_label}")


