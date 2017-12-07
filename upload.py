# coding:utf-8
from flask import Flask,render_template,request,redirect,url_for
from shutil import rmtree
from os import path, sep,mkdir,listdir
from utils import get_file_create_time

app = Flask(__name__,template_folder="template")
BASEDIR = path.dirname(__file__)
STORAGE = sep.join([BASEDIR,"src"])

try:
    mkdir(STORAGE)
except:
    pass


# todo:sort by time
@app.route('/', methods=['GET',])
def home():
    files = listdir(STORAGE)
    nfile = len(files)
    times = [get_file_create_time(sep.join([STORAGE,f])) for f in files]
    return render_template("home.html",
                           nfile=nfile,
                           filenames= files,
                           filetimes=times)

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        if f:
            store_path = sep.join([STORAGE,f.filename])
            f.save(store_path)
        return redirect(url_for('home'))
    return redirect(url_for('home'))

@app.route("/delete_all/",methods=["GET",])
def delete_all():
    try:
        rmtree(STORAGE)
        mkdir(STORAGE)
    except:
        print("unable to delete all")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)