from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Create Flask app
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)

# Define Note model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    type = db.Column(db.String(10))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'type': self.type
        }

# Route for the root URL ("/")
@app.route('/')
def index():
    return 'Welcome to the Notes App'

# API endpoints
@app.route('/api/notes', methods=['POST'])
def create_note():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    type_ = data.get('type')

    # Create a new note
    note = Note(title=title, content=content, type=type_)
    db.session.add(note)
    db.session.commit()

    # Return the created note
    return jsonify(note.to_dict()), 201

@app.route('/api/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    # Retrieve the note from the database
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'error': 'Note not found'}), 404

    # Return the retrieved note
    return jsonify(note.to_dict())

@app.route('/api/notes', methods=['GET'])
def get_all_notes():
    # Retrieve all notes from the database
    notes = Note.query.all()

    # Return the list of notes
    return jsonify([note.to_dict() for note in notes])

# Create the database tables (run this once before the first use)
with app.app_context():
    db.create_all()

# Start the server
if __name__ == '__main__':
    app.run(debug=True)
