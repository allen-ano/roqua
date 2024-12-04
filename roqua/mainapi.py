"""
所有程序入口
"""
from llm import Qwen
from douyin.api import DouyinAPI
from yelp.api import YelpAPI
from flask import Flask, request, jsonify
from flask_cors import CORS

llm = Qwen()
dapi = DouyinAPI(llm)
yapi = YelpAPI(llm)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app, resources=r'/*')

@app.route('/douyin', methods=['GET', 'POST'])
def getDouyinApi():
    try:
        data = request.get_json()  # 使用get_json()方法
        query = data.get('query')
        if not query:
            return "Query not provided"
        opinion = dapi.run(query)
        return opinion  # 返回 JSON 格式的响应
    except Exception as e:
        return "error"


@app.route('/yelp', methods=['GET', 'POST'])
def getYelpApi():  # 修改函数名
    try:
        data = request.get_json()  # 使用get_json()方法
        query = data.get('query')
        if not query:
            return "Query not provided"
        opinion = yapi.run(query)
        return opinion  # 返回 JSON 格式的响应
    except Exception as e:
        return "error"

if __name__ == '__main__':
    app.run(debug=False)  # 添加 debug=True 方便调试
"""
所有程序入口
"""
from llm import Qwen
from douyin.api import DouyinAPI
from yelp.api import YelpAPI
from flask import Flask, request, jsonify
from flask_cors import CORS

llm = Qwen()
dapi = DouyinAPI(llm)
yapi = YelpAPI(llm)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app, resources=r'/*')

@app.route('/douyin', methods=['GET', 'POST'])
def getDouyinApi():
    try:
        data = request.get_json()  # 使用get_json()方法
        query = data.get('query')
        if not query:
            return "Query not provided"
        opinion = dapi.run(query)
        return opinion  # 返回 JSON 格式的响应
    except Exception as e:
        return "error"


@app.route('/yelp', methods=['GET', 'POST'])
def getYelpApi():  # 修改函数名
    try:
        data = request.get_json()  # 使用get_json()方法
        query = data.get('query')
        if not query:
            return "Query not provided"
        opinion = yapi.run(query)
        return opinion  # 返回 JSON 格式的响应
    except Exception as e:
        return "error"

if __name__ == '__main__':
    app.run(debug=False)  # 添加 debug=True 方便调试
