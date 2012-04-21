#-*- coding: UTF-8 -*-
from JJEhr import settings

__author__ = 'sam.sun'

def event_type_image_prefix_url(request):
    return {"event_type_image_prefix_url": settings.EVENT_TYPE_IMAGE_URL_PREFIX}

