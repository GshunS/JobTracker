import sqlalchemy
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_cors import CORS, cross_origin
from enum import Enum

pymysql.install_as_MySQLdb()
app = Flask(__name__)
CORS(app)

"""
==============================================================================================================
                                              Configs
==============================================================================================================
"""

class Config(object):
    user = 'root'
    password = 'admin123'
    database = 'Kiwi'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@127.0.0.1:3306/%s' % (user, password, database)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False

app.config.from_object(Config)
db = SQLAlchemy(app)

"""
==============================================================================================================
                                                 Models
==============================================================================================================
"""

class Status(Enum):
    APPLYING = 1
    FIRST_INTERVIEW = 2
    SECOND_INTERVIEW = 3
    ACCEPTED = 4
    REJECTED = 5
    CANCELLED = 6

class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.String(45), nullable=False)
    company = db.Column(db.String(45), nullable=False)
    applied_time = db.Column(db.Date, nullable=False)
    password = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(45), nullable=False)

"""
==============================================================================================================
                                            Data Access Level     
==============================================================================================================
"""

def queryWithCondition(order_attr, order_type, filter_status):
    map_dict = {'title': Jobs.title,
                'company': Jobs.company,
                'applied_time': Jobs.applied_time
                }

    result = db.session.query(Jobs)
    if filter_status != 'null':
        result = result.filter_by(status=filter_status)

    if order_attr != 'null':
        if order_type == 'asc':
            return result.order_by(map_dict[order_attr].asc())

        if order_type == 'desc':
            return result.order_by(map_dict[order_attr].desc())

    return result.order_by(map_dict['applied_time'].desc())


def insertRecord(jobs_json):
    before_count = Jobs.query.count()
    job_list = []
    for job in jobs_json:
        title = job['title']
        company = job['company']
        applied_time = job['applied_time']
        status = job['status']
        job = Jobs(title=title, company=company, applied_time=applied_time, status=status)
        job_list.append(job)

    db.session.add_all(job_list)
    db.session.commit()

    end_count = Jobs.query.count()
    return end_count - before_count


def updateStatus(item_id, new_status):
    db.session.query(Jobs).filter_by(id=item_id).update({'status': new_status})
    db.session.commit()

def deleteRecord(item_id):

    job = db.session.query(Jobs).filter(Jobs.id == item_id).first()
    db.session.delete(job)
    db.session.commit()

"""
==============================================================================================================
                                                Routes     
==============================================================================================================
"""

@app.route('/', methods=['GET'])
def queryAll():
    filterStatus = request.args.get('filterStatus')
    orderAttr = request.args.get('orderAttr')
    orderType = request.args.get('orderType')

    result = queryWithCondition(orderAttr, orderType, filterStatus)
    init_list = []
    for job in result:
        init_list.append({'id': job.id,
                          'title': job.title,
                          'company': job.company,
                          'applied_time': job.applied_time.strftime("%d/%m/%Y"),
                          'status': job.status})
    return jsonify(init_list)


@app.route('/insert', methods=['POST'])
@cross_origin(origin='http://localhost:3000', headers=['Content-Type'])
def insert_application():
    try:
        data = request.get_json()
        diff = insertRecord(data)
        return jsonify({'message': 'success', 'diff': diff}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/update_status', methods=['POST'])
@cross_origin(origin='http://localhost:3000', headers=['Content-Type'])
def update_status():
    try:
        data = request.get_json()
        item_id = data.get('itemId')
        new_status = data.get('newStatus')

        updateStatus(item_id, new_status)

        return jsonify({'message': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/delete', methods=['POST'])
@cross_origin(origin='http://localhost:3000', headers=['Content-Type'])
def delete_record():
    try:
        data = request.get_json()
        item_id = data.get('record_id')
        deleteRecord(item_id)

        return jsonify({'message': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

"""
==============================================================================================================
                                                  Init     
==============================================================================================================
"""
if __name__ == '__main__':
    app.run(debug=True)



