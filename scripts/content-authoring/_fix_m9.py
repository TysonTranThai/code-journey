#!/usr/bin/env python3
"""Fix m9: envelope test (drop 503), validate-user ordering — JSON tests + ledger."""
import io
import json

BASE = "src/content/tracks/python/courses/python-advanced/modules/production-apis/practices"
LEDGER = "scripts/content-authoring/py-solutions.mjs"

# 1. pa-api-error-envelope: replace test-1 code (503 not in the fixed title table).
p1 = BASE + "/pa-p9-design-practice/challenges/pa-api-error-envelope.json"
d1 = json.load(io.open(p1, encoding="utf-8"))
t1 = d1["tests"][0]
assert "503" in t1["code"], t1["code"][:80]
t1["code"] = (
    "assert error_envelope(422, 'email is not valid', 'email') == "
    "{'error': {'status': 422, 'title': 'validation_failed', 'field': 'email', 'detail': 'email is not valid'}}\n"
    "assert error_envelope(404, 'no such widget')['error']['title'] == 'not_found'\n"
    "assert error_envelope(500, 'secrets: ConnectionRefused at db-7')['error']['detail'] == 'an unexpected error occurred'\n"
    "assert error_envelope(500)['error'] == {'status': 500, 'title': 'internal_error', 'detail': 'an unexpected error occurred'}\n"
    "print('ok')"
)
io.open(p1, "w", encoding="utf-8").write(json.dumps(d1, indent=2, ensure_ascii=False) + "\n")

# 2. pa-api-validate-user: replace test-2 code (sorted expectations + payload with a valid name).
p2 = BASE + "/pa-p9-validation-practice/challenges/pa-api-validate-user.json"
d2 = json.load(io.open(p2, encoding="utf-8"))
t2 = d2["tests"][1]
assert "extra" in t2["code"], t2["code"][:80]
t2["code"] = (
    "clean, errors = validate_user({'name': 'Lan', 'email': 'nope', 'age': 999, 'extra': 1, 'zz': 2})\n"
    "assert clean == {'name': 'Lan'}\n"
    "fields = [e['field'] for e in errors]\n"
    "assert fields == ['age', 'email', 'extra', 'zz'], fields\n"
    "missing = validate_user({})\n"
    "assert [e['field'] for e in missing[1]] == ['age', 'email', 'name']\n"
    "print('ok')"
)
# spec: declare the sorting contract too
d2["prompt"] = d2["prompt"].replace(
    "The contract: report ALL problems in one call (collect, don't abort at the first).",
    "The final error list is sorted by field name.\n\n"
    "The contract: report ALL problems in one call (collect, don't abort at the first).",
)
io.open(p2, "w", encoding="utf-8").write(json.dumps(d2, indent=2, ensure_ascii=False) + "\n")

# 3. Ledger: rebuild the LAST R/W entry for the two ids.
src = io.open(LEDGER, encoding="utf-8").read()

validate_ref = (
    "def validate_user(payload):\n"
    "    clean, errors = {}, []\n"
    "    name = payload.get('name')\n"
    "    if not isinstance(name, str) or not name.strip():\n"
    "        errors.append({'field': 'name', 'detail': 'name is required'})\n"
    "    else:\n"
    "        clean['name'] = name.strip()\n"
    "    email = payload.get('email')\n"
    "    if not isinstance(email, str) or '@' not in email:\n"
    "        errors.append({'field': 'email', 'detail': 'email must contain @'})\n"
    "    else:\n"
    "        clean['email'] = email.strip().lower()\n"
    "    age = payload.get('age')\n"
    "    if isinstance(age, str) and age.strip().isdigit():\n"
    "        age = int(age)\n"
    "    if not isinstance(age, int) or isinstance(age, bool) or not (0 <= age <= 150):\n"
    "        errors.append({'field': 'age', 'detail': 'age must be an integer 0..150'})\n"
    "    else:\n"
    "        clean['age'] = age\n"
    "    unknown = set(payload) - {'name', 'email', 'age'}\n"
    "    for field in sorted(unknown):\n"
    "        errors.append({'field': field, 'detail': 'unknown field'})\n"
    "    errors.sort(key=lambda e: e['field'])\n"
    "    return clean, errors\n"
)

import re


def replace_last(src, key, kind, value):
    pat = re.compile(kind + r'\["' + re.escape(key) + r'"\] = (\{.*?\}|".*?");', re.S)
    matches = list(pat.finditer(src))
    assert matches, f"{kind}[{key}] not found"
    m = matches[-1]
    return src[: m.start()] + f'{kind}["{key}"] = {json.dumps(value)};' + src[m.end():]


# envelope ref is unchanged in behavior; validate ref gains the final sort.
src = replace_last(src, "pa-api-validate-user", "R", validate_ref)
io.open(LEDGER, "w", encoding="utf-8").write(src)

print("m9 fixer: JSON tests updated, ledger validate ref updated")
