from PIL import Image
import numpy as np
import av
import base64

# Read the image using Pillow
image = Image.open('image2.png')
image = image.convert('RGB')

# Convert the image to a NumPy array
image_array = np.array(image)

# Create a VideoFrame from the image array
frame = av.VideoFrame.from_ndarray(image_array, format='rgb24')
frame=frame.reformat(format='yuv420p')
y_data=frame.planes[0].to_bytes()
u_data=frame.planes[1].to_bytes()
v_data=frame.planes[2].to_bytes()

frame_data = y_data+u_data+v_data
encoded_data = base64.b64encode(frame_data)
decoded_data = encoded_data.decode('utf-8')

with open('output2.dat', 'w') as file:
    file.write(decoded_data)