import cv2
import numpy as np
import os

def read_image(path):
    img = cv2.imread(path)
    if img is None:
        raise ValueError(f"Görsel bulunamadı: {path}")
    img = cv2.resize(img, (300, 300))
    return img

def enhance_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    return edges

def morphological_operations(edges):
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=1)
    eroded = cv2.erode(dilated, kernel, iterations=1)
    return eroded

def find_largest_contour(processed_img):
    contours, _ = cv2.findContours(processed_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    largest_contour = max(contours, key=cv2.contourArea)
    mask = np.zeros(processed_img.shape, dtype=np.uint8)
    cv2.drawContours(mask, [largest_contour], -1, 255, thickness=cv2.FILLED)
    return mask

def extract_orb_features(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create()
    keypoints, descriptors = orb.detectAndCompute(gray, None)
    return keypoints, descriptors

def load_templates(template_folder):
    templates = []
    labels = []
    label_list = open('labels.txt', 'r', encoding='utf-8').read().splitlines()

    for foldername in sorted(os.listdir(template_folder)):
        folder_path = os.path.join(template_folder, foldername)
        if os.path.isdir(folder_path) and foldername.isdigit():
            idx = int(foldername)
            if idx < len(label_list):
                for filename in os.listdir(folder_path):
                    img_path = os.path.join(folder_path, filename)
                    img = read_image(img_path)
                    kp, des = extract_orb_features(img)
                    templates.append((kp, des))
                    labels.append(label_list[idx])
    return templates, labels

def predict(img, templates, labels):
    orb = cv2.ORB_create()
    kp2, des2 = extract_orb_features(img)

    if des2 is None:
        return "Trafik işareti bulunamadı (özellik yok)"

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    best_score = -1
    prediction = None

    for (kp1, des1), label in zip(templates, labels):
        if des1 is None:
            continue

        matches = bf.match(des1, des2)

        # Kaliteli eşleşmeleri seçiyoruz: distance < 50
        good_matches = [m for m in matches if m.distance < 50]

        if len(good_matches) > best_score:
            best_score = len(good_matches)
            prediction = label

    # Çok az kaliteli eşleşme varsa "emin değilim" diyelim
    if best_score < 10:
        return "Emin değilim (çok az kaliteli eşleşme)"

    return prediction
