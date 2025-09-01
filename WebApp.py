import html
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from models import db, Note, NoteHistory
import config
from contact import contact_bp
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.register_blueprint(contact_bp)

db_secret_id=os.getenv("DB_SECRET_ID")
sendgrid_secret_id=os.getenv("SENDGRID_SECRET_ID")
DBConn=os.getenv("DB_WEBAPP_CONN")
app.secret_key = os.getenv("FLASK_SECRET_KEY")

db_secrets=config.get_secret(db_secret_id)
sendgrid_secrets=config.get_secret(sendgrid_secret_id)


app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_secrets['username']}:{db_secrets['password']}@{DBConn}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["sendgrid_key"] = sendgrid_secrets["SENDGRID_API_KEY"]

db.init_app(app)

with app.app_context():
    db.create_all()

def sanitize_input(text:str) -> str:
     if not text:
          return ""
     return html.escape(text.strip())

def obfuscate_name(name: str) -> str:
     if not name:
          return ""
     if len(name) <=2:
          return name[0] + "*"
     return name [0] + "*" * (len(name)-2) + name[-1]

@app.route("/")
def home():
    all_notes=Note.query.filter_by(active=True).all()
    return render_template("index.html", notes=all_notes)

@app.route("/notes", methods=["POST"])
def notes():
        nickname = sanitize_input(request.form.get("nickname"))
        content = sanitize_input(request.form.get("content"))
        if not nickname or not content:
             abort(400, "Nickname and content are required")

        new_note=Note(nickname=nickname, content=content)
        db.session.add(new_note)
        db.session.flush()

        history=NoteHistory(
            note_id=new_note.id,
            version=1,
            nickname=new_note.nickname,
            content=new_note.content,
            )
        db.session.add(history)
        db.session.commit()
        return redirect(url_for("home"))


#Delete
@app.route("/delete/<int:note_id>", methods=["POST"])
def delete(note_id):
    note = Note.query.get_or_404(note_id)
    nickname=sanitize_input(request.form.get("nickname"))
    if nickname != note.nickname:
         abort(403, "You can only delete your own note")

    note.active = False
    db.session.flush()

    version = NoteHistory.query.filter_by(note_id=note.id).count() + 1
    history = NoteHistory(
         note_id=note.id,
         version=version,
         nickname=note.nickname,
         content=f"[DELETED] {note.content}"
    )
    db.session.add(history)
    db.session.commit()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
         return jsonify({"success": True})
    return redirect(url_for("home"))


#Edit 
@app.route("/edit/<int:note_id>", methods=["POST"])
def edit(note_id):
    note = Note.query.get_or_404(note_id)
    new_content = sanitize_input(request.form.get("content"))
    nickname=sanitize_input(request.form.get("nickname"))
    if nickname != note.nickname:
         abort(403, "You can only edit your own note")

    if not new_content:
         abort(400, "Content is required")

    note.content = new_content
    db.session.flush()

    version= NoteHistory.query.filter_by(note_id=note.id).count() + 1
    history= NoteHistory(
         note_id=note.id,
         version=version,
         nickname=note.nickname,
         content=new_content
    )
    db.session.add(history)
    db.session.commit()

    # IF AJAX req, return JSON
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
         return jsonify({"success": True, "new_content": note.content})
    
    return redirect(url_for("home"))

app.jinja_env.globals.update(obfuscate_name=obfuscate_name)


if __name__ == "__main__":
    app.run(debug=True, port=5000)


