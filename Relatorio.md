# Relatório de Laboratório

*Laboratório de Experimentação de Software — Modelo/Template de Relatório*

Este documento é um MODELO válido para qualquer um dos 5 laboratórios da disciplina (Lab01 a Lab05). Os parágrafos em itálico cinza/verde, iniciados por "ORIENTAÇÃO", explicam o que cada subseção deve conter — apague-os e escreva o conteúdo real do grupo no lugar. Textos entre colchetes [assim] indicam onde inserir informação específica do seu grupo/laboratório.

| | |
|---|---|
| **Curso** | Engenharia de Software |
| **Disciplina** | Laboratório de Experimentação de Software |
| **Turno / Período** | Noite / 6º |
| **Professor(a)** | Danilo Maia |
| **Laboratório** | [Lab01 — Repositórios Populares] |
| **Grupo (trio)** | Arthur Lara Panzera · Felipe Augusto Pereira · Gabriel Reis Lebron |
| **Link do repositório / GitHub Projects** | https://github.com/GabrielReiiss/Lab-ExperimentacaoDeSoftware |
| **Data de entrega** | 26/08/2026 |

---

## 1. Introdução

Repositórios populares no GitHub concentram grande parte da atenção da comunidade open-source: costumam ser referência de qualidade, atraem contribuidores e influenciam práticas adotadas pelo mercado. Apesar disso, o que de fato caracteriza esses repositórios (se são maduros, bem mantidos, concentrados em poucas linguagens, ou geridos com algum rigor de processo) raramente é medido de forma sistemática, ficando mais no campo da percepção do que da evidência. Este trabalho caracteriza empiricamente os 1.000 repositórios open-source mais populares do GitHub por número de estrelas, a partir de dados coletados via API GraphQL do GitHub, para verificar se essas percepções comuns se sustentam nos dados coletados.

Essa caracterização importa tanto para a engenharia de software, que ganha evidência sobre práticas associadas a projetos populares (cadência de release, resposta a issues, frequência de atualização), quanto para o próprio grupo, que usa o exercício para praticar coleta de dados em escala via API, tratamento de valores ausentes e outliers, e comunicação de resultados estatísticos.

A caracterização é guiada por sete questões de pesquisa do enunciado, RQ01 a RQ07:

- **RQ01**: Sistemas populares são maduros/antigos?
    - métrica: idade do repositório.
- **RQ02**: Sistemas populares recebem muita contribuição externa?
    - métrica: total de pull requests mescladas.
- **RQ03**: Sistemas populares lançam releases com frequência?
    - métrica: total de releases.
- **RQ04**: Sistemas populares são atualizados com frequência?
    - métrica: tempo até a última atualização.
- **RQ05**: Sistemas populares são escritos nas linguagens mais populares?
    - métrica: linguagem primária de cada repositório.
- **RQ06**: Sistemas populares possuem um alto percentual de issues fechadas?
    - métrica: razão entre issues fechadas e total de issues.
- **RQ07**: Sistemas escritos nas linguagens mais populares recebem mais contribuição externa, lançam mais releases e são atualizados com mais frequência?
    - métrica: RQ02, RQ03 e RQ04 agrupadas pela linguagem da RQ05.

**Hipóteses informais**, formuladas pelo grupo antes da análise formal dos dados:

- **RQ01**: esperamos que repositórios populares sejam majoritariamente antigos, já que acumular um número alto de estrelas costuma exigir tempo de exposição e uso contínuo pela comunidade, tornando repositórios muito recentes uma minoria entre os mais populares.
- **RQ02**: esperamos que repositórios populares recebam contribuição externa significativa, medida pelo número de pull requests mescladas, dado que maior visibilidade tende a atrair mais colaboradores dispostos a propor mudanças.
- **RQ03**: esperamos que repositórios populares lancem releases com frequência regular, já que projetos com muita visibilidade tendem a ter ciclos de desenvolvimento mais estruturados e cadência de versionamento previsível.
- **RQ04**: esperamos que repositórios populares sejam atualizados com frequência alta, dado que atraem mais colaboradores e exigem manutenção constante para sustentar a base de usuários.
- **RQ05**: esperamos que a maioria dos repositórios populares esteja concentrada nas linguagens de propósito geral mais usadas do mercado (ex.: JavaScript/TypeScript, Python, Java), já que essas linguagens têm o maior número de desenvolvedores e ecossistemas mais maduros para projetos open-source de grande escala. Fonte adotada para "linguagens mais populares": GitHub Octoverse 2025, detalhada na seção 2.
- **RQ06**: esperamos que repositórios populares tenham uma alta taxa de issues fechadas, já que a visibilidade atrai mantenedores e contribuidores que respondem e resolvem problemas relatados com mais agilidade.
- **RQ07**: esperamos que repositórios escritos nas linguagens mais populares recebam mais contribuição externa, lancem mais releases e sejam atualizados com mais frequência do que os demais, já que ecossistemas de linguagem maiores tendem a atrair mais desenvolvedores e ferramentas de automação de build e release.

**Inovações do grupo (30% da nota)**, detalhadas na Metodologia (seção 3.6):

- Análise de correlação (Pearson e Spearman) entre as seis métricas normalizadas de RQ01-RQ06, para verificar se alguma delas é redundante o suficiente para ser descartada.
- Índice composto de saúde/maturidade do repositório, combinando as seis métricas normalizadas por média ponderada num único score por repositório.

## 2. Contexto

*ORIENTAÇÃO: Situe o leitor no cenário do estudo. Primeiro, o contexto acadêmico: em qual momento do semestre este laboratório se encontra e como ele se conecta aos anteriores (ex.: "este é o Lab04, que consome os dados de mineração do Lab03 e os snapshots do Kanban mantidos desde o Lab01"). Segundo, o contexto do objeto de estudo em si: o que exatamente está sendo medido (os 1.000 repositórios mais populares do GitHub — Lab01; o processo de resolução de katas com e sem IA — Lab02; repositórios com CI/CD via GitHub Actions — Lab03; o board Kanban do próprio grupo — Lab04/Lab05). Cite aqui referências conceituais relevantes usadas como base teórica (ex.: o livro Accelerate, de Forsgren, Humble & Kim, para métricas DORA; o método GQM de Basili, Caldiera & Rombach para o meta-laboratório; o índice usado para "linguagens mais populares" no Lab01 — TIOBE, GitHut ou GitHub Octoverse, mantendo a mesma fonte do início ao fim).*

*[conteúdo do grupo — substituir este texto]*

## 3. Metodologia

*ORIENTAÇÃO: Esta é a seção mais longa do relatório e a que mais evidencia o trabalho real do grupo. Ela tem seis subseções — as cinco primeiras cobrem principalmente os 70% do enunciado; a última (Inovações) é onde os 30% de contribuição própria do grupo devem ficar explícitos e fáceis de identificar na correção.*

### 3.1 Principais Desafios

*ORIENTAÇÃO: Relate as dificuldades técnicas e metodológicas reais enfrentadas pelo grupo — não uma lista de trivialidades já resolvidas, e sim decisões difíceis de fato. Exemplos típicos, conforme o laboratório: limite de taxa (rate limit) da API do GitHub ao consultar milhares de repositórios ou workflow runs (Lab01/Lab03); paginação de grandes volumes de dados; ausência de histórico de mudança de status consultável via API no GitHub Projects, exigindo snapshots manuais recorrentes (todos os laboratórios); dificuldade de padronizar katas de dificuldade equivalente e evitar memorização de soluções pela IA (Lab02); ambiguidade na definição operacional de uma métrica, como lead time (Lab03); dados incompletos ou repositórios sem GitHub Actions habilitado (Lab03).*

*[conteúdo do grupo — substituir este texto]*

### 3.2 Tomadas de Decisão

*ORIENTAÇÃO: Documente as decisões metodológicas do grupo e o raciocínio (trade-off) por trás de cada uma — não apenas a escolha final. Exemplos que os enunciados pedem explicitamente: o limite de WIP definido para a coluna Doing e sua justificativa (obrigatório em todo laboratório); qual assistente de IA foi usado e por quê, e como se garantiu o mesmo tratamento em todos os trials (Lab02); qual definição operacional de métrica foi adotada quando o enunciado permite variação, mantendo-a consistente para toda a amostra (ex.: lead time no Lab03); critério de inclusão/exclusão de repositórios na amostra; linguagem de programação escolhida em função da ferramenta de métricas estáticas disponível (CK exige Java; Radon para Python).*

*[conteúdo do grupo — substituir este texto]*

### 3.3 Etapas

*ORIENTAÇÃO: Descreva o processo de desenvolvimento em sprints, seguindo a estrutura do enunciado (ex.: Lab0XS01, S02, S03 + Relatório Final), com o que foi efetivamente entregue em cada uma e quem (qual integrante) foi responsável por qual parte — a correção do professor é feita a partir do board (GitHub Projects), então a divisão aqui deve refletir os Assignees reais das Issues, não uma divisão apenas narrativa. Inclua também a subseção "Configuração do processo" exigida em todos os laboratórios: as colunas do board (mínimo Backlog → To Do → Doing → Review → Done), a política de limite de WIP em uso, e uma captura de tela (print) do board ao final do laboratório, mostrando o fluxo real de trabalho do grupo.*

[Tabela ou linha do tempo com Sprint | Entregas | Responsável(is) | Issues (nº)]

> Sugestão: insira aqui o print do quadro Kanban (GitHub Projects) mencionado na orientação acima.

### 3.4 Ferramentas

*ORIENTAÇÃO: Liste as ferramentas usadas na coleta, processamento e análise de dados — sejam específicas (nome e versão quando relevante), não genéricas. Exemplos conforme o laboratório: GraphQL e/ou REST API do GitHub para mineração (Lab01/Lab03 — bibliotecas de terceiros para consulta à API não são permitidas, o script deve ser próprio do grupo); Python/Pandas para manipulação de dados; Matplotlib/Seaborn ou Plotly/Dash/Streamlit para visualização; CK, PMD ou Radon para métricas estáticas de código (Lab02); testes estatísticos como o de Wilcoxon para amostras pareadas (Lab02); ferramenta de BI (Power BI, Tableau, Looker Studio) caso o grupo não opte pelo dashboard em código (Lab04). Inclua também a ferramenta de processo, obrigatória em todos os laboratórios: GitHub Projects (v2), com o link do repositório/board do grupo.*

*[conteúdo do grupo — substituir este texto]*

### 3.5 Tabela de Métricas

*ORIENTAÇÃO: Construa uma tabela relacionando cada Questão de Pesquisa à métrica correspondente, sua definição operacional exata (a fórmula ou regra de cálculo — não basta o nome) e a ferramenta/fonte usada para coletá-la. Isso é o que garante que o laboratório seja reprodutível por outro grupo. A primeira linha abaixo é um exemplo ilustrativo (baseado no Lab01); substitua pelas RQs e métricas do seu laboratório.*

| RQ | Métrica | Definição Operacional | Unidade | Ferramenta / Fonte |
|---|---|---|---|---|
| *RQ01 (exemplo)* | *Idade do repositório* | *Data atual − data de criação do repositório* | *Dias* | *Script GraphQL (API do GitHub)* |
| | | | | |
| | | | | |
| | | | | |
| | | | | |

### 3.6 Inovações Propostas pelo Grupo (30% da nota)

*ORIENTAÇÃO: O enunciado do laboratório corresponde a 70% da exigência da disciplina. Os outros 30% dependem de uma contribuição original do grupo, que deve estar claramente identificada aqui — não diluída no restante do texto — para facilitar a correção. Escolha uma ou mais frentes de inovação, entre: (a) uma nova Questão de Pesquisa, além das do enunciado; (b) uma métrica ou variável adicional, não pedida no enunciado; (c) uma mudança de arquitetura/ferramenta de coleta (ex.: paralelizar a coleta, usar cache, trocar de biblioteca de visualização); (d) uma metodologia alternativa ou complementar (ex.: um teste estatístico adicional, uma segmentação diferente da amostra, uma técnica de controle de ameaça à validade não exigida pelo enunciado). Para cada inovação escolhida, explique o que foi feito, por que o grupo considerou relevante, e onde o resultado dela aparece nas seções de Resultados/Discussão e na Conclusão — inovação sem resultado discutido não conta como contribuição efetiva.*

*[conteúdo do grupo — substituir este texto]*

**Índice composto de saúde/maturidade do repositório.** As seis RQs do enunciado respondem, cada uma isoladamente, "esse repositório é antigo?", "recebe muita contribuição?", "libera releases com frequência?", mas nenhuma delas diz, sozinha, se um repositório é *no geral* saudável e maduro. Essa inovação existe para preencher essa lacuna: resume as seis métricas num único score de 0 a 1 por repositório, permitindo comparar e ranquear os repositórios da amostra por uma nota geral de maturidade, em vez de olhar métrica por métrica (`src/analysis/health_index.py`, `scripts/compute_health_index.py`). O score é uma média ponderada das seis métricas, cada uma antes normalizada por min-max (0 a 1); os pesos refletem o quanto cada métrica sinaliza saúde/maturidade de forma direta e pouco ruidosa: PRs aceitas (25%, sinal mais direto de colaboração externa), idade (20%), releases (15%), atualização recente (15%), linguagem popular (15%) e razão de issues fechadas (10%, menor peso por variar muito entre processos de projeto). `update_frequency_days` entra invertida antes da normalização, para que "atualizado há pouco tempo" pese a favor do score, e não contra.

**Análise de correlação entre as métricas.** O grupo calculou a matriz de correlação (Pearson e Spearman) entre as seis métricas normalizadas por min-max (idade, PRs aceitas, releases, tempo desde a última atualização, razão de issues fechadas e linguagem popular), implementada em `src/analysis/correlation.py` e `scripts/compute_correlations.py`. Além da matriz completa, o script reporta explicitamente os quatro pares indicados como prioritários (idade × releases, idade × razão de issues fechadas, PRs aceitas × releases, tempo desde update × razão de issues fechadas) e gera um scatterplot com linha de tendência para todo par, entre os 15 possíveis, com `|r| de Pearson| > 0,3`. O objetivo é verificar se as métricas usadas nas RQs do enunciado, tratadas de forma isolada, escondem relações entre si que ajudem a explicar os resultados da seção 4.3, os resultados e a interpretação de cada par relevante estão na seção 4.4.

## 4. Resultados

### 4.1 Coleta de Dados

A coleta mais recente reúne 980 dos 1.000 repositórios-alvo (23/08/2026), buscados via GraphQL pelo número de estrelas. A diferença para a meta é esperada: falhas transitórias de rede/timeout na API do GitHub descartam páginas isoladas da paginação sem interromper a coleta, e o próprio ranking de estrelas muda um pouco a cada execução do script.

Das seis métricas usadas para responder as RQs, quatro não têm nenhum valor ausente porque derivam de campos sempre presentes na API (data de criação, data do último push, contagens diretas). As outras duas têm ausência real, documentada e não preenchida artificialmente:

| RQ | Métrica | Válidos | Ausentes | % ausentes | Motivo da ausência |
|---|---|---|---|---|---|
| RQ01 | Idade (dias) | 980 | 0 | 0% | — |
| RQ02 | PRs mescladas | 980 | 0 | 0% | — |
| RQ03 | Releases | 980 | 0 | 0% | — |
| RQ04 | Dias desde atualização | 980 | 0 | 0% | — |
| RQ05 | Linguagem primária | 897 | 83 | 8,5% | Repositório sem código-fonte majoritário (ex.: listas de recursos, e-books) |
| RQ06 | Razão de issues fechadas | 938 | 42 | 4,3% | Repositório sem nenhuma issue registrada (rastreador desligado ou não usado) |

Três grupos de outliers foram identificados e mantidos na amostra, com a ressalva discutida na seção 4.3: `firstcontributions/first-contributions`, com 103.516 PRs mescladas (repositório-tutorial, não comparável a projetos reais); 23 repositórios com exatamente 1000 releases, teto conhecido do campo na API do GitHub (confirmado à parte para o `electron`, que tem 1981 releases reais); e 26 repositórios com razão de issues fechadas de exatamente 100%.

A RQ07 não é uma métrica coletada à parte — é RQ02, RQ03 e RQ04 agrupadas pela linguagem da RQ05, então não tem linha própria na tabela acima. Ela usa a amostra completa de 980 repositórios sem perder nenhum: os 83 sem linguagem detectada (já contados na ausência da RQ05) não são excluídos do agrupamento, entram na categoria "Outras" junto com as linguagens de baixa frequência.

### 4.2 Visualização Gráfica

Os sete gráficos abaixo são gerados dinamicamente pelo Dashboard Exploratório, recalculados conforme os filtros de linguagem, estrelas e idade aplicados pelo usuário. Os valores citados em texto correspondem à amostra completa (980 repositórios), sem filtro.

**RQ01 — Sistemas populares são maduros/antigos?**
Histograma da idade dos repositórios, em dias desde a criação. Mediana de 2834 dias (~7,8 anos), variando de 10 a 6708 dias (~18,4 anos). Os cinco repositórios mais antigos da amostra são `rails`, `git`, `jekyll`, `redis` e `jquery`, todos criados entre 2008 e 2009.

![RQ01: Idade dos repositórios](data/Prints/rq01.png)

**RQ02 — Sistemas populares recebem muita contribuição externa?**
Boxplot (escala logarítmica) do total de pull requests mescladas. Mediana de 768 PRs. 19 repositórios (1,9%) aparecem com zero PRs, incluindo `torvalds/linux` e `FFmpeg/FFmpeg`, que usam fluxo de contribuição por lista de e-mail em vez de pull request do GitHub.

![RQ02: Contribuição externa](data/Prints/rq02.png)

**RQ03 — Sistemas populares lançam releases com frequência?**
Histograma do total de releases. Mediana geral de 37,5 releases; considerando só quem lança ao menos uma release, a mediana sobe para 95. 288 repositórios (29,4%) não têm nenhuma release.

![RQ03: Frequência de releases](data/Prints/rq03.png)

**RQ04 — Sistemas populares são atualizados com frequência?**
Histograma dos dias desde a última atualização. Mediana de 2 dias; 305 repositórios (31,1%) foram atualizados no mesmo dia da coleta. 114 repositórios (11,6%) estão parados há mais de um ano, o caso mais extremo com 2455 dias (~6,7 anos) sem atualização.

![RQ04: Frequência de atualização](data/Prints/rq04.png)

**RQ05 — Sistemas populares são escritos nas linguagens mais populares?**
Gráfico de barras da distribuição de linguagens primárias, comparada ao ranking GitHub Octoverse 2025. 43 linguagens distintas identificadas. Top 3: Python (23,0%), TypeScript (17,3%) e JavaScript (11,1%), 51,4% acumulado.

![RQ05: Linguagem](data/Prints/rq05.png)

**RQ06 — Sistemas populares possuem um alto percentual de issues fechadas?**
Histograma da razão entre issues fechadas e total de issues. Mediana de 87,5%, mínimo de 7,6%, máximo de 100%.

![RQ06: Issues fechadas](data/Prints/rq06.png)

**RQ07 — Sistemas escritos em linguagens mais populares recebem mais contribuição externa, lançam mais releases e são atualizados com mais frequência?**
Três gráficos de barras (PRs mescladas, releases e dias desde atualização, cada um com mediana por linguagem, top 10 + "Outras"). Comparando as 5 linguagens do GitHub Octoverse 2025 (TypeScript, Python, JavaScript, Java, C#) contra o restante: mediana de 912 PRs mescladas contra 646, 50 releases contra 27, e 2 dias desde a última atualização contra 3. Rust (2217) e TypeScript (2091) têm a maior mediana de PRs mescladas entre todas as linguagens, acima até de Python (500), a mais frequente na amostra.

![RQ07: Contribuição, releases e atualização por linguagem](data/Prints/rq07.png)

### 4.3 Discussão

**RQ01 — hipótese confirmada.** A mediana de ~7,8 anos e a concentração dos cinco repositórios mais antigos (2008-2009) entre os mais populares sustentam a expectativa de que popularidade se acumula ao longo do tempo. Ressalva: existe uma cauda de repositórios recém-criados (o mais novo tem 10 dias de existência), sinal de que picos de interesse pontuais, como lançamentos ligados a IA, também conseguem entrar rapidamente no top 1000, sem esperar anos de exposição.

**RQ02 — hipótese confirmada.** A mediana de 768 PRs mescladas indica volume relevante de contribuição externa. Ameaça à validade: a métrica subestima colaboração em projetos que não usam o fluxo de pull request do GitHub (`linux`, `FFmpeg`, zero PRs registrados apesar de serem projetos ativos), e o outlier `first-contributions` (103.516 PRs, repositório-tutorial) precisa ser excluído de qualquer análise agregada por média, sob risco de distorcer a conclusão.

**RQ03 — hipótese parcialmente confirmada.** A mediana condicionada a quem lança ao menos uma release (95) sustenta a ideia de cadência estruturada entre quem usa o recurso, mas 29,4% da amostra não lança nenhuma release, contrariando a expectativa de que a maioria adotaria ciclos formais de versionamento (muitos desses são listas de recursos ou material de referência, que popularizam sem seguir um processo de release tradicional). O teto de 1000 no campo, confirmado à parte para o `electron`, é uma ameaça à validade real: a mediana geral (37,5) é subestimada para os projetos mais ativos, que provavelmente ultrapassam esse valor.

**RQ04 — hipótese confirmada.** A mediana de apenas 2 dias e quase um terço da amostra (31,1%) atualizada no mesmo dia da coleta mostram manutenção ativa na maioria dos projetos populares. A minoria parada há mais de um ano (11,6%) reforça a hipótese em vez de contradizê-la: em geral são materiais de referência estáticos (livros, roadmaps), não projetos de software que exigiam manutenção contínua e a perderam.

**RQ05 — hipótese confirmada parcialmente.** Usando o GitHub Octoverse 2025 como referência, Python, TypeScript e JavaScript concentram 51,4% da amostra e ocupam as três primeiras posições também no ranking de referência, confirmando a expectativa central. Mas a ordem interna diverge (Python é 1º na amostra e 2º na referência) e duas linguagens de peso corporativo no Octoverse, Java (4º na referência, 8º na amostra, 4,0%) e C# (5º na referência, 16º na amostra, 0,8%), aparecem bem abaixo do esperado, indício de que popularidade por estrelas no GitHub favorece ecossistemas de scripting, web e IA mais do que linguagens tipicamente usadas em software corporativo fechado.

**RQ06 — hipótese confirmada.** A mediana de 87,5% de issues fechadas é uma taxa alta, sustentando a expectativa de que repositórios populares recebem atenção de manutenção suficiente para resolver a maioria dos problemas relatados. Ressalva dupla: repositórios sem nenhuma issue registrada (4,3%) ficam fora do cálculo, incluindo casos como o `linux`, que desliga deliberadamente o rastreador de Issues do GitHub; e 2,7% da amostra tem razão de exatamente 100%, incluindo repositórios com milhares de issues todas fechadas, o que sugere bots de triagem automática ou política agressiva de fechamento, não necessariamente resolução manual de cada problema.

**RQ07 — hipótese confirmada.** Repositórios em linguagens populares (top 5 do GitHub Octoverse 2025: TypeScript, Python, JavaScript, Java, C#) superam o restante da amostra nas três métricas: mediana de 912 PRs mescladas contra 646 (+41%), 50 releases contra 27 (quase o dobro), e 2 dias desde a última atualização contra 3. A diferença é mais forte em releases e mais fraca em frequência de atualização, onde a mediana geral já é baixa (2-3 dias) pra quase toda a amostra, sobrando pouca margem pra diferença aparecer. Olhando linguagem a linguagem, não só popular vs. resto, o próprio grupo "popular" está longe de ser uniforme: Rust e TypeScript têm mediana de PRs mescladas (2217 e 2091) bem acima até de Python (500), a linguagem mais frequente da amostra. Ressalva: a comparação é uma correlação, não uma relação causal — linguagens do Octoverse também tendem a pertencer a ecossistemas com mais automação de release (ex.: semantic-release, comum no mundo JS/TS), o que pode explicar parte da diferença em RQ03 independentemente da popularidade da linguagem em si.

**Ameaças à validade gerais.** Os dados são um retrato de um único instante (23/08/2026): o ranking de estrelas, a contagem de releases e a razão de issues fechadas mudam continuamente, então uma nova coleta produz números levemente diferentes dos aqui reportados, como já observado entre coletas anteriores do grupo. O teto de 1000 no campo `releases` e os projetos que não usam o fluxo nativo de pull request do GitHub são limitações da própria API, não do método de coleta do grupo. O Octoverse 2025 mede popularidade de linguagem no GitHub como um todo, não especificamente entre os repositórios mais populares, então a comparação da RQ05 é uma aproximação.

As inovações do grupo, detalhadas na seção 3.6, aprofundam esses resultados combinando as seis métricas num índice único de saúde/maturidade por repositório e cruzando-as par a par numa matriz de correlação; a discussão específica de cada uma é apresentada naquela seção e, em mais detalhe, a seguir em 4.4 (correlação) e 4.5 (índice de saúde/maturidade).

### 4.4 Análise de Correlação entre Métricas

Matriz de correlação de Pearson entre as seis métricas normalizadas por min-max (`update_frequency_days` invertida antes da normalização, como no índice de saúde, de modo que valor alto = atualização mais recente):

| | Idade | PRs aceitas | Releases | Atualização recente | Issues fechadas | Linguagem popular |
|---|---|---|---|---|---|---|
| **Idade** | 1,00 | 0,21 | 0,04 | -0,11 | 0,24 | -0,14 |
| **PRs aceitas** | 0,21 | 1,00 | 0,33 | 0,15 | 0,16 | -0,04 |
| **Releases** | 0,04 | 0,33 | 1,00 | 0,20 | 0,24 | 0,05 |
| **Atualização recente** | -0,11 | 0,15 | 0,20 | 1,00 | 0,32 | 0,01 |
| **Issues fechadas** | 0,24 | 0,16 | 0,24 | 0,32 | 1,00 | 0,04 |
| **Linguagem popular** | -0,14 | -0,04 | 0,05 | 0,01 | 0,04 | 1,00 |

A matriz de Spearman segue o mesmo formato; os valores usados no texto abaixo vêm dela quando divergem do Pearson.

**Pares solicitados pela issue #33:**

- **Idade × Releases**: r=0,04, ρ=0,06 — correlação praticamente nula. Repositórios mais antigos não lançam sistematicamente mais releases: idade sozinha não é um bom preditor de cadência de versionamento (consistente com a ressalva da RQ03, onde 29,4% da amostra nunca lança release, independente de quanto tempo existe).
- **Idade × Razão de issues fechadas**: r=0,24, ρ=0,24 — correlação positiva fraca. Repositórios mais antigos tendem a ter uma razão de issues fechadas um pouco maior, possivelmente por terem tido mais tempo para amadurecer processo de triagem, mas o efeito é pequeno demais para ser a explicação principal da alta mediana observada na RQ06 (87,5%).
- **PRs aceitas × Releases**: r=0,33, ρ=0,59 — correlação positiva fraca a moderada, com divergência relevante entre os dois coeficientes. A diferença indica que a relação é mais monotônica do que linear (esperado, já que ambas as métricas têm distribuição bastante assimétrica, com poucos repositórios concentrando valores muito altos): projetos que recebem mais contribuição externa mesclada tendem a lançar mais releases, mas não numa proporção constante.
- **Atualização recente × Razão de issues fechadas**: r=0,32, ρ=0,30 — correlação positiva fraca. Como a métrica de atualização foi invertida (valor alto = atualização mais recente), o resultado indica que repositórios atualizados mais recentemente tendem a fechar uma fração maior de suas issues — coerente com a ideia de manutenção ativa incluir também o fechamento de issues, não só commits/releases.

**Pares com `|r|` de Pearson `> 0,3`** (os dois únicos entre os 15 possíveis; scatterplots gerados por `scripts/compute_correlations.py` em `reports/figures/`):

**PRs aceitas × Releases**

![Correlação entre PRs aceitas e Releases](reports/figures/corr_merged_pull_requests_x_releases.png)

PRs aceitas e Releases apresentam correlação positiva fraca a moderada (Pearson r=0,33, Spearman ρ=0,59): colaboração externa e cadência de release andam juntas na amostra, mas de forma não estritamente linear — a maior parte dos repositórios se concentra em valores normalizados baixos de ambas as métricas, com uma cauda de poucos projetos muito ativos em ambas.

**Atualização recente × Razão de issues fechadas**

![Correlação entre atualização recente e razão de issues fechadas](reports/figures/corr_update_frequency_days_x_closed_issues_ratio.png)

Atualização recente e razão de issues fechadas apresentam correlação positiva fraca (Pearson r=0,32, Spearman ρ=0,30): repositórios com atualização mais recente tendem a fechar uma fração maior das suas issues, sugerindo que times ativos tratam commits/releases e a fila de issues como parte do mesmo ciclo de manutenção, em vez de tratar um e negligenciar o outro.

**Leitura geral.** Nenhum dos pares da matriz passa de correlação moderada (`|r|` máximo de 0,33 no Pearson), o que reforça que as seis métricas usadas nas RQs do enunciado capturam, em grande parte, dimensões distintas da popularidade/maturidade de um repositório — nenhuma delas é redundante o suficiente para ser descartada em favor de outra. Isso também justifica, a posteriori, a escolha de combiná-las por média ponderada (em vez de descartar alguma por colinearidade) no índice de saúde/maturidade da seção 3.6.

### 4.5 Índice Composto de Saúde/Maturidade

Índice único (0 a 1) combinando as seis métricas normalizadas por min-max por média ponderada, implementado em `src/analysis/health_index.py` e gerado por `python -m scripts.compute_health_index`:

| Métrica | Peso | Justificativa |
|---|---|---|
| PRs aceitas | 25% | Maior peso: sinal mais direto de colaboração externa |
| Idade | 20% | Projeto estabelecido, popularidade sustentada |
| Releases | 15% | Cadência de versionamento |
| Atualização recente | 15% | Manutenção ativa (invertida: menos dias desde a última atualização = melhor) |
| Linguagem popular | 15% | Binário: repositório está ou não no top 5 do GitHub Octoverse 2025 |
| Issues fechadas | 10% | Menor peso: sinal mais ruidoso, varia muito entre processos de projeto |

Quando falta um dado no repositório (ex.: sem linguagem detectada ou sem issues registradas), a métrica é excluída e os pesos das demais são renormalizados, em vez de penalizar o repositório com o pior valor possível.

![Distribuição do índice de saúde/maturidade](reports/figures/health_index_distribuicao.png)

Mediana de 0,418, média de 0,421, distribuição aproximadamente simétrica em torno da mediana, sem nenhum repositório da amostra ficando sem score.

**Top 5 (maior índice):** `home-assistant/core` (0,905), `elastic/elasticsearch` (0,840), `getsentry/sentry` (0,810), `grafana/grafana` (0,796), `frappe/erpnext` (0,783). São repositórios que pontuam bem nas seis métricas ao mesmo tempo: antigos, com alto volume de PRs mescladas, releases frequentes, atualização recente e linguagem popular.

**Bottom 5 (menor índice):** `facebookresearch/segment-anything` (0,163), `CompVis/stable-diffusion` (0,166), `anthropics/prompt-eng-interactive-tutorial` (0,167), `karpathy/LLM101n` (0,171), `exacity/deeplearningbook-chinese` (0,172). Predominam repositórios de pesquisa ou tutorial de IA publicados uma vez e sem manutenção contínua depois: poucas ou nenhuma release e atualização parada, com o `deeplearningbook-chinese` já citado na RQ04 por mais de 6 anos sem update.

**Leitura geral.** A escolha de combinar as seis métricas por média ponderada, em vez de descartar alguma por redundância, é sustentada pela análise de correlação da seção 4.4: nenhum par de métricas passa de correlação moderada (`|r|` máximo de 0,33), então cada uma contribui com um sinal distinto para o índice em vez de repetir a mesma informação. O peso mais alto (PRs aceitas, 25%) e o mais baixo (issues fechadas, 10%) refletem uma escolha justificada do grupo, não um resultado estatístico; testar o índice com pesos iguais (1/6 cada) como baseline alternativo é uma extensão natural para trabalho futuro.

## 5. Conclusão

*ORIENTAÇÃO: Sintetize, em poucos parágrafos, as respostas a todas as RQs (enunciado + inovação do grupo), sem repetir números já discutidos em detalhe — o objetivo aqui é a mensagem final, não os dados brutos. Aponte as principais limitações do estudo (tamanho de amostra, ameaças à validade não mitigadas, período de coleta). Quando o enunciado pedir explicitamente uma postura de consultoria (caso do Lab05, que pede recomendações de melhoria de processo "como se o grupo fosse consultoria para um time real"), inclua recomendações objetivas e acionáveis, não genéricas. Encerre indicando o que o grupo faria diferente com mais tempo ou recursos, e quais das inovações propostas (30%) valeriam a pena expandir em um trabalho futuro.*

*[conteúdo do grupo — substituir este texto]*

## 5. Referências

- ZUSE, Horst. A framework of software measurement. Walter de Gruyter, 2013.
- GitHub Octoverse 2025 - ranking de linguagens mais populares, referência da RQ05. 
