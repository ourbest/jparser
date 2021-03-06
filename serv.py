import json
import sys
import time

import requests
from flask import Flask, request, render_template, jsonify

import sentry_reporter
from eparser import PageModel

app = Flask(__name__)

sentry_reporter.init_sentry(app)


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


@app.route("/spi/url/article", methods=["GET", "POST"])
@app.route('/article', methods=["GET", "POST"])
def article():
    current_time = time.time()
    url = request.values.get('url')
    code = 100

    try:
        if url and url.strip():
            url = url.strip()
            if not url.startswith('http://www.qle.me'):
                page = _get_url_content(url)
                if 'error' == page:
                    page = _get_url_content(url)
                if 'error' == page:
                    return jsonify(code=code, result='访问过于频繁')
                pm = PageModel(page, url)
                result = pm.extract()
                code = 0
            else:
                result = '错误的URL'

        else:
            result = '错误的URL'
    except:
        result = str(sys.exc_info()[0])

    total = time.time() - current_time
    if total > 60:
        sentry_reporter.sentry.captureMessage('process url %s too long %ss' % (url, total))

    return jsonify(code=code, result=result)


def _get_url_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/63.0.3239.132 Safari/537.36'}
    with requests.get(url, headers=headers, stream=True, timeout=(10, 30), proxies={
        'http': 'http://10.9.131.47:3128',
        'https': 'http://10.9.131.47:3128'
    }) as resp:
        if int(resp.headers.get('content-length', '0')) > 1024 * 1024:
            return ''
        try:
            page = resp.content.decode('utf-8')
        except:
            page = resp.content.decode('gb18030', 'ignore')

        if '访问过于频繁，请用微信扫描二维码' in page:
            sentry_reporter.sentry.captureMessage('process url %s 访问过于频繁' % url)
            return 'error'

        return page


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8838, debug='release' != sys.argv[1] if len(sys.argv) >= 2 else '')
