from collections import Counter

def distribution(rows):
    subject=Counter(); topic=Counter(); qtype=Counter()
    for r in rows:
        if r["status"]=="approved":
            subject[r["discipline"]]+=1
            if r["topic"]:topic[(r["discipline"],r["topic"])]+=1
            qtype[r["qtype"]]+=1
    return subject,topic,qtype

def score(c,approved,config):
    s,t,q=distribution(approved)
    subjects=list(config["subjects"])
    mean=sum(s[x] for x in subjects)/max(len(subjects),1)
    sg=max(0,mean-s[c["discipline"]])/max(mean,1)

    topics=config["subjects"][c["discipline"]]["topics"]
    tm=sum(t[(c["discipline"],x)] for x in topics)/max(len(topics),1)
    tg=max(0,tm-t[(c["discipline"],c.get("topic"))])/max(tm,1)

    type_gap=1/(q.get(c["qtype"],0)+1)
    return .55*sg+.40*tg+.05*type_gap

def select(candidates,approved,config,n=10):
    pool=list(candidates); work=list(approved); out=[]
    for _ in range(n):
        if not pool:break
        best=max(pool,key=lambda x:score(x,work,config))
        out.append(best); work.append(best); pool.remove(best)
    return out
