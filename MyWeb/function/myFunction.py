import base64
import numpy as np
from io import BytesIO


def saveBase64Img(buf: BytesIO):
    plot_data = buf.getvalue()
    imb = base64.b64encode(plot_data)  # 对plot_data进行编码
    ims = imb.decode()
    imd = "data:image/png;base64," + ims
    return imd


def toJson(obj):
    objJson = {}
    for item in obj:
        if type(obj[item]) == np.ndarray:
            objJson.update({item: obj[item].tolist()})
        else:
            objJson.update({item: obj[item]})
    return objJson
