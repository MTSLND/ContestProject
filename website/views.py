from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Votos
from . import db

views = Blueprint('views',__name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        grupo = request.form.get('grupo')
        voto = Votos.query.filter_by(user_id=current_user.id).first()
        if voto:
            flash('Somente um Voto por Pessoa Permitido', 'error')
            return redirect(url_for('views.home'))
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

    return render_template("home.html", user=current_user)