import numpy as np
from PIL import Image
import image_processing
import os
from flask import Flask, render_template, request, make_response
from datetime import datetime
from functools import wraps, update_wrapper
from shutil import copyfile
import subprocess

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return update_wrapper(no_cache, view)


@app.route("/index")
@app.route("/")
@nocache
def index():
    return render_template("home.html", file_path="img/image_here.png")


@app.route("/about")
@nocache
def about():
    return render_template('about.html')


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route("/file3d", methods=["POST"])
@nocache
def file3d():
    target = os.path.join(APP_ROOT, "static/img")
    if not os.path.isdir(target):
        if os.name == 'nt':
            os.makedirs(target)
        else:
            os.mkdir(target)
    for file in request.files.getlist("file"):
        file.save("static/img/obj_now.obj")
    copyfile("static/img/obj_now.obj", "static/img/obj_normal.obj")
    return render_template("file3d.html", file_path="img/obj_now.obj")


@app.route("/upload", methods=["POST"])
@nocache
def upload():
    target = os.path.join(APP_ROOT, "static/img")
    if not os.path.isdir(target):
        if os.name == 'nt':
            os.makedirs(target)
        else:
            os.mkdir(target)
    for file in request.files.getlist("file"):
        file.save("static/img/img_now.png")
    copyfile("static/img/img_now.png", "static/img/img_normal.png")
    copyfile("static/img/img_now.png", "static/img/test.png")
    return render_template("uploaded.html", file_path="img/img_now.png")


@app.route("/normal", methods=["POST"])
@nocache
def normal():
    copyfile("static/img/img_normal.png", "static/img/img_now.png")
    return render_template("uploaded.html", file_path="img/img_now.png")


@app.route("/grayscale", methods=["POST"])
@nocache
def grayscale():
    image_processing.grayscale()
    return render_template("uploaded.html", file_path="img/img_now.png")


@app.route("/zoomin", methods=["POST"])
@nocache
def zoomin():
    image_processing.zoomin()
    return render_template("uploaded.html", file_path="img/img_now.png")


@app.route("/zoomout", methods=["POST"])
@nocache
def zoomout():
    image_processing.zoomout()
    return render_template("uploaded.html", file_path="img/img_now.png")


@app.route("/move_left", methods=["POST"])
@nocache
def move_left():
    image_processing.move_left()
    return render_template("uploaded.html", file_path="img/img_now.png")


@app.route("/move_right", methods=["POST"])
@nocache
def move_right():
    image_processing.move_right()
    return render_template("uploaded.html", file_path="img/img_now.png")


@app.route("/move_up", methods=["POST"])
@nocache
def move_up():
    image_processing.move_up()
    return render_template("uploaded.html", file_path="img/img_now.png")


@app.route("/move_down", methods=["POST"])
@nocache
def move_down():
    image_processing.move_down()
    return render_template("uploaded.html", file_path="img/img_now.png")


@app.route("/brightness_addition", methods=["POST"])
@nocache
def brightness_addition():
    image_processing.brightness_addition()
    return render_template("uploaded.html", file_path="img/img_now.png")


@app.route("/brightness_substraction", methods=["POST"])
@nocache
def brightness_substraction():
    image_processing.brightness_substraction()
    return render_template("uploaded.html", file_path="img/img_now.png")


@app.route("/brightness_multiplication", methods=["POST"])
@nocache
def brightness_multiplication():
    image_processing.brightness_multiplication()
    return render_template("uploaded.html", file_path="img/img_now.png")


@app.route("/brightness_division", methods=["POST"])
@nocache
def brightness_division():
    image_processing.brightness_division()
    return render_template("uploaded.html", file_path="img/img_now.png")


@app.route("/histogram_equalizer", methods=["POST"])
@nocache
def histogram_equalizer():
    image_processing.histogram_equalizer()
    return render_template("uploaded.html", file_path="img/img_now.png")


@app.route("/edge_detection", methods=["POST"])
@nocache
def edge_detection():
    image_processing.edge_detection()
    return render_template("uploaded.html", file_path="img/img_now.png")


@app.route("/blur", methods=["POST"])
@nocache
def blur():
    image_processing.blur()
    return render_template("uploaded.html", file_path="img/img_now.png")


@app.route("/sharpening", methods=["POST"])
@nocache
def sharpening():
    image_processing.sharpening()
    return render_template("uploaded.html", file_path="img/img_now.png")


@app.route("/histogram_rgb", methods=["POST"])
@nocache
def histogram_rgb():
    image_processing.histogram_rgb()
    if image_processing.is_grey_scale("static/img/img_now.png"):
        return render_template("histogram.html", file_paths=["img/grey_histogram.png"])
    else:
        return render_template("histogram.html", file_paths=["img/red_histogram.png", "img/green_histogram.png", "img/blue_histogram.png"])


@app.route("/thresholding", methods=["POST"])
@nocache
def thresholding():
    lower_thres = np.int_(request.form['lower_thres'])
    upper_thres = np.int_(request.form['upper_thres'])
    image_processing.threshold(lower_thres, upper_thres)
    return render_template("uploaded.html", file_path="img/img_now.png")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
