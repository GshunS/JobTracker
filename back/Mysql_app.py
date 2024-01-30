from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import pymysql
import re
from flask_cors import CORS, cross_origin
from datetime import datetime, date
from enum import Enum

pymysql.install_as_MySQLdb()
app = Flask(__name__)
CORS(app)

class Status(Enum):
    APPLYING = 1
    FIRST_INTERVIEW = 2
    SECOND_INTERVIEW = 3
    ACCEPTED = 4
    REJECTED = 5
    CANCELLED = 6

class Config(object):
    """配置参数"""
    # 设置连接数据库的URL
    user = 'root'
    password = 'admin123'
    database = 'Kiwi'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@127.0.0.1:3306/%s' % (user, password, database)

    # 设置sqlalchemy自动更跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 查询时会显示原始SQL语句
    app.config['SQLALCHEMY_ECHO'] = True

    # 禁止自动提交数据处理
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False

# 读取配置
app.config.from_object(Config)

# 创建数据库sqlalchemy工具对象
db = SQLAlchemy(app)

class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.String(45), nullable=False)
    company = db.Column(db.String(45), nullable=False)
    applied_time = db.Column(db.Date, nullable=False)
    password = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(45), nullable=False)

def insertOne(title, company, applied_time, status, password=''):
    job = Jobs(title=title, company=company, applied_time=applied_time, status=status, password=password)
    db.session.add(job)
    db.session.commit()

def insertFromFile(filename):
    with open(filename) as f:
        lines = f.readlines()
    f.close()

    pattern_normal = r"(.+?)\s+-+\s+(.+?)\s+-+\s+(\d{2}/\d{2}/\d{4})"
    pattern_password = r'^(.+?)\s*[-]+?\s*(.+?)\s*[-]+?\s*(\d{2}/\d{2}/\d{4})\s*[-]+?\s*(@\w+\.)$'
    password_flag = False
    job_list = []

    for line in lines:
        line = line.strip()
        if line == '':
            continue
        if line[-4:] == '2024':
            password_flag = False
            match = re.match(pattern_normal, line)
        else:
            password_flag = True
            match = re.match(pattern_password, line)

        title = match.group(1).strip()
        company = match.group(2).strip()
        applied_time = datetime.strptime(match.group(3).strip(), '%d/%m/%Y')
        password = ''
        if password_flag:
            password = match.group(4).strip()

        job = Jobs(title=title, company=company, applied_time=applied_time, password=password)
        job_list.append(job)

    db.session.add_all(job_list)
    db.session.commit()

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
            result = result.order_by(map_dict[order_attr].asc())

        if order_type == 'desc':
            result = result.order_by(map_dict[order_attr].desc())

    return result.order_by(map_dict['applied_time'].desc())

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

@app.route('/update_status', methods=['POST'])
@cross_origin(origin='http://localhost:3000', headers=['Content-Type'])
def update_status():
    try:
        data = request.get_json()
        item_id = data.get('itemId')
        new_status = data.get('newStatus')

        update(item_id, new_status)

        return jsonify({'message': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def update(item_id, new_status):
    db.session.query(Jobs).filter_by(id=item_id).update({'status': new_status})
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
    # with app.app_context():
    #     db.session.query(Jobs).filter_by(id=2).update({'status': 'APPLYING'})
    #     db.session.commit()

        ### insert one
        # title = 'Data Scientist'
        # company = '40 Foot'
        # # applied_time = datetime.strptime('15/01/2024', '%d/%m/%Y')
        # applied_time = date.today()
        # status = Status.APPLYING.name
        # password = ''
        # insertOne(title, company, applied_time, status, password)
        # result = db.session.query(Jobs).filter_by(status=None)

        # result = Jobs.query.all()
        # for r in result:
            # print(f'\n{r.title} - {r.company} - {r.applied_time} - {r.status}\n')

        ### delete one
        # db.session.delete(Jobs.query.filter_by(id=1).first())
        # db.session.commit()



