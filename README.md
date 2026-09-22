# Study Question Engine — FINAL v1.0

Motor universal da plataforma de estudos.

## Objetivo

Pesquisar questões na internet, extrair uma questão real, converter para o formato
universal do banco, validar, detectar duplicatas, classificar disciplina/tema/subtema,
calcular as lacunas do banco e selecionar 10 candidatas para revisão humana.

A decisão final continua sendo humana: a questão só entra como `approved` depois de você
aceitá-la.

## Formato universal da questão

Cada questão possui:

- ID
- DISCIPLINA
- TEMA
- SUBTEMA
- INSTITUIÇÃO
- TIPO
- NÚMERO ORIGINAL
- FONTE
- GABARITO
- ENUNCIADO
- AFIRMATIVAS
- ALTERNATIVAS
- IMAGEM
- OBSERVAÇÕES
- STATUS

Tipos previstos:
- `multipla_escolha`
- `somatoria`
- `verdadeiro_falso`
- `associacao`

O formato foi separado do buscador: trocar a fonte da internet não muda o banco nem
o algoritmo de distribuição.

## Instalação

Python 3.11+:

```bash
pip install -r requirements.txt
```

Inicializar:

```bash
python main.py init
```

Pesquisar candidatos:

```bash
python main.py discover --per-query 8
```

Selecionar 10:

```bash
python main.py select --amount 10
```

Revisar:

```bash
python main.py review
```

## Importar questões já estruturadas

Também existe:

```bash
python main.py import-json arquivo.json
```

O arquivo precisa conter uma lista no formato de `sample_question.json`.

## Observação

A extração automática é conservadora. O sistema não inventa gabarito, alternativa ou
texto. Se não conseguir comprovar a estrutura mínima, a página não é promovida para
candidata.

A busca na internet deve respeitar direitos autorais, termos de uso e robots.txt das
fontes. O banco guarda a URL da fonte e os metadados necessários para rastreabilidade.
