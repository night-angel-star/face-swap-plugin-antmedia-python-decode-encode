from flask import Flask, request, jsonify, Response
import time

import base64
import numpy as np
import av
from PIL import Image
from datetime import datetime
import threading

webService = Flask(__name__)

@webService.route('/', methods=['POST'])
def process_request():
    receivedData = request.get_json()  # Get JSON data from the request
    start_time = time.time_ns()  
    save_to_image(receivedData["data"],receivedData["width"],receivedData["height"])
    end_time = time.time_ns()  # Get the current time again
    execution_time = end_time - start_time  # Calculate the difference to get the 
    print("Execution time:", execution_time, "ns")
    return Response(receivedData["data"], status=200, content_type="application/text")

def image_saving_thread(image, path):
    image.save(path)

def save_to_image(encoded,w,h):
    decoded_bytes = base64.b64decode(encoded)

    width=int(w)
    height=int(h)


    data=np.frombuffer(decoded_bytes,dtype=np.uint8)
    y_size = int((2/3) * len(data))
    uv_size = int((1/6) * len(data))

    y_data= data[:y_size]
    u_data=data[y_size:y_size+uv_size]
    v_data=data[y_size+uv_size:]
    half_height=int(height/2)
    half_width=int(width/2)

    y_data = np.array(y_data, dtype=np.uint8).reshape(height,width)
    u_data = np.array(u_data, dtype=np.uint8).reshape(half_height,half_width)
    v_data = np.array(v_data, dtype=np.uint8).reshape(half_height,half_width)

    # u_data = np.repeat(np.repeat(u_data, 2, axis=1),2,axis=0)
    # v_data = np.repeat(np.repeat(v_data, 2, axis=1),2,axis=0)

    # data = np.concatenate((y_data, u_data, v_data), axis=0)

    frame=av.VideoFrame(width, height, 'yuv420p')

    frame.planes[0].update(y_data)
    frame.planes[1].update(u_data)
    frame.planes[2].update(v_data)
    
    numpy_array = frame.to_ndarray(format='rgb24')

    image=Image.fromarray(numpy_array)
    current_datetime = datetime.now()
    time_string = current_datetime.strftime("%Y%m%d_%H%M%S_%f")[:-3]

    path=time_string+'.png'

    save_thread = threading.Thread(target=image_saving_thread, args=(image, path))
    save_thread.start()


webService.run(host='0.0.0.0',port=5000)