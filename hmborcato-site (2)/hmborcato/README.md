# Site institucional — H.M. Borçato Representação Comercial e Marketing

Site institucional e comercial em **Flask + SQLite + Tailwind CSS**, mobile-first, com formulário de contato funcional e painel administrativo simples para ver as mensagens recebidas.

## Como rodar no PyCharm / Windows

1. Abra a pasta `hmborcato` no PyCharm como projeto.
2. Crie um ambiente virtual (PyCharm geralmente sugere automaticamente) e instale as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Rode o arquivo `app.py` (botão ▶ do PyCharm, ou `python app.py`).
4. Acesse **http://127.0.0.1:5000** no navegador.

O banco de dados SQLite (`instance/hmborcato.db`) é criado automaticamente na primeira execução — não precisa de nenhuma configuração extra.

## Estrutura do projeto

```
hmborcato/
├── app.py                  # rotas, banco de dados e configurações da empresa
├── requirements.txt
├── instance/                # banco SQLite (criado automaticamente)
├── static/
│   ├── css/style.css        # estilos customizados (linha de rota, animações)
│   ├── js/main.js           # menu mobile, scroll reveal, máscara de telefone
│   └── img/favicon.svg
└── templates/
    ├── base.html             # layout com header, footer e botão do WhatsApp
    ├── _icons.html           # ícones SVG inline (sem dependência externa)
    ├── index.html            # Home
    ├── sobre.html            # Sobre / história / linha do tempo
    ├── marcas.html           # Linhas de autopeças representadas
    ├── cobertura.html        # Mapa de cobertura em Minas Gerais
    ├── contato.html          # Formulário de contato
    ├── admin_login.html      # Login do painel
    └── admin_mensagens.html  # Lista de mensagens recebidas
```

## O que você precisa personalizar antes de publicar

Tudo fica centralizado no topo do `app.py`, no dicionário `EMPRESA`:

- Telefone, WhatsApp, e-mails, endereço, CNPJ e horário de funcionamento
- `fundacao_ano`: usado para calcular "X anos de mercado" automaticamente
- `admin_senha`: senha do painel `/admin/login` (troque antes de publicar!)
- Links de Instagram e LinkedIn

Outros pontos de customização:

- **Logo**: hoje é um monograma em SVG dentro de `templates/base.html` (busque por `<svg width="40" height="40"`). Troque pelo logo real assim que tiver o arquivo — recomendo SVG para manter a nitidez em qualquer tamanho.
- **Linhas de produto representadas**: lista `LINHAS_PRODUTOS` em `app.py`. Ajuste nomes e descrições para as marcas/linhas reais que a empresa representa.
- **Regiões de cobertura**: lista `REGIOES_MG` em `app.py`. As posições `x`/`y` controlam onde o marcador aparece no mapa estilizado (SVG `viewBox 0 0 500 520`, veja `templates/cobertura.html`).
- **Linha do tempo**: lista `HISTORICO` em `app.py` — ajuste para a história real da empresa.

## Formulário de contato

As mensagens são salvas no banco SQLite e aparecem em **`/admin/mensagens`** (login em `/admin/login`, senha definida em `ADMIN_SENHA`/`admin_senha`).

Se quiser também **receber por e-mail** a cada novo contato, adicione o envio via SMTP dentro da rota `contato()` em `app.py`, logo após o `db.commit()` — por exemplo usando `smtplib` com as credenciais do seu provedor de e-mail (Gmail, Zoho, etc.), ou um serviço como SendGrid/Resend. Prefiro deixar essa parte para você conectar com suas credenciais reais, em vez de colocar segredos falsos no código.

## Ideias de melhoria para os próximos passos

- **Fotos reais**: substituir os ícones/ilustrações por fotos da equipe, showroom ou produtos — aumenta a confiança em sites B2B.
- **Depoimentos de clientes**: uma seção de avaliações de lojistas parceiros é um dos maiores gatilhos de conversão em representação comercial.
- **Google Business Profile + mapa incorporado**: complementa o mapa estilizado com um mapa real (Google Maps embed) na página de Contato.
- **Blog/Notícias**: conteúdo sobre lançamentos de linhas e dicas para lojistas ajuda no SEO orgânico de médio prazo.
- **Catálogo em PDF para download**: um botão "Baixar catálogo" na página de Marcas é um bom gerador de leads (pode pedir e-mail antes do download).
- **Google Analytics / Meta Pixel**: adicionar assim que tiver as contas, para medir a origem dos contatos.
- **Deploy**: quando for publicar, plataformas simples como Render, Railway ou PythonAnywhere rodam Flask sem muita configuração. Nesse momento, também troque `SECRET_KEY` e `admin_senha` por valores fortes via variáveis de ambiente.

## Performance

- Zero dependências JS pesadas — apenas Tailwind via CDN e um `main.js` pequeno (vanilla JS).
- Ícones em SVG inline (sem requisições externas nem bibliotecas de ícones).
- Fontes carregadas com `preconnect` e `display=swap`.
- HTML semântico (`header`, `nav`, `main`, `footer`, `section`), com foco visível e respeito a `prefers-reduced-motion` para acessibilidade.
