import torch 
from ulti.model import MobileFaceNet
import cv2
import numpy as np

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

def feature_normalization(embedding_features):
    normalized_features = embedding_features/np.linalg.norm(embedding_features)
    
    return normalized_features

def feature_comparison(feature_1, feature_2):

    cosine = np.dot(feature_1, feature_2)
    cosine = np.clip(cosine, -1.0, 1.0)

    return cosine

def processing_image(img):

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (112, 112))

    img = img/255
    img = img.transpose(2, 0, 1)
    img = img[None, :]
    img = torch.from_numpy(img).float()

    return img 

threshold = 0.6

    # path to image of two face we want to verify (same or different person)
face1_path = 'Org_images.jpg'
face2_path = 'Org_images_2.jpg'

# read images
img1 = cv2.imread(face1_path)
img2 = cv2.imread(face2_path)

# init MobileFaceNet model
net = MobileFaceNet()

# load trained model from folder ./saved_model
net.load_state_dict(torch.load('100.pth',map_location=torch.device('cpu')))

# 
net.eval()
net = net.to(device)

with torch.no_grad():
    # pre-processing image before input to model
    img1 = processing_image(img1)
    img2 = processing_image(img2)

    img1 = img1.to(device)
    img2 = img2.to(device)

    # input face image to model to get embedding features
    embedding_features1 = net(img1)
    embedding_features1 = embedding_features1.squeeze()

    embedding_features2 = net(img2)
    embedding_features2 = embedding_features2.squeeze()

    # convert features from torch to numpy
    embedding_features1 = embedding_features1.data.cpu().numpy()
    embedding_features2 = embedding_features2.data.cpu().numpy()

    # normalize embedding features
    normalized_features1 = feature_normalization(embedding_features1)
    normalized_features2 = feature_normalization(embedding_features2)

    cosine = feature_comparison(normalized_features1, normalized_features2)

    if cosine > threshold:
        print('Cosin = {}: TWO FACE ARE SAME PERSON'.format(cosine))

    else:
        print('Cosin = {}: TWO FACE ARE DIFFERENT PERSON'.format(cosine))