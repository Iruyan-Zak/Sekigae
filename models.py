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

    def __repr__(self):
        return "{0}-{1}: [{2}] {3}".format(self.room_id, self.id, self.index, self.name)


class Command(db.Model):
    CHANGE = 1
    REQUEST = 2
    DECLINE = 3
    from_op = {CHANGE: "change", REQUEST: "request", DECLINE: "decline"}
    to_op = {"change": CHANGE, "request": REQUEST, "decline": DECLINE}

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    op = db.Column(db.Integer)
    pos1 = db.Column(db.String(32))
    pos2 = db.Column(db.String(32))
    available = db.Column(db.Boolean)

    def __init__(self, room_id, op, pos1, pos2, available):
        self.room_id = room_id
        self.op = op
        self.pos1 = pos1
        self.pos2 = pos2
        self.available = available

    def __repr__(self):
        s = "{0}: {1} {2} {3}".format(self.id, self.from_op[self.op], self.pos1, self.pos2)
        if self.available:
            s += " *"
        return s
