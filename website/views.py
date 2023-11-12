from flask import Blueprint, render_template, request, flash, redirect, url_for
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
        voto = Votos.query.filter_by(user_id=current_user.id).first()
        if voto:
            flash('Somente um Voto Permitido Pessoa', 'error')
            return redirect(url_for('views.votacao'))
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
        flash('Voto Contabilizado com Sucesso', 'success')
        return redirect(url_for('views.votacao'))

    return render_template("home.html", user=current_user)

@views.route('/votacao')
def votacao():
    
    total_votos = Votos.query.count()
    contagem_por_grupo = Votos.query.with_entities(Votos.grupo, func.count().label('count')).group_by(Votos.grupo).all()
    porcentagens = {}
    for grupo, contagem in contagem_por_grupo:
        porcentagem = (contagem / total_votos) * 100
        porcentagens[grupo] = porcentagem
    usuarios = User.query.all()

    return render_template("votacao.html", user=current_user, total_votos=total_votos, contagem_por_grupo=contagem_por_grupo, porcentagem = porcentagem)