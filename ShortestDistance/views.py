import os

import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from selenium import webdriver

import GoogleMaps.settings as stt
import ShortestDistance.PathCalculator as pathCalc


# Create your views here.
def index(request):
    return render(request, 'index.html')


def ShortestPath(request):
    sourceLocation = []
    targetLocation = []
    shortestRouteTitle = []
    shortestRouteDistance = []

    outputFileName = request.POST["outputFileName"]
    source_location = request.POST["location"]
    uploaded_file = request.FILES['document']
    fs = FileSystemStorage()
    name = fs.save(uploaded_file.name, uploaded_file)
    BASE_DIR = stt.BASE_DIR
    path = os.path.join(BASE_DIR, name)
    target_locations = pd.read_csv(path)
    output_df = pd.DataFrame

    chrome = webdriver.Chrome()

    for target_location in target_locations['Target Locations']:
        output_df = pathCalc.find(chrome, source_location, target_location, sourceLocation, targetLocation
                                  , shortestRouteTitle,
                                  shortestRouteDistance)
    chrome.quit()

    df = pd.DataFrame(
        {'Source Location': output_df['sourceLocation'],
         'Target Location': output_df['targetLocation'],
         'Route Name': output_df['shortestRouteTitle'],
         'Route Distance in KMs': output_df['shortestRouteDistance']
         })

    output_filename = outputFileName + '.csv'
    output_path = os.path.join(BASE_DIR, output_filename)

    df.to_csv(output_path, index=False, header=True, encoding='utf-8-sig')
    context = {"result": df.to_html(), 'url': output_path}
    return render(request, 'Distances.html', context)
