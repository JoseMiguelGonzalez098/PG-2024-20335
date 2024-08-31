from flask import Blueprint, jsonify, request
from app import db
from app.models import Traduccion, User

traduction_bp = Blueprint('traduction_bp', __name__)

@traduction_bp.route('/send_traduction', methods=['POST'])
def send_traduction():
    id_user = request.form.get('id_user')
    sentence_lensegua = request.form.get('sentence_lensegua')
    traduction_esp = request.form.get('traduction_esp')

    # Verificar que el usuario exista
    usuario = User.query.filter_by(id=id_user).first()
    if not usuario:
        return jsonify({"error": "User not found"}), 404

    # Verificar que se han proporcionado ambas traducciones
    if not sentence_lensegua or not traduction_esp:
        return jsonify({"error": "Both sentence_lensegua and traduction_esp are required"}), 400

    # Crear una nueva traducción
    new_traduction = Traduccion(
        id_user=id_user,
        sentence_lensegua=sentence_lensegua,
        traduction_esp=traduction_esp
    )

    db.session.add(new_traduction)
    db.session.commit()

    return jsonify({"message": "Traduction added successfully", "traduction_id": new_traduction.id}), 200

@traduction_bp.route('/fav_traduction', methods=['POST'])
def fav_traduction():
    id_user = request.form.get('id_user')
    id_sentence = request.form.get('id_sentence')

    # Verificar que la traducción exista y pertenezca al usuario
    traduction = Traduccion.query.filter_by(id=id_sentence, id_user=id_user).first()
    if not traduction:
        return jsonify({"error": "Traduction not found or does not belong to the user"}), 404

    # Marcar la traducción como favorita
    traduction.favoritos = True
    db.session.commit()

    return jsonify({"message": "Traduction marked as favorite"}), 200

@traduction_bp.route('/remove_traduction', methods=['DELETE'])
def remove_traduction():
    id_sentence = request.form.get('id_sentence')

    # Verificar que la traducción exista
    traduction = Traduccion.query.filter_by(id=id_sentence).first()
    if not traduction:
        return jsonify({"error": "Traduction not found"}), 404

    # Eliminar la traducción
    db.session.delete(traduction)
    db.session.commit()

    return jsonify({"message": "Traduction removed successfully"}), 200
