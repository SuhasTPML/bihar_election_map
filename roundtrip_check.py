import json, pathlib, subprocess, sys

base = pathlib.Path('.')
pairs = [
    ('parties.json','parties.csv','parties.rt.json'),
    ('bihar_election_results_consolidated.json','bihar_election_results_consolidated.csv','bihar_election_results_consolidated.rt.json'),
]

all_ok = True
for jname, cname, outj in pairs:
    j = base/jname
    cj = json.loads(j.read_text(encoding='utf-8'))
    subprocess.check_call([sys.executable, 'json_to_csv.py', jname])
    subprocess.check_call([sys.executable, 'csv_to_json.py', cname])
    rt_json = base/jname
    (base/outj).write_text(rt_json.read_text(encoding='utf-8'), encoding='utf-8')
    cj2 = json.loads((base/outj).read_text(encoding='utf-8'))
    eq = (cj == cj2)
    print(f"{jname} round-trip equal: {eq}")
    if not eq:
        if isinstance(cj, list) and isinstance(cj2, list) and len(cj)==len(cj2):
            for i,(a,b) in enumerate(zip(cj,cj2)):
                if a!=b:
                    print('First diff at index', i)
                    ka, kb = set(a.keys()), set(b.keys())
                    print('keys only in A:', sorted(ka-kb))
                    print('keys only in B:', sorted(kb-ka))
                    for k in sorted(ka&kb):
                        if a[k]!=b[k]:
                            print('field diff', k, a[k], '!=', b[k])
                            break
                    break
        all_ok=False
print('ALL_OK', all_ok)

