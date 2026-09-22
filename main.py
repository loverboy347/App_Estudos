import argparse,json
from engine.database import init_db,insert
from engine.pipeline import discover,candidates_for_review,review

p=argparse.ArgumentParser(description="Study Question Engine")
s=p.add_subparsers(dest="cmd")
s.add_parser("init")
d=s.add_parser("discover"); d.add_argument("--per-query",type=int,default=8)
z=s.add_parser("select"); z.add_argument("--amount",type=int,default=10)
s.add_parser("review")
j=s.add_parser("import-json"); j.add_argument("file")
a=p.parse_args()

if a.cmd=="init":
    init_db(); print("Banco inicializado.")
elif a.cmd=="discover":
    print(discover(a.per_query))
elif a.cmd=="select":
    for i,q in enumerate(candidates_for_review(a.amount),1):
        print(f"{i}. ID {q['id']} | {q['discipline']} | {q['topic']} | {q['qtype']} | {q['source_url']}")
elif a.cmd=="review":
    review(10)
elif a.cmd=="import-json":
    init_db()
    data=json.load(open(a.file,encoding="utf8"))
    for q in data: insert(q)
    print(f"{len(data)} questões importadas.")
else:
    p.print_help()
