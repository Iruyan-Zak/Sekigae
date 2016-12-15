from flask import Flask, render_template, redirect, request, url_for, abort
from flask_sqlalchemy import SQLAlchemy
import ast

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rows = db.Column(db.Integer)
    columns = db.Column(db.Integer)
    # unused_seats = db.Column(db.PickleType)
    # persons = db.relationship('Person', backref='room')
    # commands = db.relationship('Command', backref='room')

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        # self.persons = []
        # self.commands = []
        # self.unused_seats = unused_seats


# class Seat(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
#     index = db.Column(db.Integer)
#     person = db.relationship('Person', backref='seat', uselist=False)
#
#     def __init__(self, index):
#         self.index = index

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer)
    name = db.Column(db.String(32))
    room_id = db.Column(db.Integer)  # , db.ForeignKey('room.id'))

    def __init__(self, index, name, room_id):
        self.index = index
        self.name = name
        self.room_id = room_id


class Command(db.Model):
    CHANGE = 1
    REQUEST = 2
    DECLINE = 3

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    op = db.Column(db.Integer)
    pos1 = db.Column(db.Integer)
    pos2 = db.Column(db.Integer)


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
    positions = iter(positions.split('\n'))
    unused_seats = ast.literal_eval(unused_seats)
    room = Room(rows, columns)
    db.session.add(room)
    db.session.commit()

    for i in range(0, rows * columns):
        if i not in unused_seats:
            # seat = Seat(i)
            # seat.room_id = room.id
            person = Person(i, next(positions), room.id)
            # person.room_id = room.id
            # room.persons.append(person)
            db.session.add(person)
            # db.session.add(seat)

    db.session.commit()
    # except:
    #     return redirect('/create')
    print("OK.")

    return redirect(url_for('rooms', room_id=room.id))


@app.route('/rooms/<room_id>')
def rooms(room_id):
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
    return render_template("rooms.html", room=room, seats=l)

if __name__ == '__main__':
    db.create_all()
    app.run()
