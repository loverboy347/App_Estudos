QUESTION_TYPES = {
    "multipla_escolha",
    "somatoria",
    "verdadeiro_falso",
    "associacao",
}

REQUIRED = [
    "disciplina","tema","instituicao","tipo","fonte",
    "gabarito","enunciado","afirmativas","alternativas"
]

def validate(q):
    errors=[]
    for k in REQUIRED:
        if k not in q or q[k] in (None,""):
            errors.append(f"campo ausente: {k}")

    if q.get("tipo") not in QUESTION_TYPES:
        errors.append("tipo de questão inválido")

    if q.get("tipo")=="somatoria":
        if not isinstance(q.get("afirmativas"),list) or not q["afirmativas"]:
            errors.append("somatória precisa de afirmativas")

    if q.get("tipo")=="multipla_escolha":
        if len(q.get("alternativas",[])) < 2:
            errors.append("múltipla escolha precisa de alternativas")

    if q.get("tipo")=="verdadeiro_falso":
        if not q.get("afirmativas"):
            errors.append("verdadeiro/falso precisa de afirmativas")

    if len(q.get("enunciado","")) < 30:
        errors.append("enunciado muito curto")

    return errors
