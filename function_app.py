import azure.functions as func
import logging
import cv2
import base64
import numpy as np
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# Define os intervalos de cores em HSV
def is_red(h, s, v):
    return ((h >= 0 and h <= 10) or (h > 160 and h <= 180)) and s > 100 and v > 100

def is_orange(h, s, v):
    return h > 10 and h <= 25 and s > 100 and v > 100

def is_yellow(h, s, v):
    return h > 25 and h <= 35 and s > 100 and v > 100

def is_green(h, s, v):
    return h > 35 and h <= 85 and s > 100 and v > 100

def is_blue(h, s, v):
    return h > 85 and h <= 140 and s > 100 and v > 100

def is_black(h, s, v):
    return v <= 30

def get_dominant_color(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    height, width, _ = hsv_image.shape

    color_count = {
        'red': 0,
        'blue': 0,
        'yellow': 0,
        'green': 0,
        'orange': 0,
        'black': 0
    }

    for y in range(height):
        for x in range(width):
            h, s, v = hsv_image[y, x]

            if is_red(h, s, v):
                color_count['red'] += 1
            elif is_blue(h, s, v):
                color_count['blue'] += 1
            elif is_yellow(h, s, v):
                color_count['yellow'] += 1
            elif is_green(h, s, v):
                color_count['green'] += 1
            elif is_orange(h, s, v):
                color_count['orange'] += 1
            elif is_black(h, s, v):
                color_count['black'] += 1

    dominant_color = max(color_count, key=color_count.get)

    return dominant_color, color_count['red'],color_count['blue'],color_count['yellow'], color_count['green'],color_count['orange'],color_count['black']


@app.route(route="http_trigger_read_color")
def http_trigger_read_color(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try: 

        req_body = req.get_json()
        image_base64 = req_body.get('image_base64')
        image_data = base64.b64decode(image_base64)
        np_array = np.frombuffer(image_data, dtype=np.uint8)
        image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        dominant_color, red, blue, yellow, green, orange, black = get_dominant_color(image)

        collor = { "dominant_color": dominant_color, "colors": {"red": red, "blue": blue, "yellow":yellow, "orange": orange, "green": green, "black": black } }
        json_collor = json.dumps(collor, ensure_ascii=False)

        return func.HttpResponse(json_collor, status_code=200)
    
    except ValueError:

        return func.HttpResponse("This HTTP triggered function executed with erros." + str(ValueError), status_code=500)
