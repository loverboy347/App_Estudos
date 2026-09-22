import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENGINE_DIR = ROOT / "study_question_engine_FINAL_v1_0" / "study_question_engine_final"
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

from engine.database import init_db, insert


def load_json_array(path: Path):
    data = json.loads(path.read_text(encoding="utf8"))
    if isinstance(data, list):
        return data
    raise ValueError(f"Arquivo {path} não contém uma lista JSON")


def load_js_array(path: Path):
    text = path.read_text(encoding="utf8")
    match = re.search(r"\[(.*)\]\s*;?\s*$", text, re.S)
    if not match:
        raise ValueError(f"Não foi possível extrair array JS de {path}")
    payload = match.group(0)
    # keep only the contents between the first '[' and the last ']'
    start = payload.find("[")
    end = payload.rfind("]")
    return json.loads(payload[start:end + 1])


def normalize_question(item, source_name, default_discipline):
    qtype = "somatoria" if item.get("mode") == "sum" or isinstance(item.get("a"), list) else "multipla_escolha"
    alternatives = item.get("o") or []
    answer = item.get("a")
    if isinstance(answer, list):
        answer = ",".join(str(int(v)) for v in answer)
    elif isinstance(answer, (int, float)):
        answer = str(int(answer))
    else:
        answer = str(answer or "")

    return {
        "id": item.get("id"),
        "disciplina": item.get("discipline") or default_discipline,
        "tema": item.get("topic") or "Geral",
        "subtema": None,
        "instituicao": "Banco local",
        "tipo": qtype,
        "numero_original": str(item.get("id") or ""),
        "fonte": f"local://{source_name}",
        "source_title": item.get("s") or source_name,
        "gabarito": answer,
        "enunciado": item.get("q") or "",
        "afirmativas": [
            {"numero": idx + 1, "texto": alt}
            for idx, alt in enumerate(alternatives)
        ] if qtype in {"somatoria", "verdadeiro_falso"} else [],
        "alternativas": alternatives,
        "imagem": item.get("img"),
        "observacoes": f"Importado do banco local: {source_name}",
        "status": "candidate",
    }


def main():
    init_db()
    imported = []
    for filename, loader, discipline in [
        ("questions.json", load_json_array, "Biologia"),
        ("historia_questions.js", load_js_array, "História"),
    ]:
        path = ROOT / filename
        if not path.exists():
            print(f"Pulando {path}: arquivo não encontrado.")
            continue
        rows = loader(path)
        for item in rows:
            imported.append(normalize_question(item, filename, discipline))

    for question in imported:
        insert(question)

    print(f"{len(imported)} questões do banco local importadas para o engine.")


if __name__ == "__main__":
    main()
