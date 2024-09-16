from flask import Blueprint, jsonify, request
from app import db
from app.models import Traduccion, User

traduction_bp = Blueprint('traduction_bp', __name__)

@traduction_bp.route('/send_traduction', methods=['POST'])
def send_traduction():
    data = request.get_json()
    id_user = data.get('id_user')
    sentence_lensegua = data.get('sentence_lensegua')

    # Verificar que el usuario exista
    usuario = User.query.filter_by(id=id_user).first()
    if not usuario:
        return jsonify({"message": "User not found"}), 404
    
    # Verificar que se ha proporcionado la frase en lensegua
    if not sentence_lensegua:
        return jsonify({"message": "sentence_lensegua is required"}), 400
    
    # Traducir la frase a español
    traduccion_esp = sentence_lensegua[::-1]

    new_traduction = Traduccion(
        id_user=id_user,
        traduction_esp=traduccion_esp
    )

    db.session.add(new_traduction)
    db.session.commit()

    return jsonify(
        {   
            "message": "Traduction added successfully", 
            "traduction_id": new_traduction.id, 
            "traduction_esp": new_traduction.traduction_esp
        }
    ), 200

@traduction_bp.route('/fav_traduction', methods=['POST'])
def fav_traduction():
    data = request.get_json()
    id_user = data.get('id_user')
    id_sentence = data.get('id_sentence')

    # Verificar que la traducción exista y pertenezca al usuario
    traduction = Traduccion.query.filter_by(id=id_sentence, id_user=id_user).first()
    if not traduction:
        return jsonify({"message": "Traduction not found or does not belong to the user"}), 404

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
        return jsonify({"message": "Traduction not found"}), 404

    # Eliminar la traducción
    db.session.delete(traduction)
    db.session.commit()

    return jsonify({"message": "Traduction removed successfully"}), 200
