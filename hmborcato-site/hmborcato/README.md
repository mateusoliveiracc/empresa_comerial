
## Estrutura de páginas

```
/                 Home
/empresa          A Empresa — história, fundador, missão/visão/valores, equipe
/representadas    Marcas representadas (NTN, Tungsram, Airmaks)
/linhas           Catálogo de linhas de produto
/atuacao-mg       Território — mapa e dados reais de Minas Gerais
/conteudo         Mercado & Novidades
/contato          Formulário de contato
/admin/login      Painel administrativo (mensagens recebidas)
```

## O que é real e o que é placeholder

Todo o conteúdo textual foi extraído do site atual (hmborcato.com.br) em 19/08/2026:
telefone, WhatsApp, e-mail, fundador, ano de fundação, missão/visão/valores, equipe,
marcas (NTN, Tungsram, Airmaks) e dados de Minas Gerais (área, municípios, frota).

**CNPJ e endereço** foram confirmados via base pública de CNPJ (Receita Federal),
cruzados com um diretório de representantes comerciais que usa o mesmo e-mail e
celular do fundador — por isso entraram como dado real, não placeholder.

**Fotografias**: o hero, a foto de equipe e as fotos individuais vêm do site atual
via link direto (hotlink) para hmborcato.com.br/images/..., por autorização do
cliente. Isso significa que **dependem do site antigo continuar no ar**. Assim que
possível, baixe as fotos em alta resolução e salve em `static/img/fotos/`, trocando
os caminhos no dicionário `FOTOS` no topo do `app.py`. Cada imagem tem fallback
automático (ícone da marca) caso o link pare de responder.

**Ainda faltam**:
- Fotos em alta resolução salvas localmente (ver acima)
- Demais marcas parceiras além de NTN, Tungsram e Airmaks
- Fotografias reais para as linhas de produto sem ícone próprio (Rolamentos,
  Iluminação, Filtros, Arrefecimento, EPI) — hoje mostram "Fotografia a adicionar"
- Corpo completo das notícias em "Mercado & Novidades" (o CMS antigo só tinha títulos e, em alguns casos, imagem)

Tudo isso fica centralizado no topo do `app.py`, nos dicionários `EMPRESA`,
`FOTOS`, `MARCAS_PARCEIRAS`, `NOTICIAS` etc. — edite ali para atualizar o site inteiro.

## Direção visual (2ª revisão)

Ajustada para se afastar de estética "SaaS/tech" e se aproximar de uma empresa
de representação comercial automotiva: hero com fotografia real (não mais
abstrato), mapa de MG escuro e integrado à identidade (não mais um card claro
tipo relatório), marcas representadas como lista tipo carteira comercial em vez
de cards coloridos, linhas de produto em formato catálogo com painel de foto.
Paleta grafite + azul aço como cor de destaque (CTAs, hover, linhas, dados) —
não o site inteiro azul. Números só aparecem quando confirmados; "anos de
experiência" nunca é apresentado como idade da empresa.

## Revisão de marcas, linhas e imagens (3ª rodada)

**Hero**: a foto anterior (do site atual do cliente) estava com baixa nitidez — foi substituída por uma fotografia profissional de componentes automotivos em alta resolução, do banco de imagens gratuito Unsplash (uso comercial livre, sem necessidade de atribuição). Estrutura pronta para trocar por foto real da H.M. Borçato — é só editar `FOTOS["hero"]` no topo do `app.py`.

**Marcas representadas**: a lista foi substituída pela lista oficial informada pelo cliente (11 marcas). Antes de implementar, cada marca foi pesquisada individualmente na internet para confirmar segmento e linha real:

| Marca | Linha confirmada |
|---|---|
| Sintech | Componentes de motor (anéis, bronzinas, pistões, buchas, válvulas) |
| Pysko | Kits automotivos (amortecedor, homocinética, direção, câmbio) |
| Cofran | Iluminação automotiva (lanternas e retrovisores) |
| Hexlub | Lubrificantes automotivos, industriais e agrícolas |
| Nidec | Componentes elétricos/eletrônicos automotivos |
| Aeroflex | Produtos químicos e aerossóis |
| Mundial Prime | Linha automotiva de aerossóis (marca da Aeroflex) |
| VP (Virtual Plásticos) | Acessórios plásticos (retrovisores, máquinas de vidro) |
| Cyclo | Adesivos e silicones automotivos |
| **FB** | **[CONFIRMAR LINHA DA MARCA]** — não foi possível identificar com segurança qual "FB" é essa, entre várias empresas com esse nome |
| **Clintech** | **[CONFIRMAR LINHA DA MARCA]** — não encontrei nenhuma referência a uma marca automotiva com esse nome |

As marcas antigas (NTN, Tungsram, Airmaks) foram **removidas** do site, incluindo as notícias que faziam referência a elas em "Mercado & Novidades" (ficaram inconsistentes com a nova lista oficial).

**Linhas de produto**: reorganizadas para refletir apenas categorias com marca confirmada por trás (Motor/Sintech, Suspensão e Direção/Pysko, Iluminação/Cofran, Lubrificação/Hexlub, Eletrônica/Nidec, Aerossóis/Aeroflex+Mundial Prime, Acessórios/VP, Adesivos/Cyclo). Categorias antigas sem marca confirmada (Freios, Rolamentos, Filtros, Arrefecimento) foram removidas.

**Logos das marcas**: não incluí logos oficiais de terceiros no site — teria que baixar e confirmar direitos de uso de 9 marcas diferentes, o que está fora do que consigo validar com segurança neste momento. Os cards usam tipografia limpa, com estrutura pronta para trocar por logo real (campo `img` em cada marca no `app.py`, hoje vazio).

**Fundos alternados**: a Home agora segue Hero(escuro+foto) → Marcas(claro) → Experiência(escuro/azul+foto) → O que fazemos(claro) → Linhas(escuro+ícones) → Atuação em MG(claro+mapa escuro) → Conteúdo(claro, se houver) → CTA final(escuro/azul) — sem mais sequências de fundo branco repetidas.

## Ideias de melhoria para os próximos passos

- Fotos reais da equipe e de produtos/estoque
- Corpo completo de cada notícia em "Mercado & Novidades", com datas
- Depoimentos de clientes/distribuidores parceiros
- Catálogo em PDF para download (bom gerador de leads)
- Google Analytics / Meta Pixel
- Deploy em Render, Railway ou PythonAnywhere — trocar `SECRET_KEY` e `admin_senha` por variáveis de ambiente fortes antes de publicar
