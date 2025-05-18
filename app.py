from flask import Flask, render_template, request
import os
import cv2
import uuid
from utils import read_image, enhance_image, morphological_operations, find_largest_contour, load_templates, predict

UPLOAD_FOLDER = 'static/uploads'
PROCESSED_FOLDER = 'static/processed'
TEMPLATE_FOLDER = 'templates_data'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

print("Templates yükleniyor...")
templates, labels = load_templates(TEMPLATE_FOLDER)
print(f"{len(templates)} adet template yüklendi.")

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    original_image_filename = None
    processed_image_filename = None

    if request.method == 'POST':
        file = request.files['file']

        if file:
            filename = str(uuid.uuid4()) + ".jpg"
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(upload_path)

            img = read_image(upload_path)
            edges = enhance_image(img)
            processed = morphological_operations(edges)
            mask = find_largest_contour(processed)

            if mask is not None:
                result_img = cv2.bitwise_and(img, img, mask=mask)

                # Kontur çizelim
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cv2.drawContours(img, contours, -1, (0, 0, 255), 3)

                prediction = predict(result_img, templates, labels)

                # İşlenen fotoğrafı kaydet
                processed_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
                cv2.imwrite(processed_path, img)

                original_image_filename = filename
                processed_image_filename = filename
            else:
                prediction = "Trafik işareti bulunamadı."

    return render_template('index.html', prediction=prediction, 
                           original_image_filename=original_image_filename, 
                           processed_image_filename=processed_image_filename)

if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)
    app.run(debug=True)