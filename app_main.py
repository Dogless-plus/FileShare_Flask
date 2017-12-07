# coding:utf-8
from flask import Flask,render_template,request,redirect,url_for,send_file,make_response
from shutil import rmtree
from os import path, sep,mkdir,listdir,remove
from utils import get_file_create_time,get_md5,get_filesize


app = Flask(__name__,template_folder="template")
BASEDIR = path.dirname(__file__)
STORAGE = sep.join([BASEDIR,"src"])
code_map = {}   # code map for files

try:
    mkdir(STORAGE)
except:
    pass


# todo:sort by time
@app.route('/', methods=['GET',])
def home():
    files = listdir(STORAGE)
    nfile = len(files)
    codes = [get_md5(f) for f in files]
    filesizes =[get_filesize(sep.join([STORAGE,f])) for f in files]
    global code_map
    code_map=dict(zip(codes,files))
    times = [get_file_create_time(sep.join([STORAGE,f])) for f in files]
    return render_template("home.html",
                           nfile=nfile,
                           items=zip(codes,files,filesizes,times),)

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

@app.route("/download/<filename>/",methods=["GET",])
def download_file(filename):
    filename=code_map[filename]
    response = make_response(send_file(sep.join([STORAGE,filename]),as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response

@app.route("/delete/<filename>/",methods=["GET",])
def delete_file(filename):
    filename = code_map[filename]

    remove(sep.join([STORAGE,filename]))

    # print("unable to delete %s"%filename.encode().decode('latin-1'))
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)