import numpy
from flask import render_template, request

import pandas as pd
from flask_login import login_required
from apps.api.students import blueprint


@blueprint.route('/students', methods=['GET'])
@login_required
def students():
    code = request.args.get('code')

    df = pd.read_csv('advanced_python.csv', sep=';')
    if code:
        df = df[df['student code'] == code]

    records_student = []
    for data in df.values:
        data_student = {}
        data_student['code'] = data[1]
        data_student['first_name'] = data[2]
        data_student['last_name'] = data[3]
        data_student['dob'] = data[4]
        data_student['major'] = data[4].replace(' ', '')

        records_student.append(data_student)

    return render_template('students/students.html', student=records_student)


@blueprint.route('/student/chart', methods=['GET'])
@login_required
def student_chart():
    df = pd.read_csv('advanced_python.csv', sep=';')

    birthday = df['DOB'].values

    list_dob = []
    for data in birthday:
        list_dob.append(data[-4:])

    data = numpy.array(list_dob)
    unique, counts = numpy.unique(data, return_counts=True)

    data_return = dict(zip(unique, counts))
    key_data = data_return.keys()

    return render_template('home/charts-morris.html', keys=key_data, data=data_return)
