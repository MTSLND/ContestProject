from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from flask_login import login_required, current_user
from .models import User, Votos
from sqlalchemy.sql import func
from . import db

views = Blueprint('views',__name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        grupo = request.form.get('grupo')

        if 'votou' in request.cookies:
            #Verifica nos cookies se a pessoa já votou
            flash('Você já votou. Somente um voto permitido por pessoa.', 'error')
            return redirect(url_for('views.resultado'))
        voto = Votos.query.filter_by(user_id=current_user.id).first()
        if voto:
            #Verifica pelo email se a pessoa ja votou
            flash('Somente um Voto Permitido por Pessoa', 'error')
            return redirect(url_for('views.resultado'))
        elif grupo == 'grupo1':
            voto = 1
        elif grupo == 'grupo2':
            voto = 2
        elif grupo == 'grupo3':
            voto = 3
        elif grupo == 'grupo4':
            voto = 4
        else:
            flash('Grupo inválido', 'error')
            return redirect(url_for('views.home'))

        new_voto = Votos(grupo=voto, user_id=current_user.id)
        db.session.add(new_voto)
        db.session.commit()

        response = make_response(redirect(url_for('views.resultado')))
        response.set_cookie('votou', '1')

        return response

    return render_template("home.html", user=current_user)

@views.route('/resultado')
def resultado():
    
    total_votos = Votos.query.count()
    contagem_por_grupo = Votos.query.with_entities(Votos.grupo, func.count().label('count')).group_by(Votos.grupo).all()
    usuarios = User.query.all()
    
    return render_template("resultado.html", user=current_user, total_votos=total_votos, contagem_por_grupo=contagem_por_grupo)