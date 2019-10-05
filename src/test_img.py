from config import getApi
import os
api = getApi()

def postWithImage(update, media):
    print(api.PostUpdate(update, media=media))
    os.remove(media)

postWithImage("hi", "tempplot.png")
