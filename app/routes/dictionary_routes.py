from flask import Blueprint, jsonify, request
from app import db
from app.models import Dictionary, User

dictionary_bp = Blueprint('dictionary_bp', __name__)

@dictionary_bp.route('/add_dictionary', methods=['POST'])
def add_dictionary():
    data = request.get_json()
    id_user = data.get('id_user')
    id_word = data.get('id_word')

    # Verificar que el usuario exista
    usuario = User.query.filter_by(id=id_user).first()
    if not usuario:
        return jsonify({"message": "User not found"}), 404

    # Crear una nueva entrada en el diccionario
    new_entry = Dictionary(
        id_user=id_user,
        id_word=id_word
    )

    try:
        db.session.add(new_entry)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error al guardar en la base de datos: {e}")
        return jsonify({"message": "Error al guardar en la base de datos"}), 500

    return jsonify({"message": "Word added to dictionary successfully"}), 200

@dictionary_bp.route('/remove_dictionary', methods=['DELETE'])
def remove_dictionary():
    id_user = request.form.get('id_user')
    id_word = request.form.get('id_word')

    # Verificar que la entrada exista
    entry = Dictionary.query.filter_by(id_user=id_user, id_word=id_word).first()
    if not entry:
        return jsonify({"message": "Entry not found"}), 404

    # Eliminar la entrada del diccionario
    db.session.delete(entry)
    db.session.commit()

    return jsonify({"message": "Word removed from dictionary successfully"}), 200

@dictionary_bp.route('/get_dictionary', methods=['POST'])
def get_dictionary():
    data = request.get_json()
    id_user = data.get('id_user')

    # Verificar que el usuario exista
    usuario = User.query.filter_by(id=id_user).first()
    if not usuario:
        return jsonify({"message": "User not found"}), 404

    # Obtener todas las palabras del diccionario para el usuario
    words = Dictionary.query.filter_by(id_user=id_user).all()

    # Formatear las palabras en una lista de JSON
    word_list = [{"id_word": word.id_word} for word in words]

    return jsonify({"words": word_list}), 200
