from flask import Flask
from seolab import gaon_chart
from muse import gaon_to_melon
#from ldav import pylda

import json
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/seolab/<year>/<week>')
def se(year,week):
    if year and week:
        result = gaon_chart.gaon_top_rank(year,week)
        return json.dumps(result,ensure_ascii='False')
    else:
        return "error value"

@app.route('/seolab/gaon_<ga_id>')
def get_melon_album(ga_id):
    try:
        result = gaon_to_melon.ga_mel(gaon_id=ga_id)
        return result

    except:
        return "error value"

@app.route('/json')
def jso():
    a = [1,2,3,4,5]
    return json.dumps(a,ensure_ascii=False)

@app.route("/ldav")
def lda_view():
    return "Progressing"
    #return pylda.get_lda()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)


