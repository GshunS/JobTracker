import re
from datetime import datetime

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

        # job = Jobs(title=title, company=company, applied_time=applied_time, password=password)
        # job_list.append(job)

    # db.session.add_all(job_list)
    # db.session.commit()