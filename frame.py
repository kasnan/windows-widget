import os
from PIL import Image, ImageSequence

def get_frameCnt(PIL_Image_object):
    FILENAME = os.path.join(os.path.dirname(__file__),
                        './default.gif')
    """ Returns the average framerate of a PIL Image object """
    PIL_Image_object.seek(0)
    frames = duration = 0
    while True:
        try:
            frames += 1
            duration += PIL_Image_object.info['duration']
            PIL_Image_object.seek(PIL_Image_object.tell() + 1)
        except EOFError:
            if int(frames/10):
                return int(frames / 10) * 10
            return frames
    return None

def process_frame(im,filepath):
    size = im.size
    frames = ImageSequence.Iterator(im)

    # Wrap on-the-fly thumbnail generator
    def thumbnails(frames):
        for frame in frames:
            thumbnail = frame.copy()
            thumbnail.thumbnail(size, Image.LANCZOS)
            yield thumbnail

    frames = thumbnails(frames)
    
    # Save output
    om = next(frames) # Handle first frame separately
    om.save(filepath, save_all=True, append_images=list(frames))

