from flask import Flask, request, jsonify
from models.refeicao import Refeicao
from models.User import User
from database import db
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/login', methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if username and password:
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            print(current_user)
            return jsonify({"message": "Credenciais enviadas com sucesso!"})
    return jsonify({"message": "Credênciais inválidas."}), 400


@app.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso."})

@app.route('/cadastrar', methods=["POST"])
@login_required
def add_refeicao():
    data = request.json
    descricao = data.get("descricao")
    data_hora_str = data.get("data_hora")
    data_hora = datetime.strptime(data_hora_str, '%d-%m-%y %H:%M')
    dieta = data.get("dieta")
    
    if descricao and data_hora and dieta is not None:
        refeicao = Refeicao(nome=current_user,
                            descricao=descricao, 
                            data_hora=data_hora,
                             dieta=dieta)
        refeicao = Refeicao(nome=current_user.username, descricao=descricao, data_hora=data_hora, dieta=dieta)
        db.session.add(refeicao)
        db.session.commit()
        return jsonify({"message": "Refeição adicionada com sucesso!"})
    return jsonify({"message": "Dados inválidos"}), 401


if __name__ == "__main__":
    app.run(debug=True)