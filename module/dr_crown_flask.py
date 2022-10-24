from flask import Flask
from flask.templating import render_template
from flask import request
from flask_cors import CORS
import json

from module.dr_crown_recommend import Recommend

app = Flask(__name__, static_url_path='')
CORS(app)

@app.route('/')
@app.route('/recommend')
def test01():
    
    p_no = request.args.get('pNo')
    
    recommend = Recommend()
    
    r_list = recommend.getTeethByPatient(p_no)
    
    arr=[]
    for row in r_list:
        arr.append(row)
    
    json_string = json.dumps(arr,ensure_ascii=False)
    return json_string

if __name__ == '__main__':
    app.run()