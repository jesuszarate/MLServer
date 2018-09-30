from django import forms
from django.shortcuts import render, HttpResponse
import json
import os
import sys

sys.path.append('..')

import config
from .Classifier.classify_image import classify
from .RecommendationSystem.rec_sys import RecommendationSystem as rec_sys
from .Utilitites import parse_ids
from .Rankade import rankade


class UploadFileForm(forms.Form):
    file = forms.FileField()


def index(request):
    return render(request, 'index.html')


def recSystem(request):
    rs = rec_sys()
    html = "<div><b>{0}<b></div>".format(rs.greeting())
    return HttpResponse(html)


def uploadPicture(request):
    return render(request, 'upload_picture.html')


def jj(request):
    d = {'jj': 'this is the value'}
    data = json.dumps(d)
    return HttpResponse(data, content_type='application/json')


def handle_uploaded_file(f):
    path = os.path.join(config.IMAGES_PATH, 'name.jpg')
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def upload_pic(request):
    if request.method == 'POST':

        handle_uploaded_file(request.FILES['image'])

        scores = classify("name")

        data = json.dumps(scores)

        return HttpResponse(data, content_type='application/json')

    else:
        return HttpResponse('<center><h1>Invalid request. It must be a post request</h1></center>')


def load_ids(request):
    return render(request, 'parse_ids.html')


def get_ids(request):
    print(request.GET['ids'])
    num, ids = parse_ids.get_ids(request.GET['ids'])

    html = "<div>{0}</div><br><br><div>{1}</div>".format(ids, num)

    return HttpResponse(html)


def record_rankade_score(request):
    return render(request, 'rankade_scores.html')


def send_rankade_scores(request):
    if request.method == 'POST':
        print('Recording scores')

        try:
            players, scores = rankade.read_match(request.POST["matches"])

            r = rankade.Rankade(os.environ['username'], os.environ['token'])

            r.add_matches(players, scores)
            r.close()

            d = {'Success': '{0}{1}'.format(players, scores)}

            data = json.dumps(d)
            return HttpResponse(data, content_type='application/json')
        except Exception as ex:
            d = {'error': 'Unable to add scores: {0}'.format(ex)}
            data = json.dumps(d)
            return HttpResponse(data, content_type='application/json')
    else:
        d = {'error': 'must be a post request'}
        data = json.dumps(d)
        return HttpResponse(data, content_type='application/json')
