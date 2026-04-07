from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

# ---------------- BASE MODEL ----------------
class BaseModel(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

# ---------------- USER ----------------
class User(BaseModel):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))

# ---------------- TODOS ----------------
class Todos(BaseModel):
    __tablename__ = "todos"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date)
    completed = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

# ---------------- EVENTS ----------------
class Events(BaseModel):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

# ---------------- NOTES ----------------
class Notes(BaseModel):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

# ---------------- HABITS ----------------
class Habits(BaseModel):
    __tablename__ = "habits"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

# ---------------- GOALS ----------------
class Goals(BaseModel):
    __tablename__ = "goals"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

# ---------------- MOODS ----------------
class Moods(BaseModel):
    __tablename__ = "moods"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

# ---------------- JOURNAL ----------------
class JournalEntries(BaseModel):
    __tablename__ = "journal_entries"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

# ---------------- POSTS ----------------
class Posts(BaseModel):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

# ---------------- COMMENTS ----------------
class Comments(BaseModel):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))

# ---------------- LIKES ----------------
class Likes(BaseModel):
    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))

# ---------------- TAGS ----------------
class Tags(BaseModel):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

# ---------------- TAG ASSOCIATIONS ----------------
class TagAssociations(BaseModel):
    __tablename__ = "tag_associations"

    id = db.Column(db.Integer, primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    note_id = db.Column(db.Integer, db.ForeignKey("notes.id"))
    habit_id = db.Column(db.Integer, db.ForeignKey("habits.id"))
    goal_id = db.Column(db.Integer, db.ForeignKey("goals.id"))

# ---------------- IMAGES ----------------
class Images(BaseModel):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    note_id = db.Column(db.Integer, db.ForeignKey("notes.id"))
    journal_entry_id = db.Column(db.Integer, db.ForeignKey("journal_entries.id"))

# ---------------- VIDEOS ----------------
class Videos(BaseModel):
    __tablename__ = "videos"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    note_id = db.Column(db.Integer, db.ForeignKey("notes.id"))
    journal_entry_id = db.Column(db.Integer, db.ForeignKey("journal_entries.id"))

# ---------------- PROFILE ----------------
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bio = db.Column(db.String(500))
    age = db.Column(db.Integer)

# ---------------- SETTINGS ----------------
class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    theme = db.Column(db.String(50))
    notifications_enabled = db.Column(db.Boolean, default=True)

# ---------------- NOTIFICATIONS ----------------
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    message = db.Column(db.String(255))

# ---------------- FRIENDS ----------------
class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    friend_id = db.Column(db.Integer)