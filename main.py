from flask import Flask, request, send_file
from kruskal import MST
from email_sort import Sort
from steganography import Steganography
import json
import io

app = Flask(__name__)

@app.route('/email', methods=['POST'])
def sort_email():
    file = request.files['email']
    file.save("emails.txt")
    sort = Sort("emails.txt")
    sort.sort()
    return send_file(sort.output_file)

@app.route('/hide-message', methods=['POST'])
def hide_message():
    message = request.form['message']
    image = request.files['image']
    steg = Steganography()
    data = bytearray(image.read())
    steg.hide_message(data, message)
    return send_file(io.BytesIO(data))

@app.route('/get-message', methods=['POST'])
def extrac_message():
    steg = Steganography()
    image = request.files['image']
    data = bytearray(image.read())
    arr = steg.extract_message(data)
    message = arr.decode()
    print(message)
    return message

@app.route('/kruskal', methods=['POST'])
def get_mst():
    mst = MST(request.json)
    result = mst.get_mst()
    print(result)
    return json.dumps(result)
