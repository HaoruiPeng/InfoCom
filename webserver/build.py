from flask import Flask, redirect, render_template, jsonify, request
import json

app = Flask(__name__)

@app.route('/')
def do_GET():
    return render_template('index.html')

@app.route('/submit',  methods=['POST'])
def do_submit():
    r = json.loads(request.data.decode())
    data = {'src_x': float(r['src_x']),
            'src_y': float(r['src_y']),
            'dst_x': float(r['dst_x']),
            'dst_y': float(r['dst_y']),
            }
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
