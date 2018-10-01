from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
def slack_score(request):
    if request.method == 'POST':
        print('Recording scores')

        print(request.POST)
        try:
            text = request.POST['text']
            # players, scores = rankade.read_match(request.POST["matches"])
            players, scores = rankade.read_match(text)
            print(players)
            print(scores)
        #
        #     r = rankade.Rankade(os.environ['username'], os.environ['token'])
        #
        #     r.add_matches(players, scores)
        #     r.close()
        #
        #     d = {'Success': '{0}{1}'.format(players, scores)}
        #
        #     data = json.dumps(d)
        #     return HttpResponse(data, content_type='application/json')
        except Exception as ex:
            d = {'error': 'Unable to add scores: {0}'.format(ex)}
            data = json.dumps(d)
        return HttpResponse(json.dumps({'Success': "nice!"}), content_type='application/json')
    else:
        d = {'error': 'must be a post request'}
        data = json.dumps(d)
        return HttpResponse(data, content_type='application/json')

