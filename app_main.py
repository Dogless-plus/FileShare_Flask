# coding:utf-8
from flask import Flask,render_template,request,redirect,url_for,send_file,make_response
from shutil import rmtree
from os import path, sep,mkdir,listdir,remove
from utils import get_file_create_time,get_md5,get_filesize,get_foldersize,sort_by_time


app = Flask(__name__,template_folder="template")
BASEDIR = path.abspath(path.dirname(__file__))
STORAGE = path.abspath(sep.join([BASEDIR,"src"]))
code_map = {}   # code map for files

try:
    mkdir(STORAGE)
except:
    pass


@app.route('/', methods=['GET',])
def home():
    files = listdir(STORAGE)
    nfile = len(files)
    codes = [get_md5(f) for f in files]
    filesizes =[get_filesize(sep.join([STORAGE,f])) for f in files]
    memory = get_foldersize(STORAGE)
    global code_map
    code_map=dict(zip(codes,files))
    times = [get_file_create_time(sep.join([STORAGE,f])) for f in files]
    codes, files, filesizes, times = sort_by_time(codes,files,filesizes,times)
    return render_template("home.html",
                           nfile=nfile,
                           memory=memory,
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
    try:
        remove(sep.join([STORAGE,filename]))
    except:
        print("unable to delete %s"%filename.encode().decode('latin-1'))
    return redirect(url_for('home'))

if __name__ == '__main__':
    print(BASEDIR)
    print(STORAGE)
    app.run(host="0.0.0.0",
            port=10086,
            threaded=True,)