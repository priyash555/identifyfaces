from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.template.loader import render_to_string
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from .models import TestImages
from .forms import TestImageform
import face_recognition as fr
import os
import cv2
import face_recognition
import numpy as np
from time import sleep
from django.conf import settings


# Create your views here.
def starting(request):
    if request.method == 'POST':
        form = TestImageform(request.POST, request.FILES)
        if form.is_valid() :
            
            objs = TestImages.objects.all().delete()
            form.save()
            # class = classify_face("./test/test2.jpg")
            # print(form)
            # print(request.FILES)
            req = request.FILES
            objs = TestImages.objects.all()[0]
            img = classify_face(req['PersonImage'],objs.GroupImage.path)
            finalpath = str(settings.MEDIA_ROOT) + "\\final\\final.jpg"
            print(finalpath)
            cv2.imwrite(finalpath, img)
            objs.ResultImage = finalpath
            # objs.save()
            return render(request, 'home/result.html', {'img':objs})

    else:
        form = TestImageform()
        return render(request, 'home/starting.html', {'form':form})


def about(request):
    return render(request, 'home/about.html', {})

def get_encoded_faces(img):
    encoded = {}
    face = fr.load_image_file(img)
    encoding = fr.face_encodings(face)[0]
    encoded['Person'] = encoding
    return encoded


def unknown_image_encoded(img):
    face = fr.load_image_file("faces/" + img)
    encoding = fr.face_encodings(face)[0]

    return encoding


def classify_face(train_img, test_img):
    faces = get_encoded_faces(train_img)
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    img = cv2.imread(test_img,1) 

    face_locations = face_recognition.face_locations(img)
    unknown_face_encodings = face_recognition.face_encodings(
        img, face_locations)

    face_names = []
    for face_encoding in unknown_face_encodings:
        matches = face_recognition.compare_faces(faces_encoded, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(
            faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Draw a box around the face
            if name != "Unknown" :
                cv2.rectangle(img, (left-20, top-20),
                            (right+20, bottom+20), (255, 0, 0), 2)

                # Draw a label with a name below the face
                # cv2.rectangle(img, (left-20, bottom - 15),
                #             (right+20, bottom+20), (255, 0, 0), cv2.FILLED)
                # font = cv2.FONT_HERSHEY_DUPLEX
            # cv2.putText(img, name, (left - 20, bottom + 15),
            #             font, 1.0, (255, 255, 255), 2)
    # cv2.imshow(img,1)
    return img


