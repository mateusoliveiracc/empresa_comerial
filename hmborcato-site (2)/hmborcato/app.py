# -*- coding: utf-8 -*-
"""
H.M. Borçato Representação Comercial e Marketing
Site institucional e comercial - Flask + SQLite

Para rodar:
    pip install -r requirements.txt
    python app.py
Acesse: http://127.0.0.1:5000
"""
import os
import sqlite3
from datetime import datetime
from functools import wraps

from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, session, g, Response
)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "instance", "hmborcato.db")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "troque-esta-chave-em-producao")

# ---------------------------------------------------------------------------
# CONFIGURAÇÕES DA EMPRESA
# Edite os dados abaixo para atualizar as informações em TODO o site de uma vez.
# ---------------------------------------------------------------------------
EMPRESA = {
    "nome": "H.M. Borçato Representação Comercial e Marketing",
    "nome_curto": "H.M. Borçato",
    "slogan": "Representação comercial de autopeças em Minas Gerais",
    "fundacao_ano": 2004,  # ajuste para o ano real de fundação (base para "20+ anos")
    "telefone_exibicao": "(31) 3333-4455",
    "whatsapp_numero": "5531999998888",  # formato internacional, somente dígitos
    "whatsapp_mensagem_padrao": "Olá! Vim pelo site e gostaria de falar com a H.M. Borçato.",
    "email_contato": "contato@hmborcato.com.br",
    "email_comercial": "comercial@hmborcato.com.br",
    "endereco_logradouro": "Av. Exemplo, 1234 - Sala 10",
    "endereco_bairro": "Centro",
    "endereco_cidade": "Belo Horizonte",
    "endereco_estado": "MG",
    "endereco_cep": "30000-000",
    "cnpj": "00.000.000/0001-00",
    "horario_funcionamento": "Segunda a sexta, 8h às 18h",
    "instagram": "https://instagram.com/hmborcato",
    "linkedin": "https://linkedin.com/company/hmborcato",
    "admin_senha": os.environ.get("ADMIN_SENHA", "borcato2026"),
}
EMPRESA["anos_atuacao"] = datetime.now().year - EMPRESA["fundacao_ano"]


# ---------------------------------------------------------------------------
# BANCO DE DADOS
# ---------------------------------------------------------------------------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    os.makedirs(os.path.join(BASE_DIR, "instance"), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS mensagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            empresa TEXT,
            cidade TEXT,
            telefone TEXT NOT NULL,
            email TEXT,
            assunto TEXT,
            mensagem TEXT NOT NULL,
            criado_em TEXT NOT NULL,
            lida INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# DADOS ESTÁTICOS DE CONTEÚDO (fácil de editar / expandir)
# ---------------------------------------------------------------------------
MARCAS_PARCEIRAS = [
    {"nome": "NTN"},
    {"nome": "Filtros Brasil"},
    # Adicione aqui as demais marcas parceiras (nome exatamente como deve aparecer no site)
]

LINHAS_PRODUTOS = [
    {"nome": "Motor", "desc": "Componentes para motor, juntas, retentores e correias dentadas.", "icone": "engine", "img": "piston.png"},
    {"nome": "Freios", "desc": "Pastilhas, discos, cilindros e sistemas completos de frenagem.", "icone": "brake", "img": "brake.png"},
    {"nome": "Suspensão e Direção", "desc": "Amortecedores, molas, terminais e componentes de direção.", "icone": "suspension", "img": "suspension.png"},
    {"nome": "Transmissão", "desc": "Embreagens, homocinéticas e componentes de câmbio.", "icone": "gear"},
    {"nome": "Elétrica e Iluminação", "desc": "Baterias, alternadores, sensores e sistemas de iluminação.", "icone": "bolt"},
    {"nome": "Filtros", "desc": "Filtros de óleo, ar, combustível e cabine para todas as linhas.", "icone": "filter"},
    {"nome": "Arrefecimento", "desc": "Radiadores, mangueiras, bombas d'água e componentes correlatos.", "icone": "coolant"},
    {"nome": "Ar Condicionado", "desc": "Compressores, condensadores e componentes de climatização.", "icone": "ac"},
]

REGIOES_MG = [
    {"nome": "Região Metropolitana de BH", "cidades": "Belo Horizonte, Contagem, Betim, Nova Lima, Sabará", "x": 300, "y": 300},
    {"nome": "Triângulo Mineiro", "cidades": "Uberlândia, Uberaba, Araguari, Patos de Minas", "x": 90, "y": 210},
    {"nome": "Zona da Mata", "cidades": "Juiz de Fora, Muriaé, Ubá, Ponte Nova", "x": 420, "y": 400},
    {"nome": "Sul de Minas", "cidades": "Poços de Caldas, Varginha, Pouso Alegre, Passos", "x": 200, "y": 440},
    {"nome": "Vale do Aço", "cidades": "Ipatinga, Coronel Fabriciano, Timóteo", "x": 430, "y": 260},
    {"nome": "Região Central", "cidades": "Sete Lagoas, Divinópolis, Curvelo", "x": 260, "y": 230},
    {"nome": "Norte de Minas", "cidades": "Montes Claros, Januária, Pirapora", "x": 250, "y": 90},
    {"nome": "Alto Paranaíba", "cidades": "Patrocínio, Araxá, Ibiá", "x": 130, "y": 300},
]

DIFERENCIAIS = [
    {"titulo": "20+ anos de know-how", "desc": "Duas décadas de experiência no mercado B2B de autopeças em Minas Gerais.", "icone": "award"},
    {"titulo": "Atendimento consultivo", "desc": "Acompanhamento próximo, com visitas técnicas e suporte comercial dedicado.", "icone": "handshake"},
    {"titulo": "Cobertura estadual", "desc": "Presença ativa nas principais regiões e polos automotivos de MG.", "icone": "map"},
    {"titulo": "Portfólio diversificado", "desc": "Múltiplas linhas de produtos para atender diferentes perfis de cliente.", "icone": "grid"},
]

HISTORICO = [
    {"ano": str(EMPRESA["fundacao_ano"]), "titulo": "Fundação", "desc": "Início das atividades de representação comercial no setor de autopeças em Minas Gerais."},
    {"ano": str(EMPRESA["fundacao_ano"] + 6), "titulo": "Expansão de carteira", "desc": "Ampliação do portfólio de marcas representadas e da equipe comercial."},
    {"ano": str(EMPRESA["fundacao_ano"] + 13), "titulo": "Cobertura estadual", "desc": "Consolidação do atendimento nas principais regiões de Minas Gerais."},
    {"ano": str(datetime.now().year), "titulo": "Presente", "desc": "Mais de " + str(EMPRESA["anos_atuacao"]) + " anos de mercado, com foco em relacionamento de longo prazo e resultado para os parceiros."},
]


@app.context_processor
def inject_globals():
    return {
        "empresa": EMPRESA,
        "ano_atual": datetime.now().year,
    }


# ---------------------------------------------------------------------------
# AUTENTICAÇÃO SIMPLES DO PAINEL ADMIN
# ---------------------------------------------------------------------------
def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin_logado"):
            return redirect(url_for("admin_login"))
        return view(*args, **kwargs)
    return wrapped


# ---------------------------------------------------------------------------
# ROTAS PÚBLICAS
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template(
        "index.html",
        diferenciais=DIFERENCIAIS,
        linhas=LINHAS_PRODUTOS[:6],
        regioes=REGIOES_MG,
        marcas_parceiras=MARCAS_PARCEIRAS,
    )


@app.route("/sobre")
def sobre():
    return render_template("sobre.html", historico=HISTORICO, diferenciais=DIFERENCIAIS)


@app.route("/marcas")
def marcas():
    return render_template("marcas.html", linhas=LINHAS_PRODUTOS, marcas_parceiras=MARCAS_PARCEIRAS)


@app.route("/cobertura")
def cobertura():
    return render_template("cobertura.html", regioes=REGIOES_MG)


@app.route("/contato", methods=["GET", "POST"])
def contato():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        empresa_nome = request.form.get("empresa", "").strip()
        cidade = request.form.get("cidade", "").strip()
        telefone = request.form.get("telefone", "").strip()
        email = request.form.get("email", "").strip()
        assunto = request.form.get("assunto", "").strip()
        mensagem = request.form.get("mensagem", "").strip()

        erros = []
        if not nome:
            erros.append("Informe seu nome.")
        if not telefone:
            erros.append("Informe um telefone para contato.")
        if not mensagem:
            erros.append("Escreva uma mensagem.")

        if erros:
            for erro in erros:
                flash(erro, "erro")
            return render_template("contato.html", form=request.form), 400

        db = get_db()
        db.execute(
            """INSERT INTO mensagens
               (nome, empresa, cidade, telefone, email, assunto, mensagem, criado_em, lida)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)""",
            (nome, empresa_nome, cidade, telefone, email, assunto, mensagem,
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        db.commit()
        flash("Mensagem enviada com sucesso! Em breve entraremos em contato.", "sucesso")
        return redirect(url_for("contato"))

    return render_template("contato.html", form={})


@app.route("/robots.txt")
def robots():
    return Response("User-agent: *\nAllow: /\nSitemap: /sitemap.xml\n", mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap():
    pages = ["index", "sobre", "marcas", "cobertura", "contato"]
    urls = "\n".join(
        f"  <url><loc>{request.url_root.rstrip('/')}{url_for(p) if p != 'index' else '/'}</loc></url>"
        for p in pages
    )
    xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>'
    return Response(xml, mimetype="application/xml")


# ---------------------------------------------------------------------------
# PAINEL ADMIN (mensagens recebidas pelo formulário de contato)
# ---------------------------------------------------------------------------
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        senha = request.form.get("senha", "")
        if senha == EMPRESA["admin_senha"]:
            session["admin_logado"] = True
            return redirect(url_for("admin_mensagens"))
        flash("Senha incorreta.", "erro")
    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logado", None)
    return redirect(url_for("admin_login"))


@app.route("/admin/mensagens")
@login_required
def admin_mensagens():
    db = get_db()
    mensagens = db.execute("SELECT * FROM mensagens ORDER BY id DESC").fetchall()
    return render_template("admin_mensagens.html", mensagens=mensagens)


@app.route("/admin/mensagens/<int:msg_id>/marcar-lida")
@login_required
def marcar_lida(msg_id):
    db = get_db()
    db.execute("UPDATE mensagens SET lida = 1 WHERE id = ?", (msg_id,))
    db.commit()
    return redirect(url_for("admin_mensagens"))


@app.route("/admin/mensagens/<int:msg_id>/excluir")
@login_required
def excluir_mensagem(msg_id):
    db = get_db()
    db.execute("DELETE FROM mensagens WHERE id = ?", (msg_id,))
    db.commit()
    flash("Mensagem excluída.", "sucesso")
    return redirect(url_for("admin_mensagens"))


init_db()

if __name__ == "__main__":
    app.run(debug=True)
