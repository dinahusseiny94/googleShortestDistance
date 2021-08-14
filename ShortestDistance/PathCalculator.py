from time import sleep
from django.shortcuts import render
import pandas as pd


def find(request, chrome, source_location, destination, sourceLocation, targetLocation, shortestRouteTitle,
         shortestRouteDistance):
    sleep(2)
    chrome.get("https://www.google.com/maps/dir/" + source_location)
    minDistance = 10000
    minIndex = 0
    routeTitleCol = []
    sleep(5)
    targetLocationInput = chrome.find_element_by_xpath(
        '/html/body/jsl/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[2]/div[2]/div/div/input')
    targetLocationInput.send_keys(destination)
    sleep(5)
    searchButton = chrome.find_element_by_xpath(
        '/html/body/jsl/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[2]/div[2]/button[1]')
    searchButton.click()
    sleep(5)
    routes = chrome.find_elements_by_class_name('section-directions-trip-title')
    routes_distances = chrome.find_elements_by_class_name('section-directions-trip-distance')
    while len(routes) == 0:
        routes = chrome.find_elements_by_class_name('section-directions-trip-title')
        routes_distances = chrome.find_elements_by_class_name('section-directions-trip-distance')
    for routeTitle in routes:
        routeTitleText = routeTitle.text
        if routeTitleText != '':
            routeTitleCol.append(routeTitleText)
    count = 0
    for routeDistance in routes_distances:
        routeDistanceText = routeDistance.text
        routeDistanceText = routeDistanceText.replace('m', '')
        routeDistanceText = routeDistanceText.replace('م', '')
        if 'k' not in routeDistanceText and 'ك' not in routeDistanceText:
            routeDistanceText = str(float(routeDistanceText.strip()) / 1000)
        routeDistanceText = routeDistanceText.replace('k', '')
        routeDistanceInKM = routeDistanceText.replace('ك', '')
        if routeDistanceInKM == '':
            routeDistanceInKM = '10000'
        minRouteDistance = float(routeDistanceInKM.strip())
        if minRouteDistance < minDistance:
            minDistance = minRouteDistance
            minIndex = count
        count = count + 1
    sourceLocation.append(source_location)
    targetLocation.append(destination)
    shortestRouteDistance.append(minDistance)
    shortestRouteTitle.append(routeTitleCol[minIndex])
    dict_result = {"sourceLocation": sourceLocation, "targetLocation": targetLocation,
                   "shortestRouteDistance": shortestRouteDistance, "shortestRouteTitle": shortestRouteTitle}
    df = pd.DataFrame(
        {'Source Location': dict_result['sourceLocation'],
         'Target Location': dict_result['targetLocation'],
         'Route Name': dict_result['shortestRouteTitle'],
         'Route Distance in KMs': dict_result['shortestRouteDistance']
         })

    context = {"result": df.to_html()}
    return render(request, 'Distances.html', context)
