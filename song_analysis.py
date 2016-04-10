from flask import Flask
from seolab import parsing
import json
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/seolab/')
def se():
    result = parsing.test(3)
    return str(result)

@app.route('/json')
def jso():
    a = [1,2,3,4,5]
    return json.dumps(a,ensure_ascii=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=8000)
