from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from threading import Thread
import requests

import json
import os
import sys

sys.path.append('..')

from .Utilitites import parse_ids
from .Rankade import rankade

def index(request):
    return render(request, 'index.html')

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



def backgroundworker(players, scores, response_url):

    try:
        print("*"*25 + "_logging in_" + "*"*25)
        r = rankade.Rankade(os.environ['username'], os.environ['token'])
        print("*"*25 + "_logged in_" + "*"*25)

        print("*"*25 + "_adding_matches_" + "*"*25)
        r.add_matches(players, scores)
        r.close()
        print("*"*25 + "_done adding matches_" + "*"*25)

        payload = {"text":"Successfully added matches",
                   "username": "bot"}

        requests.post(response_url,data=json.dumps(payload))

    except Exception as ex:
        d = {'error': 'Unable to add scores: {0}'.format(ex)}
        data = json.dumps(d)
        return HttpResponse(data, content_type='application/json')

@csrf_exempt
def slack_score(request):
    if request.method == 'POST':
        print('Recording scores')

        print(request.POST)

        response_url = request.POST['response_url']

        try:
            text = request.POST['text']
            players, scores = rankade.read_match(text)
            print(players)
            print(scores)

            thr = Thread(target=backgroundworker, args=[players, scores, response_url])
            thr.start()

            d = {'Adding the following matches': '{0}{1}'.format(players, scores)}

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


import time

def stopwatch(seconds):
    start = time.time()
    time.clock()
    elapsed = 0
    while elapsed < seconds:
        elapsed = time.time() - start
        print("loop cycle time: %f, seconds count: %02d" % (time.clock() , elapsed))
        r = requests.get(url = "rl.jesuszarate.com")
        time.sleep(1)

stopwatch(20)