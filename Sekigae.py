from flask import Flask, render_template, redirect, request, url_for
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
    seats = db.relationship('seat', backref='room')
    commands = db.relationship('Command', backref='room')

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns


class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    person = db.relationship('Person', backref='seat', uselist=False)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seat_id = db.Column(db.Integer, db.ForeignKey('seat.id'))
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

    width = request.form['width']
    height = request.form['height']
    unused_seats = request.form['unused_seats']
    positions = request.form['positions']

    # try:
    width = int(width)
    height = int(height)
    positions = iter(positions.split('\n'))
    unused_seats = ast.literal_eval(unused_seats)
    room = Room(width, height)
    db.session.add(room)
    for i in range(0, width * height):
        if i not in unused_seats:
            seat = Seat()
            seat.room_id = room.id
            person = Person(i, next(positions))
            person.seat_id = seat.id
            db.session.add(person)
            db.session.add(seat)

    db.session.commit()
    # except:
    #     return redirect('/create')

    return redirect(url_for('/{0}'.format(room.id)))


@app.route('/rooms/<room_id>')
def rooms(room_id):
    Room.query.filter_by(id=room_id).first()

if __name__ == '__main__':
    app.run()
