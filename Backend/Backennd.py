from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from models import db , User
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '123456789'  

bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "*"}}) 

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    walletAddress = data['walletAddress']
    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=username, password=password , walletAddress=walletAddress)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    walletAddress = User.query.filter_by(walletAddress=data['walletAddress']).first()
    if user and walletAddress and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@app.route('/all-users' , methods=["GET"])
def allUsersList():
    users = User.query.all()
    users_list = []
    for user in users:
        users_list.append({
            "id": user.id,
            "username": user.username,
            "walletAddress": user.walletAddress,
            "startdate": user.startdate,
            "enddate": user.enddate,
            "cycles": user.cycles
        })
    return jsonify(users_list)


@app.route('/set-dates', methods=['POST'])
def setDates():
    data = request.json
    username = data.get('username')
    startdate = data.get('startdate')
    enddate = data.get('enddate')  
    cycles = data.get('cycles')
    user = User.query.filter_by(username=username).first() 
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.startdate = datetime.strptime(startdate, '%Y-%m-%d').date() if startdate else None
    user.enddate = datetime.strptime(enddate, '%Y-%m-%d').date() if enddate else None

    if cycles is not None:
        user.cycles = cycles
    else:
        user.calculate_cycles()

    db.session.commit()
    return jsonify({"message": "User dates updated successfully", "cycles": user.cycles}), 200



if __name__ == "__main__":
    app.run(debug=True)