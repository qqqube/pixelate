from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import cv2

app = Flask(__name__)
UPLOAD_FOLDER = 'static/input'
PIXELATED_FOLDER = 'static/output'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_PIXEL_SIZES = {4, 8, 16, 32, 64}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PIXELATED_FOLDER'] = PIXELATED_FOLDER

def allowed_file(img_name):
    return '.' in img_name and img_name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print("file: \n")
        print(file)
        pixel_size = int(request.form.get("pixel_size"))
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename) and pixel_size in ALLOWED_PIXEL_SIZES:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            pixelated = pixelate(filepath, pixel_size)
            pixelated_path = os.path.join(app.config['PIXELATED_FOLDER'], filename)
            print(filepath)
            print(pixelated_path)
            cv2.imwrite(pixelated_path, pixelated)
            return render_template("pixel.html", original=filepath, new=pixelated_path)
    return render_template("index.html")




def pixelate(image_path, size):
    img = cv2.imread(image_path)
    height, width = img.shape[:2]
    w, h = (size, size)
    temp = cv2.resize(img, (w, h), interpolation=cv2.INTER_LINEAR)
    output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
    return output



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
