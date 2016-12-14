from flask import Flask, render_template, redirect, request, url_for, abort
from flask_sqlalchemy import SQLAlchemy
import ast

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
db.create_all()


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rows = db.Column(db.Integer)
    columns = db.Column(db.Integer)
    unused_seats = db.Column(db.PickleType)
#     seats = db.relationship('seat', backref='room')
    commands = db.relationship('Command', backref='room')

    def __init__(self, rows, columns, unused_seats):
        self.rows = rows
        self.columns = columns
        self.unused_seats = unused_seats


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
#     seat_id = db.Column(db.Integer, db.ForeignKey('seat.id'))
    index = db.Column(db.Integer)
    name = db.Column(db.String(32))

    def __init__(self, index, name):
        self.index = index
        self.name = name


class Command(db.Model):
    CHANGE = 1
    REQUEST = 2
    DECLINE = 3

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    op = db.Column(db.Integer)
    person1 = db.relationship('Person', backref='command', uselist=False)
    person2 = db.relationship('Person', backref='command', uselist=False)


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
    abort(404)
    # 下の行で 400 Bad request が出る。
    unused_seats = request.form['unused_seats']
    positions = request.form['positions']

    # try:
    rows = int(rows)
    columns = int(columns)
    positions = iter(positions.split('\n'))
    unused_seats = ast.literal_eval(unused_seats)
    room = Room(rows, columns, unused_seats)
    db.session.add(room)
    for i in range(0, rows * columns):
        if i not in unused_seats:
            # seat = Seat(i)
            # seat.room_id = room.id
            person = Person(i, next(positions))
            person.room_id = room.id
            db.session.add(person)
            # db.session.add(seat)

    db.session.commit()
    # except:
    #     return redirect('/create')

    return redirect(url_for('/rooms/{0}'.format(room.id)))


@app.route('/rooms/<room_id>')
def rooms(room_id):
    room = Room.query.filter_by(id=room_id).first()
    persons = Person.query.filter_by(room_id=room.id).all().sort(lambda p: p.index)
    return render_template("rooms.html", room=room, persons=persons)

if __name__ == '__main__':
    app.run()
