import json
import sys
import time

import requests
from flask import Flask, request, render_template, jsonify

from eparser import PageModel

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/parser", methods=["GET", "POST"])
def parser():
    t1 = time.time()
    url = request.args.get('url')
    if url and url.strip() != "":
        page = _get_url_content(url)
    else:
        page = request.form.get("html_content")
    t2 = time.time()
    pm = PageModel(page, url)
    result = pm.extract()
    t3 = time.time()
    return render_template("result.html", data=result['content'], title=result['title'],
                           json_s=json.dumps(result, indent=4),
                           download_cost=t2 - t1, extract_cost=t3 - t2)


@app.route('/article', methods=["GET", "POST"])
def article():
    url = request.args.get('url')
    code = 100

    try:
        if url and url.strip():
            url = url.strip()
            page = _get_url_content(url)
            pm = PageModel(page, url)
            result = pm.extract()
            code = 0
        else:
            result = '错误的URL'
    except:
        result = str(sys.exc_info()[0])

    return jsonify(code=code, result=result)


def _get_url_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/63.0.3239.132 Safari/537.36'}
    rsps = requests.get(url, headers=headers)
    try:
        page = rsps.content.decode('utf-8')
    except:
        page = rsps.content.decode('gb18030', 'ignore')

    return page


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8838, debug='release' != sys.argv[1] if len(sys.argv) >= 2 else '')
