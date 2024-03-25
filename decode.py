import base64
import numpy as np
import av
from PIL import Image
import json

# Open the file in read mode
with open('output2.dat', 'r') as file:
    # Read the content of the file and store it in a variable
    file_content = file.read()
    # file_content=json.loads(file_content)

    decoded_bytes = base64.b64decode(file_content)

    height=480
    width=640

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
    image.save('output.png')
    # print(frame)