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
        return jsonify({"message": "Usuario no encontrado"}), 404
    
    # Verificar que se ha proporcionado la frase en lensegua
    if not sentence_lensegua:
        return jsonify({"message": "Frase en lensegua es requerida"}), 400
    
    # Traducir la frase a español
    traduccion_esp = sentence_lensegua + "traduccion ESP"

    new_traduction = Traduccion(
        id_user=id_user,
        sentence_lensegua=sentence_lensegua,
        traduction_esp=traduccion_esp,
        is_favorite=False
    )

    db.session.add(new_traduction)
    db.session.commit()

    return jsonify(
        {
            "id_sentence": new_traduction.id, 
            "traduction_esp": new_traduction.traduction_esp
        }
    ), 200

@traduction_bp.route('/fav_traduction', methods=['POST'])
def fav_traduction():
    data = request.get_json()
    id_user = data.get('id_user')
    id_sentence = data.get('id_sentence')

    usuario = User.query.filter_by(id=id_user).first()
    if not usuario:
        return jsonify({"message": "Usuario no encontrado"}), 404

    # Verificar que la traducción exista y pertenezca al usuario
    traduction = Traduccion.query.filter_by(id=id_sentence, id_user=id_user).first()
    if not traduction:
        return jsonify({"message": "La traduccion no existe o no le pertenece al usuario"}), 404

    # Marcar la traducción como favorita
    traduction.is_favorite = True
    db.session.commit()

    return jsonify({"message": "Traduccion desmarcada como favorita"}), 200

@traduction_bp.route('/remove_fav_traduction', methods=['POST'])
def remove_fav_traduction():
    data = request.get_json()
    id_user = data.get('id_user')
    id_sentence = data.get('id_sentence')

    usuario = User.query.filter_by(id=id_user).first()
    if not usuario:
        return jsonify({"message": "Usuario no encontrado"}), 404

    # Verificar que la traducción exista y pertenezca al usuario
    traduction = Traduccion.query.filter_by(id=id_sentence, id_user=id_user).first()
    if not traduction:
        return jsonify({"message": "La traduccion no existe o no le pertenece al usuario"}), 404

    # Marcar la traducción como favorita
    traduction.is_favorite = False
    db.session.commit()

    return jsonify({"message": "Traduccion marcada como favorita"}), 200

@traduction_bp.route('/remove_traduction', methods=['DELETE'])
def remove_traduction():
    id_sentence = request.args.get('id_sentence')

    # Verificar que la traducción exista
    traduction = Traduccion.query.filter_by(id=id_sentence).first()
    if not traduction:
        return jsonify({"message": "Traduccion no encontrada"}), 404

    # Eliminar la traducción
    db.session.delete(traduction)
    db.session.commit()

    return jsonify({"message": "Traduccion borrada con exito"}), 200
