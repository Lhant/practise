import json

import mpld3
from flask import Flask, render_template, jsonify, request, make_response
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
from mpld3._display import NumpyEncoder

import function.myFunction as myFun
import function.nonlinear as nol
import function.WEBmpld3 as WEBmpld3
import pp.pp as pp

app = Flask(__name__)


@app.route('/index')
@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/notice')
def notice():
    return render_template('notice.html')


@app.route('/clock')
def clock():
    return render_template('clock.html')


@app.route('/pages/test1')
def test1():
    return render_template('pages/test1.html')


@app.route('/pages/test2')
def test2():
    return render_template('pages/test2.html')


@app.route('/pages/noLinTemplates')
def noLinTemplates():
    fig = plt.figure()
    plt.plot()
    single_chart = dict()
    single_chart['id'] = "fig_01"
    single_chart['json'] = json.dumps(mpld3.fig_to_dict(fig))
    result = {'single_chart': single_chart}
    plt.close()
    return render_template('pages/noLinTemplates.html', result=result)


# --------------------------------以下为数据获取--------------------------------
@app.route('/getData')
def imgData():
    plt.switch_backend('agg')
    buf = BytesIO()
    x = np.arange(1, 11)
    y = 2 * x + 5
    plt.title("Matplotlib demo")
    plt.xlabel("x axis caption")
    plt.ylabel("y axis caption")
    plt.plot(x, y)
    plt.savefig(buf)
    imd = myFun.saveBase64Img(buf)
    return jsonify({"success": 200, "msg": "成功", "img_url": imd})


@app.route('/getTest2Data', methods=["POST"])
def getTest2Data():
    plt.switch_backend('agg')
    x, y, a = float(request.form.get('x')), float(request.form.get('y')), float(request.form.get('a'))
    print(a, y, x)
    imd = nol.funImg(x, y, a)
    return jsonify({"success": 200, "msg": "成功", "img_url": imd})


@app.route('/getNoLinTemplatesJson', methods=['POST'])
def getNoLinTemplatesJson():
    imgFig = pp.main(request.files['jf'])
    single_chart = dict()
    single_chart['id'] = "imgData"
    single_chart['json'] = json.dumps(mpld3.fig_to_dict(imgFig))
    result = {'single_chart': single_chart}
    return render_template('pages/noLinTemplates.html', result=result)


if __name__ == '__main__':
    app.run(host='192.168.2.238', port=5000, debug=False)
