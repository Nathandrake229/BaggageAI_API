from datetime import datetime, timezone
from model import *
from flask import Flask, render_template, request, make_response  
from werkzeug.utils import secure_filename
import psycopg2
import os
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from xml_to_box import parseXML

ALLOWED_EXTENSIONS = set(['jpg', 'xml'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__, template_folder='templates', static_folder='static')

POSTGRES = {
    'user': 'postgres',
    'pw': 'postgres',
    'db': 'testdb',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['DEBUG'] = True

db.init_app(app)
path = "C:/work/PYTHON/BaggageAI_API/"
path1 = "/static/"
@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        fname = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                fname.append(filename)
                file.save(os.path.join(path, filename))
    name_bnd = parseXML(os.path.join(path, fname[0]), os.path.join(path, fname[1]))
    user_image = os.path.join(path1, name_bnd[2])
    dt = datetime.now(timezone.utc)
    for i in range(len(name_bnd[0])):
        print(name_bnd[0][i][0], name_bnd[0][i][1], name_bnd[0][i][2], name_bnd[0][i][3], name_bnd[1][i], name_bnd[2])
        bgnd = bag_bnd_box(xmn = name_bnd[0][i][0], ymn = name_bnd[0][i][1], xmx = name_bnd[0][i][2], ymx = name_bnd[0][i][3], obj_name = name_bnd[1][i], img_name =  name_bnd[2], date = dt)
        db.session.add(bgnd)
        db.session.commit()
    os.remove(os.path.join(path, fname[0]))
    os.remove(os.path.join(path, fname[1]))
    #os.remove(os.path.join(path1, name_bnd[2]))
    return render_template('uploader.html',  user_image = user_image)

@app.route('/retrieve')
def retrieve():
    return render_template('retrieve.html')

@app.route('/delete')
def delete():
    db.session.query(bag_bnd_box).delete()
    db.session.commit()
    return "succesful"


@app.route('/result', methods=[ 'POST'])
def result():
    if request.method == 'POST':
        start = request.form.get("start-date")
        end = request.form.get("end-date")
        start_date = datetime(int(start.split('-')[0]), int(start.split('-')[1]), int(start.split('-')[1]))
        #print("start date", start_date)
        end_date = datetime(int(end.split('-')[0]), int(end.split('-')[1]), int(end.split('-')[1]))
        di = bag_bnd_box.query.all()
        #print(di)
        csv = []
        for i in di:
            d = i.date
            #print("file",d)
            ob = []
            if(d.date() >=start_date.date() and d.date() <=end_date.date()):
                #print("x",i.xmx)
                ob.append(i.xmn)
                ob.append(i.xmx)
                ob.append(i.ymn)
                ob.append(i.ymx)
                ob.append(i.obj_name)
                ob.append(i.img_name)
                ob.append(i.date)
            csv.append(ob)
        df = pd.DataFrame(csv)
        csv_data = df.to_csv(index=False)
        response = make_response(csv_data)
        cd = 'attachment; filename=result.csv'
        response.headers['Content-Disposition'] = cd 
        response.mimetype='text/csv'

    return response



with app.app_context():
    db.create_all()


if __name__ =='__main__':
    app.run(port=1234, debug=True)