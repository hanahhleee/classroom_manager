from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

association_table1 = db.Table(
    "association1",
    db.Column("course_id", db.Integer, db.ForeignKey("course.id")),
    db.Column("instructor_id", db.Integer, db.ForeignKey("user.id"))
)

association_table2 = db.Table(
    "association2",
    db.Column("course_id", db.Integer, db.ForeignKey("course.id")),
    db.Column("student_id", db.Integer, db.ForeignKey("user.id"))
)


class Course(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    assignments = db.relationship("Assignment", cascade="delete")
    instructors = db.relationship(
        "User", secondary=association_table1, back_populates="courses1")
    students = db.relationship(
        "User", secondary=association_table2, back_populates="courses2")

    def __init__(self, **kwargs):
        self.code = kwargs.get("code")
        self.name = kwargs.get("name")

    def serialize(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "assignments": [a.serialize() for a in self.assignments],
            "instructors": [i.serialize() for i in self.instructors],
            "students": [s.serialize() for s in self.students]
        }

    def serializeSome(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "assignments": [a.subserialize() for a in self.assignments],
            "instructors": [i.subserialize() for i in self.instructors],
            "students": [s.subserialize() for s in self.students]
        }

    def subserialize(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name
        }


class Assignment(db.Model):
    __tablename__ = "assignment"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    due_date = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))

    def __init__(self, **kwargs):
        self.title = kwargs.get("title")
        self.due_date = kwargs.get("due_date")
        self.course_id = kwargs.get("course_id")

    def serialize(self):
        course = Course.query.filter_by(id=self.course_id).first()
        return {
            "id": self.id,
            "title": self.title,
            "due_date": self.due_date,
            "course": [course.subserialize()]
        }

    def subserialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "due_date": self.due_date
        }


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False)
    courses1 = db.relationship(
        "Course", secondary=association_table1, back_populates="instructors")
    courses2 = db.relationship(
        "Course", secondary=association_table2, back_populates="students")

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.netid = kwargs.get("netid")

    def serialize(self):
        icourses = [i.subserialize() for i in self.courses1]
        scourses = [s.subserialize() for s in self.courses2]
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid,
            "courses": icourses+scourses
        }

    def subserialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid
        }
