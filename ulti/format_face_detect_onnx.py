import cv2
import numpy as np
import onnx
import vision.utils.box_utils_numpy as box_utils
import onnxruntime.backend as backend
import torch
from ulti.model import MobileFaceNet
import torchvision
import torch.nn as nn
# onnx runtime
import onnxruntime as ort
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# from tensorflow.keras.preprocessing.image import img_to_array
# from tensorflow.keras.models import model_from_json

def predict(width, height, confidences, boxes, prob_threshold, iou_threshold=0.3, top_k=-1):
    boxes = boxes[0]
    confidences = confidences[0]
    picked_box_probs = []
    picked_labels = []
    for class_index in range(1, confidences.shape[1]):
        probs = confidences[:, class_index]
        mask = probs > prob_threshold
        probs = probs[mask]
        if probs.shape[0] == 0:
            continue
        subset_boxes = boxes[mask, :]
        box_probs = np.concatenate([subset_boxes, probs.reshape(-1, 1)], axis=1)
        box_probs = box_utils.hard_nms(box_probs,
                                       iou_threshold=iou_threshold,
                                       top_k=top_k,
                                       )
        picked_box_probs.append(box_probs)
        picked_labels.extend([class_index] * box_probs.shape[0])
    if not picked_box_probs:
        return np.array([]), np.array([]), np.array([])
    picked_box_probs = np.concatenate(picked_box_probs)
    picked_box_probs[:, 0] *= width
    picked_box_probs[:, 1] *= height
    picked_box_probs[:, 2] *= width
    picked_box_probs[:, 3] *= height
    return picked_box_probs[:, :4].astype(np.int32), np.array(picked_labels), picked_box_probs[:, 4]

def feature_normalization(embedding_features):
    normalized_features = embedding_features/np.linalg.norm(embedding_features)
    return normalized_features

def feature_comparison(feature_1, feature_2):

    cosine = np.dot(feature_1, feature_2)
    cosine = np.clip(cosine, -1.0, 1.0)

    return cosine

def processing_image(img):
    try:
        if img is not None:
            img = cv2.GaussianBlur(img,(5,5),1)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (112, 112))

            img = img/255
            img = img.transpose(2, 0, 1)
            img = img[None, :]
            img = torch.from_numpy(img).float()

            return img
        else: pass
    except: print("Lỗi process")

def nor_emb(img):
    try:
        if img is not None:
            with torch.no_grad():
                img = processing_image(img)
                img = img.to(device)
                embedding_features = net(img)
                embedding_features = embedding_features.squeeze()
                embedding_features = embedding_features.data.cpu().numpy()
                return embedding_features
        else: pass
    except: print("Lỗi nor")

def avg_emb(path,embed = None):
    for image in os.listdir(path):
        img = cv2.imread(os.path.join(path,image))
        embeddding_features = nor_emb(img)
        if embed is None:
            embed = np.zeros((embeddding_features.shape[0],))
        embed = np.add(embed,embeddding_features)
    embed = embed/len(os.listdir(path))
    normalized_features = feature_normalization(embed)
    return normalized_features

def trans_img(orig_image):
    try:
        if orig_image is not None:
            image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, (320, 240))
            # image = cv2.resize(image, (640, 480))
            image_mean = np.array([127, 127, 127])
            image = (image - image_mean) / 128
            image = np.transpose(image, [2, 0, 1])
            image = np.expand_dims(image, axis=0)
            image = image.astype(np.float32)
            return image
        else: pass
    except: print("Lỗi trans")

def string2array64(feature):
    feature_lst = feature.strip("[]").split(",")
    feature_arr = np.array(feature_lst).astype(np.float64)
    return feature_arr

def process_spoof(img):
    try:
        if img is not None:
            resized_face = cv2.resize(img,(160,160))
            resized_face = resized_face.astype("float")/255.0
            # resized_face = img_to_array(resized_face)
            resized_face = np.expand_dims(resized_face, axis=0)
            return resized_face
    except: print("Lỗi process_spoof")

cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred, {
        "databaseURL": "https://faceattendacerealtime-50d4e-default-rtdb.firebaseio.com/"
    })

# Device
device = torch.device("cpu")
threshold = 0.7

# Load file
label_path = "models/voc-model-labels.txt"
onnx_path = "models/onnx/version-RFB-320.onnx"
image_path = "image/"
weight_path_cos = "models/face_recog/300.pth"
weight_path_realfake = "models/face_anti/005.pth"

# Load info Face detector
class_names = [name.strip() for name in open(label_path).readlines()]

predictor = onnx.load(onnx_path)
onnx.checker.check_model(predictor)
onnx.helper.printable_graph(predictor.graph)
predictor = backend.prepare(predictor, device="CPU")  # default CPU

ort_session = ort.InferenceSession(onnx_path)
input_name = ort_session.get_inputs()[0].name


model = torchvision.models.mobilenet_v2(weights=True)
model.classifier[1] = nn.Linear(in_features=1280, out_features=2)
model.load_state_dict(torch.load(weight_path_realfake, map_location=device))


# Init model
net = MobileFaceNet()
# Load the trained model from the folder ./saved_model
net.load_state_dict(torch.load(weight_path_cos, map_location=device))
net.eval()
net = net.to(device)

