"""Build data/odm.json from an AAP Critical Report CSV export.

Usage: python3 tools/build_odm.py path/to/AAP_Critical_Report_YYYYMMDDhhmmss.csv
The CSV itself is never committed; only the per-supplier summary is.
"""
import json, re, sys, os
from collections import Counter, defaultdict
import pandas as pd

INTERNAL = {'ACER', 'ACER WW LOCAL PM', 'LOCAL SOURCE'}   # sourcing codes that are not outside suppliers
SKIP = {'N', 'N/A', ''}
SITE_SUFFIX = re.compile(r'-(TH|VN|BH|SG|SH)$')

def company(code):
    head = code.split('/')[0]
    return SITE_SUFFIX.sub('', head).strip()

def main(src):
    stamp = re.search(r'(\d{8})', os.path.basename(src))
    d = pd.read_csv(src, encoding='utf-8-sig', low_memory=False)
    rows = d[d['ODM'].notna()]
    acc = defaultdict(lambda: {'codes': Counter(), 'parts': set(), 'shared': set(), 'pl': Counter(), 'cat': Counter(),
                               'stage': Counter(), 'proj': set(), 'd26': 0, 'gls': 0, 'onhand': 0, 'onorder': 0})
    col = {name: i for i, name in enumerate(d.columns)}
    STAGE, PN, ONHAND, ONORDER, GLS, D26 = (col[k] for k in ('Stage (Current)', 'Part Number', 'On Hand New', 'On Order',
                                                          'GLS recommendation M0', 'Last 26 Wks Demand QTY'))
    CAT, PROJ, PL = col['Part Category Group (PC8)'], col['Project'], col['Custom Product Line (PC7)']
    for r in rows.itertuples(index=False):
        codes = sorted({c.strip().upper() for c in str(r.ODM).split(';')} - SKIP)
        comps = {company(c) for c in codes}
        for comp in comps:
            a = acc[comp]
            pn = r[PN]
            if pn in a['parts']:
                continue
            a['parts'].add(pn)
            if len(comps) > 1: a['shared'].add(pn)
            for c in codes:
                if company(c) == comp: a['codes'][c] += 1
            if isinstance(r[PL], str): a['pl'][r[PL]] += 1
            if isinstance(r[CAT], str): a['cat'][r[CAT]] += 1
            a['stage'][str(r[STAGE]).upper() if isinstance(r[STAGE], str) else 'BLANK'] += 1
            if isinstance(r[PROJ], str):
                for p in r[PROJ].split(';'):
                    if p.strip(): a['proj'].add(p.strip())
            a['d26'] += int(r[D26] or 0); a['gls'] += int((r[GLS] or 0) > 0)
            a['onhand'] += int(r[ONHAND] or 0); a['onorder'] += int(r[ONORDER] or 0)
    out = []
    for comp, a in acc.items():
        out.append({
            'id': 'odm-' + re.sub(r'[^a-z0-9]+', '-', comp.lower()).strip('-'),
            'name': comp,
            'type': 'internal' if comp in INTERNAL else 'odm',
            'codes': dict(a['codes'].most_common()),
            'parts': len(a['parts']),
            'sharedParts': len(a['shared']),
            'projects': len(a['proj']),
            'productLines': dict(a['pl'].most_common(6)),
            'categories': dict(a['cat'].most_common(6)),
            'stages': dict(a['stage'].most_common()),
            'demand26w': a['d26'],
            'partsWithGlsM0': a['gls'],
            'onHandNew': a['onhand'],
            'onOrder': a['onorder'],
        })
    out.sort(key=lambda x: -x['parts'])
    name = re.search(r'AAP_Critical_Report_\d+\.csv', os.path.basename(src))
    meta = {'source': name.group(0) if name else os.path.basename(src), 'reportDate': stamp.group(1) if stamp else None,
            'rows': int(len(d)), 'rowsWithOdm': int(len(rows))}
    with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'odm.json'), 'w', encoding='utf-8') as f:
        json.dump({'meta': meta, 'suppliers': out}, f, ensure_ascii=False, indent=1)
    print(f"{len(out)} suppliers from {len(rows):,} rows")

if __name__ == '__main__':
    main(sys.argv[1])
