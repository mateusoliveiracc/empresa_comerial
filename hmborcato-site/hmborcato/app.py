# -*- coding: utf-8 -*-
"""
H.M. Borçato Representação Comercial e Marketing
Site institucional — Flask + SQLite
Conteúdo baseado em informações reais extraídas de hmborcato.com.br em 19/08/2026.
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
# DADOS REAIS DA EMPRESA
# Fonte primária: hmborcato.com.br (19/08/2026).
# CNPJ e endereço: confirmados via base pública de CNPJ (Receita Federal) e
# cruzados com diretório de representantes comerciais (mesmo e-mail/celular
# do fundador). Campos ainda sem confirmação ficam com placeholder explícito.
# ---------------------------------------------------------------------------
EMPRESA = {
    "nome": "H.M. Borçato Representação Comercial e Marketing",
    "nome_curto": "H.M. Borçato",
    "fundador": "Fábio Borçato",
    "fundador_cargo": "Diretor",
    "fundacao_mes_ano": "setembro de 2018",
    "fundacao_ano": 2018,
    "anos_experiencia_pre_fundacao": 14,
    "cidade_sede": "Belo Horizonte",
    "estado_sede": "MG",
    "endereco_completo": "Rua Macaé, 738 — apto 201, Graça",
    "endereco_cep": "31140-060",
    "cnpj": "28.427.986/0001-08",
    "telefone_exibicao": "(31) 3146-1975",
    "telefone_tel": "+553131461975",
    "whatsapp_numero": "5531996568022",
    "whatsapp_exibicao": "(31) 99656-8022",
    "whatsapp_mensagem_padrao": "Gostaria de fazer um orçamento",
    "email_contato": "contato@hmborcato.com.br",
    "instagram": "https://www.instagram.com/representanteautopecas/",
    "facebook": "https://www.facebook.com/HM-Bor%C3%A7ato-Representa%C3%A7%C3%A3o-comercial-e-Marketing-481143932329143/",
    "admin_senha": os.environ.get("ADMIN_SENHA", "borcato2026"),
}
EMPRESA["anos_atuacao"] = datetime.now().year - EMPRESA["fundacao_ano"]
EMPRESA["anos_experiencia_total"] = EMPRESA["anos_atuacao"] + EMPRESA["anos_experiencia_pre_fundacao"]

# ---------------------------------------------------------------------------
# FOTOGRAFIAS
# Equipe/fundador: hotlink direto do site atual (hmborcato.com.br), por
# autorização do cliente. Hero/Experiência: fotos profissionais do Unsplash
# (licença livre para uso comercial, sem necessidade de atribuição) — a foto
# anterior do hero foi trocada porque o cliente reportou baixa nitidez.
# Nenhuma foi baixada para o projeto porque o ambiente de build não tem
# acesso à rede desses domínios; ao publicar, recomenda-se salvar cópias
# locais em alta resolução em static/img/fotos/ e trocar os caminhos — para
# o hero, idealmente por fotos reais do estoque/operação da H.M. Borçato.
# Cada <img> tem fallback caso o arquivo remoto fique indisponível.
# ---------------------------------------------------------------------------
FOTOS = {
    # Hero: substituído por fotografia profissional de componentes automotivos
    # em alta resolução (Unsplash — uso livre, comercial, sem marca d'água),
    # pois a imagem anterior (do site atual do cliente) estava com baixa
    # nitidez. Estrutura pronta para substituir por foto real da empresa.
    "hero": "https://images.unsplash.com/photo-1595787142842-7404bc60470d?auto=format&fit=crop&w=1800&q=85",
    "experiencia": "https://images.unsplash.com/photo-1527383418406-f85a3b146499?auto=format&fit=crop&w=1400&q=85",
    "equipe": "https://www.hmborcato.com.br/images/equipe.jpeg",
    "fabio": "https://www.hmborcato.com.br/images/fabio.jpeg",
    "valeria": "https://www.hmborcato.com.br/images/valeria.jpeg",
    "vanessa": "https://www.hmborcato.com.br/images/vanessa.jpeg",
    "phillip": "https://www.hmborcato.com.br/images/phillip.jpeg",
    "gabriela": "https://www.hmborcato.com.br/images/gabriela.jpeg",
    "leticia": "https://www.hmborcato.com.br/images/leticia.jpg",
}

# ---------------------------------------------------------------------------
# TERRITÓRIO — dados reais de Minas Gerais (fonte: página "Serviços" do site atual)
# ---------------------------------------------------------------------------
TERRITORIO_MG = {
    "area": "586.528 km²",
    "municipios": "853",
    "populacao": "≈ 20 milhões de habitantes",
    "populacao_desc": "2º estado mais populoso do Brasil",
    "capital": "Belo Horizonte",
    "capital_desc": "≈ 5,5 milhões de hab. na região metropolitana — 3ª maior aglomeração urbana do Brasil",
    "pib": "3º maior PIB do Brasil",
    "frota": "2ª maior frota nacional",
    "frota_desc": "10,4% do total da frota circulante do país — dados 2017, divulgados pela empresa",
}

# ---------------------------------------------------------------------------
# HISTÓRIA — apenas fatos confirmados no site institucional atual
# ---------------------------------------------------------------------------
HISTORICO = [
    {
        "periodo": "Antes de 2018",
        "titulo": "Know-how no mercado mineiro",
        "desc": f"{EMPRESA['fundador']} acumula {EMPRESA['anos_experiencia_pre_fundacao']} anos em representação comercial de autopeças em Minas Gerais — atendendo distribuidores regionais e filiais de indústrias nacionais e multinacionais, a maior parte do tempo como gerente de outro escritório de representação.",
    },
    {
        "periodo": "Set. 2018",
        "titulo": "Fundação da H.M. Borçato",
        "desc": f"{EMPRESA['fundador']} inicia a H.M. Borçato Representação Comercial e Marketing. O nome homenageia seus filhos — Henrique e Mateus — e a família Borçato.",
    },
    {
        "periodo": "Atuação atual",
        "titulo": "Cobertura em todo o estado",
        "desc": "Equipe própria e sistema informatizado em nuvem sustentam uma estratégia de cobertura presencial constante, com rotas comerciais planejadas em todas as regiões de Minas Gerais.",
    },
]

MISSAO = "Proporcionar às indústrias representadas e aos clientes os negócios mais competitivos e rentáveis do mercado."
VISAO = "Ser reconhecida como referência em representação comercial em Minas Gerais, com aperfeiçoamento contínuo dos processos e rentabilidade para todos os envolvidos."
VALORES = ["Ética", "Transparência", "Respeito às pessoas", "Humildade", "Satisfação do cliente", "Evolução contínua", "Lealdade"]

# Equipe (nomes reais divulgados no site institucional; sem cargos, pois não são públicos)
EQUIPE = [
    {"nome": "Fábio Borçato", "foto": "fabio"},
    {"nome": "Valéria", "foto": "valeria"},
    {"nome": "Vanessa", "foto": "vanessa"},
    {"nome": "Phillip", "foto": "phillip"},
    {"nome": "Gabriela", "foto": "gabriela"},
    {"nome": "Letícia", "foto": "leticia"},
]

# ---------------------------------------------------------------------------
# O QUE FAZEMOS — quatro frentes de atuação
# ---------------------------------------------------------------------------
FRENTES_ATUACAO = [
    {"titulo": "Representação Comercial", "desc": "Atendimento direto a distribuidores, lojistas e filiais regionais em nome das indústrias representadas.", "icone": "handshake"},
    {"titulo": "Desenvolvimento de Mercado", "desc": "Expansão de carteira e abertura de novos pontos de venda para as marcas representadas em Minas Gerais.", "icone": "map"},
    {"titulo": "Marketing e Apoio às Marcas", "desc": "Divulgação de lançamentos, comunicação com o mercado e ações comerciais junto aos parceiros.", "icone": "award"},
    {"titulo": "Relacionamento Comercial", "desc": "Cobertura presencial constante e sistema em nuvem para agilidade, precisão e transparência nas negociações.", "icone": "grid"},
]

# ---------------------------------------------------------------------------
# DIFERENCIAIS — "Representação que gera negócio"
# ---------------------------------------------------------------------------
DIFERENCIAIS = [
    {"titulo": "Conhecimento de mercado", "desc": f"{EMPRESA['anos_experiencia_total']}+ anos de experiência acumulada no mercado automotivo mineiro.", "icone": "award"},
    {"titulo": "Presença regional constante", "desc": "Cobertura presencial ativa nas principais regiões de Minas Gerais, com rotas comerciais planejadas.", "icone": "map"},
    {"titulo": "Sistema de gestão em nuvem", "desc": "Base de dados na nuvem garante agilidade, precisão e transparência em cada negociação.", "icone": "grid"},
    {"titulo": "Marketing como estratégia", "desc": "Apoio ativo à divulgação, lançamentos e ações comerciais das marcas representadas.", "icone": "handshake"},
]

# ---------------------------------------------------------------------------
# MARCAS REPRESENTADAS — apenas marcas confirmadas no site/notícias reais.
# Adicione aqui as demais marcas parceiras que o cliente fornecer.
# ---------------------------------------------------------------------------
MARCAS_PARCEIRAS = [
    {"nome": "Sintech", "linha": "Componentes de motor — anéis, bronzinas, pistões, buchas, válvulas e comando de válvulas", "confirmado": True},
    {"nome": "Pysko", "linha": "Kits automotivos — amortecedor, homocinética, caixa de direção, câmbio, bieletas e suportes", "confirmado": True},
    {"nome": "Cofran", "linha": "Iluminação automotiva — lanternas e retrovisores", "confirmado": True},
    {"nome": "Hexlub", "linha": "Lubrificantes automotivos, industriais e agrícolas", "confirmado": True},
    {"nome": "Nidec", "linha": "Componentes elétricos e eletrônicos automotivos — motores de arranque, ignição e injeção eletrônica", "confirmado": True},
    {"nome": "Aeroflex", "linha": "Produtos químicos e aerossóis para o setor automotivo", "confirmado": True},
    {"nome": "Mundial Prime", "linha": "Linha automotiva de lubrificantes, limpeza, manutenção e aerossóis (marca da Aeroflex)", "confirmado": True},
    {"nome": "VP", "linha": "Acessórios e componentes plásticos — retrovisores, máquinas de vidro e linha mecânica", "confirmado": True},
    {"nome": "Cyclo", "linha": "Adesivos, silicones e produtos especiais para o setor automotivo", "confirmado": True},
    {"nome": "FB", "linha": "[CONFIRMAR LINHA DA MARCA]", "confirmado": False},
    {"nome": "Clintech", "linha": "[CONFIRMAR LINHA DA MARCA]", "confirmado": False},
]

# ---------------------------------------------------------------------------
# LINHAS DE PRODUTO — categorias gerais do segmento de reposição automotiva.
# Textos de exemplo fornecidos pelo próprio cliente no briefing.
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# LINHAS DE PRODUTO — organizadas por categoria REAL, cada uma associada a
# uma marca confirmada da carteira. Só existe categoria aqui quando há marca
# comprovada que atua nela — nada foi inventado.
# ---------------------------------------------------------------------------
LINHAS_PRODUTOS = [
    {"nome": "Motor", "desc": "Componentes internos de motor — anéis, bronzinas, pistões, buchas, válvulas e comando de válvulas.", "marca": "Sintech", "icone": "engine", "img": "piston.png"},
    {"nome": "Suspensão e Direção", "desc": "Kits de amortecedor, homocinética, caixa de direção, câmbio, bieletas e suportes.", "marca": "Pysko", "icone": "suspension", "img": "suspension.png"},
    {"nome": "Iluminação Automotiva", "desc": "Lanternas e retrovisores para o mercado de reposição.", "marca": "Cofran", "icone": "bulb"},
    {"nome": "Lubrificação", "desc": "Óleos e lubrificantes automotivos, industriais e agrícolas.", "marca": "Hexlub", "icone": "oildrop"},
    {"nome": "Eletrônica Automotiva", "desc": "Componentes elétricos e eletrônicos — motores de arranque, ignição e injeção eletrônica.", "marca": "Nidec", "icone": "bolt"},
    {"nome": "Aerossóis e Manutenção", "desc": "Produtos químicos, lubrificação, limpeza e manutenção automotiva em aerossol.", "marca": "Aeroflex / Mundial Prime", "icone": "spraycan"},
    {"nome": "Acessórios e Componentes", "desc": "Peças plásticas — retrovisores, máquinas de vidro e linha mecânica.", "marca": "VP", "icone": "puzzle"},
    {"nome": "Adesivos e Vedantes", "desc": "Silicones, colas e produtos especiais para o setor automotivo.", "marca": "Cyclo", "icone": "adhesive"},
]

# ---------------------------------------------------------------------------
# MERCADO & NOVIDADES — títulos reais publicados no site atual da empresa.
# Sem datas/corpo de texto porque o CMS original não os disponibiliza — a
# estrutura está pronta para receber o conteúdo completo quando fornecido.
# ---------------------------------------------------------------------------
NOTICIAS = [
    # As notícias anteriores (NTN, Tungsram, Airmaks) foram removidas porque
    # essas marcas não constam na lista oficial de representadas informada
    # pelo cliente. Adicione aqui novidades reais das marcas atuais quando
    # houver conteúdo disponível.
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


@app.context_processor
def inject_globals():
    return {"empresa": EMPRESA, "ano_atual": datetime.now().year, "fotos": FOTOS}


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
        linhas=LINHAS_PRODUTOS[:4],
        regioes=REGIOES_MG,
        marcas_parceiras=MARCAS_PARCEIRAS,
        territorio=TERRITORIO_MG,
        historico=HISTORICO,
        frentes=FRENTES_ATUACAO,
        noticias=NOTICIAS[:3],
    )


@app.route("/empresa")
def empresa():
    return render_template(
        "empresa.html",
        historico=HISTORICO,
        equipe=EQUIPE,
        missao=MISSAO, visao=VISAO, valores=VALORES,
        frentes=FRENTES_ATUACAO,
    )


@app.route("/representadas")
def representadas():
    return render_template("representadas.html", marcas_parceiras=MARCAS_PARCEIRAS, linhas=LINHAS_PRODUTOS)


@app.route("/linhas")
def linhas():
    return render_template("linhas.html", linhas=LINHAS_PRODUTOS)


@app.route("/atuacao-mg")
def atuacao_mg():
    return render_template("atuacao_mg.html", regioes=REGIOES_MG, territorio=TERRITORIO_MG)


@app.route("/conteudo")
def conteudo():
    return render_template("conteudo.html", noticias=NOTICIAS)


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
    pages = ["index", "empresa", "representadas", "linhas", "atuacao_mg", "conteudo", "contato"]
    urls = "\n".join(
        f"  <url><loc>{request.url_root.rstrip('/')}{url_for(p) if p != 'index' else '/'}</loc></url>"
        for p in pages
    )
    xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>'
    return Response(xml, mimetype="application/xml")


# ---------------------------------------------------------------------------
# PAINEL ADMIN
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
