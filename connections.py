from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from services import t_esp_map, t_ing_esp, tts_map


application = Flask(__name__)
application.config['JSON_AS_ASCII'] = False
cors = CORS(application, resources={r"/translator/*": {"origins": "*"}})
application.config['CORS_HEADERS'] = 'Content-Type'


@application.route('/translator', methods=['GET'])
def mensaje():
    return jsonify('Conectado a servicio')

@application.route('/translator/ingesp', methods=['POST'])
@cross_origin(origin='*')
def ingEsp():
    args = request.get_json(silent=True)
    return jsonify(t_ing_esp(args))


@application.route('/translator/espmap', methods=['POST'])
@cross_origin(origin='*')
def espMap():
    args = request.get_json(silent=True)
    return jsonify(t_esp_map(args))

@application.route('/translator/ttsmap', methods=['POST'])
@cross_origin(origin='*')
def ttsMap():
    args = request.get_json(silent=True)
    return jsonify(tts_map(args))


if __name__ == '__main__':
    application.run(debug=True)
