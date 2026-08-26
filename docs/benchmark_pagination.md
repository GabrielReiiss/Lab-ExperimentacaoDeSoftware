# Benchmark: paginação adaptativa vs. page_size fixo

**Data:** 26/08/2026
**Scripts:** `scripts/benchmark_pagination.py --total N`, `scripts/experimental/collect_beyond_1000.py --total N [--max-stars N]`, `scripts/diagnose_adaptive.py --total N`
**Query:** `TOP_REPOSITORIES_QUERY` (RQ01-06 unificadas), `stars:>1 sort:stars-desc`

Reproduzível a qualquer momento com os comandos acima. Histórico completo de investigação (diagnóstico, bugs encontrados, correções aplicadas) no apêndice, no final deste arquivo.

## Metodologia

Duas estratégias de paginação, comparadas coletando o mesmo volume de repositórios:

1. **Adaptativa** (`paginate()`, início em `page_size=10`): cresce/encolhe automaticamente conforme sequências de sucesso/falha da API (ver 3.2 do relatório).
2. **Fixa, `page_size=10`**: valor confirmado seguro por teste manual.

(Uma 3ª estratégia, fixa em `page_size=50`, foi usada só na fase de investigação: sempre falha, ver apêndice.)

## Resultado final

### No topo do ranking (repositórios mais populares)

| N | Adaptativa | Fixa (10) | Razão |
|---|---|---|---|
| 100 | 61,0 s | 46,5 s | 1,31x |
| 500 | 258,8 s | 232,9 s | 1,11x |
| 1.000 | 478,2 s | 460,7 s | **1,038x** |
| 2.700 (via 3 faixas de `stars:`, script `collect_beyond_1000.py`) | 1.170,7 s | 1.111,1 s | 1,05x |

Na escala real da coleta oficial (N=1.000), a adaptativa é só ~4% mais lenta, diferença pequena o bastante pra não ser o critério decisivo por si só. Persiste em N=2.700, via particionamento por `stars:` (a API de busca do GitHub limita cada consulta a ~1.000 resultados; detalhes no apêndice).

Uma diferença que não é sobre velocidade: a fixa bateu **1.000/1.000** repositórios nas três medições em N=1.000; a adaptativa ficou sempre um pouco abaixo (980, 995, 985), 3 execuções independentes com o mesmo padrão, relacionado a como cada estratégia interage com o teto de resultados da API perto do limite.

### Em repositórios menos populares (teto de estrelas ≤500)

Hipótese testada: repositórios com menos estrelas tendem a ser menos complexos (menos PRs/issues pra computar), então o algoritmo adaptativo deveria performar melhor neles, crescendo o `page_size` além do que é seguro no topo do ranking.

| `--max-stars` | Repos coletados | Adaptativa | Fixa (10) | Razão |
|---|---|---|---|---|
| 500 | 2.391 | 604,3 s | 633,1 s | **0,95x** |
| 400 | 2.006 | 489,7 s | 557,0 s | **0,88x** |
| 300 | 2.189/2.187 | 551,3 s | 603,1 s | **0,914x** |
| 250 | 2.346 | 597,8 s | 648,1 s | **0,92x** |

**Hipótese confirmada, com ressalva:** nas quatro medições a adaptativa venceu (oposto do topo do ranking): pelo log, o `page_size` cresceu de forma estável até 40-45 nessas faixas, contra ~10-25 no topo, mais que o dobro do lote processável por requisição. Mas a relação não é uma reta contínua ("quanto menos popular, sempre melhor"): os quatro pontos oscilam entre 0,88x-0,95x sem tendência clara de melhorar ainda mais abaixo de 500. Parece mais um **degrau** (populações caras → fixa vence/empata; populações baratas → adaptativa vence por margem ~5-12%) do que uma inclinação contínua. Confirmar isso exigiria repetir alguma faixa pra separar ruído de execução única de tendência real, não foi feito.

Abaixo de `max_stars≈220-250`, a densidade de repositórios por valor de estrela ultrapassa o que dá pra particionar com segurança (`safe_max_per_range=900`): precisaria de um segundo critério de partição (ex.: faixa de data de criação), não implementado.

---

## Apêndice: histórico de investigação

### 1. Resultado inicial: contraintuitivo

Antes de qualquer correção, a adaptativa era **2-4x mais lenta** que a fixa seguro em todas as escalas (N=100: 190,5s/4,0x; N=500: 512,3s/2,3x; N=1.000: 865,1s/2,0x, parando em 980/1.000). A fixa em `page_size=50` sempre falhou (502/504 consistente). Investigamos a causa em vez de aceitar o número.

### 2. Diagnóstico e correção 1: retry duplicado em duas camadas

`scripts/diagnose_adaptive.py` (instrumentação por monkeypatch, sem mudar comportamento) mostrou que 66% do tempo de uma execução em N=100 era gasto em requisições que falhavam. Causa: `run_query()` já tentava 3x sozinho em erro 502/503/504, e `paginate()` tentava o mesmo `page_size` mais 3x por cima disso antes de encolher: 9 requisições reais pra uma única decisão. **Correção:** removido o retry de 502/503/504 do `run_query()` (só `paginate()`, que sabe *o que* mudar, trata esse caso agora). Resultado: N=100 190,5s→93,9s (4,0x→2,0x); N=500 512,3s→325,3s (2,3x→1,37x); N=1.000 865,1s→607,8s (2,0x→1,33x).

### 3. Correção 2: encolher na 1ª falha, não na 3ª

Mesmo padrão de desperdício, uma camada acima: `paginate()` exigia 3 falhas confirmadas no mesmo `page_size` antes de encolher. Reduzido pra 1 (`FAILURE_STREAK_TO_SHRINK=1`, testado com 2 execuções de confirmação, ~26% mais rápido que o baseline). Com as duas correções: N=100 **61,0s (1,31x)**; N=500 **258,8s (1,11x)**; N=1.000 **478,2s (1,038x)**, melhora total de 45-68% sobre o resultado original.

### 4. O teto de ~1.000 é real, não artefato do script

Testado pedindo `total=1050` com `page_size=10` fixo (força o script a perguntar além de 1.000): resultado foi exatamente 1.000, `hasNextPage: False` genuíno do GitHub, não um efeito do critério de parada do script. A API de busca do GitHub limita cada consulta a ~1.000 resultados acessíveis via paginação: não é sobre quantos repositórios existem (`stars:>1` tem milhões), é sobre quantos uma única execução de busca deixa percorrer. Não existe forma de retomar a mesma lista além disso; a única saída é particionar em buscas diferentes (`stars:` sem sobreposição), cada uma com seu próprio orçamento de 1.000, é isso que `scripts/experimental/collect_beyond_1000.py` faz.
