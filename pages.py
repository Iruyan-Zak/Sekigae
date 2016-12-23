from flask import render_template, redirect, request, url_for, abort
import ast
from Sekigae import app, db
from models import *


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')

    print(request.form)
    rows = request.form['rows']
    columns = request.form['columns']
    unused_seats = request.form['unused_seats']
    positions = request.form['positions']

    # try:
    rows = int(rows)
    columns = int(columns)
    positions = (l for l in positions.splitlines() if l)
    unused_seats = ast.literal_eval(unused_seats)
    room = Room(rows, columns)
    db.session.add(room)
    db.session.commit()

    for i in range(0, rows * columns):
        if i not in unused_seats:
            person = Person(i, next(positions), room.id)
            db.session.add(person)

    db.session.commit()
    # except:
    #     return redirect('/create')
    print("OK.")

    return redirect(url_for('rooms', room_id=room.id))


@app.route('/rooms/<room_id>', methods=['GET', 'POST'])
def rooms(room_id):
    if request.method == 'POST':
        return post_rooms(room_id)
    return get_rooms(room_id)


def post_rooms(room_id):
    print(request.form)
    op = request.form['command']
    pos1_name = request.form['pos1']
    pos2_name = request.form['pos2']

    # try
    if pos1_name == pos2_name:
        abort(400)

    pos2 = Person.query.filter_by(room_id=room_id).filter_by(name=pos2_name).first()
    if not pos2:
        abort(400)

    if op == "decline":
        pos1_name = ""
    else:
        pos1 = Person.query.filter_by(room_id=room_id).filter_by(name=pos1_name).first()
        if not pos1:
            abort(400)

    cmd = Command(room_id, post_rooms.cmd_num[op], pos1_name, pos2_name)
    db.session.add(cmd)
    db.session.commit()
    return redirect(url_for('rooms', room_id=room_id))


post_rooms.cmd_num = {"change": 0, "request": 1, "decline": 2}


def get_rooms(room_id):
    room = Room.query.filter_by(id=room_id).first()

    persons = Person.query.filter_by(room_id=room_id).all()
    persons = sorted(persons, key=lambda p: p.index)
    l = []
    for i in range(0, room.rows*room.columns):
        if persons and i == persons[0].index:
            print(persons[0].name)
            l.append(persons.pop(0).name)
        else:
            l.append("Fail")
    commands = Command.query.filter_by(room_id=room_id).all()
    for c in commands:
        c.op = get_rooms.cmd[c.op]

    return render_template("rooms.html", room=room, seats=l, commands=commands)


get_rooms.cmd = ["change", "request", "decline"]
