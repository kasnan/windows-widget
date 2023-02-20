from PIL import Image
import os
print(Image.open('./out.gif').info)

# FILENAME = os.path.join(os.path.dirname(__file__),
#                         './out.gif')
# print(Image.open(FILENAME).info['duration'])