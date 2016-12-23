from Sekigae import db


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rows = db.Column(db.Integer)
    columns = db.Column(db.Integer)

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer)
    name = db.Column(db.String(32))
    room_id = db.Column(db.Integer)

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
    pos1 = db.Column(db.String(32))
    pos2 = db.Column(db.String(32))

    def __init__(self, room_id, op, pos1, pos2):
        self.room_id = room_id
        self.op = op
        self.pos1 = pos1
        self.pos2 = pos2
