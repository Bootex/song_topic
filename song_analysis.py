from flask import Flask
from seolab import gaon_chart
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


@app.route('/json')
def jso():
    a = [1,2,3,4,5]
    return json.dumps(a,ensure_ascii=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)
