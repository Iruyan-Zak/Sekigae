from flask import render_template, redirect, request, url_for, abort
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
    from util import extract_numbers
    rows = int(rows)
    columns = int(columns)
    positions = (l for l in positions.splitlines() if l)
    unused_seats = extract_numbers(unused_seats)
    room = Room(rows, columns)
    db.session.add(room)
    db.session.flush()

    for i in range(1, rows * columns + 1):
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
    cmd_name = request.form['command']
    pos1_name = request.form['pos1']
    pos2_name = request.form['pos2']

    op = Command.to_op[cmd_name]
    cmd = Command(room_id, op, pos1_name, pos2_name, op != Command.DECLINE)

    if op == Command.DECLINE:
        try:
            request_id = int(pos2_name)
        except ValueError:
            print("Failed to transfer id.")
            abort(400)
            return
        update_count = Command.query.filter_by(op=Command.REQUEST, id=request_id, available=True)\
            .update({'available': False})
        if update_count == 0:
            print("Failed to decline.")
            abort(400)

    else:
        if pos1_name == pos2_name:
            print("Same person's command.")
            abort(400)

        pos1 = Person.query.filter_by(room_id=room_id, name=pos1_name).first()
        pos2 = Person.query.filter_by(room_id=room_id, name=pos2_name).first()
        if not pos1 or not pos2:
            print("Person does not exist.")
            abort(400)

        if op == Command.CHANGE:
            from sqlalchemy import or_
            Command.query.filter_by(op=Command.REQUEST, available=True)\
                .filter(or_(Command.pos1 == pos1_name,
                            Command.pos2 == pos1_name,
                            Command.pos1 == pos2_name,
                            Command.pos2 == pos2_name))\
                .update({'available': False})
            p1_index = pos1.index
            Person.query.filter_by(id=pos1.id).update({'index': pos2.index})
            Person.query.filter_by(id=pos2.id).update({'index': p1_index})

    db.session.add(cmd)
    db.session.commit()
    return redirect(url_for('rooms', room_id=room_id))


def get_rooms(room_id):
    room = Room.query.filter_by(id=room_id).first()

    persons = Person.query.filter_by(room_id=room_id).all()
    persons.sort(key=lambda p: p.index)
    print(persons)
    l = []
    for i in range(1, room.rows * room.columns + 1):
        if persons and i == persons[0].index:
            print(persons[0].name)
            l.append(persons.pop(0).name)
        else:
            l.append("Unused")

    print(list(Command.query.filter_by(available=True).all()))
    commands = Command.query.filter_by(room_id=room_id).all()
    for c in commands:
        c.op = Command.from_op[c.op]

    return render_template("rooms.html", room=room, seats=l, commands=commands)
