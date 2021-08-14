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

    source_location = request.POST["location"]
    uploaded_file = request.FILES['document']
    fs = FileSystemStorage()
    name = fs.save(uploaded_file.name, uploaded_file)
    BASE_DIR = stt.BASE_DIR
    path = os.path.join(BASE_DIR, name)
    target_locations = pd.read_csv(path)
    output_df = pd.DataFrame

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--no-sandbox")
    # chrome = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    #
    # for target_location in target_locations['Target Locations']:
    #     output_df = pathCalc.find(request, chrome, source_location, target_location, sourceLocation, targetLocation
    #                               , shortestRouteTitle,
    #                               shortestRouteDistance)
    # chrome.quit()
    #
    # df = pd.DataFrame(
    #     {'Source Location': output_df['sourceLocation'],
    #      'Target Location': output_df['targetLocation'],
    #      'Route Name': output_df['shortestRouteTitle'],
    #      'Route Distance in KMs': output_df['shortestRouteDistance']
    #      })
    #
    # context = {"result": df.to_html()}
    return render(request, 'Distances.html', target_locations)
