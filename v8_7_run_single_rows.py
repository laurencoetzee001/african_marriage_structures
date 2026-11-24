#!/usr/bin/env python3
"""
Marriage Coding Instrument v8.7 (full) - two-pass run
Beyond Murdock - Coetzee & Querci

TWO WAYS TO RUN (VS Code terminal, in the folder holding these files):

  A) 1,000-row sample from the corpus (hand-coded rows excluded):
       python v8_7_run.py final_data_combined_V2.csv
  B) Every row of a file, no sampling (use this for the 360 hand-coded rows):
       python v8_7_run.py hand_coding_fix_V2.csv --all

Needs next to this script:
     Marriage_Coding_Instrument_v8_7_full.md
     the input CSV (and hand_coding_fix_V2.csv for option A, so its rows are excluded)
Set the key first:  export ANTHROPIC_API_KEY=sk-ant-...   (Windows: set ...)

Each row is coded in two passes:
  pass 1 (filter, every row): 1_mar_prac, Variable 22, other_marriage_in_window
  pass 2 (extraction, rows with 22_discreteness 1 or 2): 0_subject, variables 2-21,
         11_code_conf, 11_conf_note
Output:  <input name>_v8_7_results.csv  (and <input name>_v8_7_sample.csv for option A)
Resumable: if it stops or rows fail, run the same command again.

If your file uses different column names, change COLUMNS below.
"""

import os, re, json, time, sys
from pathlib import Path
import pandas as pd

try:
    import anthropic
except ImportError:
    sys.exit("Run:  pip install anthropic pandas json-repair")
try:
    import json_repair
except ImportError:
    json_repair = None
    print("Note: json-repair not installed; malformed model output will be retried instead of repaired.")
    print("      To install:  pip install json-repair")

# ---------------- settings you may change ----------------
N_RUN = 1000              # rows to code
SEED = 2026               # fixed so the same sample is drawn every time
COLUMNS = {               # corpus column names -> what the script calls them
    "guid": "guid_hash",
    "page_ref": "page_ref",
    "query": "search_query",
    "target": "full_text",       # the target page
    "window": "complete_text",   # preceding + target + following page (context D)
}
KEEP_EXTRA = ["region", "period", "year", "title"]   # carried through if present
# ----------------------------------------------------------

HERE = Path(__file__).resolve().parent
CODEBOOK = HERE / "Marriage_Coding_Instrument_v8_7_full.md"
HAND = HERE / "hand_coding_fix_V2.csv"
ALL_ROWS = "--all" in sys.argv
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
INPUT = HERE / ARGS[0] if ARGS else None
STEM = INPUT.stem if INPUT else "input"
SAMPLE = HERE / f"{STEM}_v8_7_sample.csv"
RESULTS = HERE / f"{STEM}_v8_7_results.csv"
MODEL = "claude-haiku-4-5-20251001"
TEMPERATURE = 0.2

PASS1_FIELDS = ["1_mar_prac", "22_discreteness", "22_nondiscrete_ref", "22_nd_type",
                "1_mar_prac_conf", "other_marriage_in_window", "12_validation_flags",
                "subject_group", "hit_text", "evidence_quote", "rule_applied",
                "internal_reasoning"]
RULES = {"0_no_hit", "1a", "1b", "1c", "1d", "1e", "2", "3", "4", "5"}
PASS2_FIELDS = ["0_subject", "2_mar_diff", "3_pol_struc", "4_ethnic_group", "5_soc_stat",
                "6_obs_type", "7_obs_location", "8_cited_loc", "9_moral_op", "10_stance",
                "13_wives_no", "13_wives_no_notes", "14_concubines", "14_concubines_notes",
                "15_dowry", "15_dowry_notes", "16_gender_roles", "17_legality", "18_kingdoms",
                "19_geo_features", "20_historian_flag", "21_rel_context", "21_rel_cited",
                "21_rel_quote", "21_rel_notes", "11_code_conf", "11_conf_note",
                "12_validation_flags"]


# ---------------- step 1: sample ----------------
def draw_sample(corpus_path):
    df = pd.read_csv(corpus_path)
    missing = [c for c in COLUMNS.values() if c not in df.columns]
    if missing:
        sys.exit(f"Input is missing columns {missing}. Edit COLUMNS at the top of the script.")
    if ALL_ROWS:
        s = df.reset_index(drop=True)
        s.insert(0, "run_id", [f"R{i:04d}" for i in range(len(s))])
        print(f"Step 1: coding all {len(s)} rows of {corpus_path.name} (no sampling)")
        return s
    if SAMPLE.exists():
        s = pd.read_csv(SAMPLE)
        print(f"Step 1: using existing sample ({len(s)} rows) in {SAMPLE.name}")
        return s
    g, p = COLUMNS["guid"], COLUMNS["page_ref"]
    df["_key"] = df[g].astype(str) + "|" + df[p].astype(str)
    df = df.drop_duplicates("_key")
    n_before = len(df)
    if HAND.exists():
        h = pd.read_csv(HAND)
        hk = set(h["guid_hash"].astype(str) + "|" + h["page_ref"].astype(str))
        df = df[~df["_key"].isin(hk)]
        print(f"Step 1: excluded {n_before - len(df)} rows already in {HAND.name}")
    else:
        print(f"Step 1: WARNING - {HAND.name} not found, so hand-coded rows are NOT excluded")
    n = min(N_RUN, len(df))
    s = df.sample(n=n, random_state=SEED).drop(columns="_key").reset_index(drop=True)
    s.insert(0, "run_id", [f"R{i:04d}" for i in range(len(s))])
    s.to_csv(SAMPLE, index=False)
    print(f"Step 1: drew {len(s)} rows from {len(df)} eligible -> {SAMPLE.name}")
    return s


# ---------------- step 2: code ----------------
def load_codebook():
    text = CODEBOOK.read_text(encoding="utf-8")
    if "<!-- PART 1 -->" not in text or "<!-- PART 2 -->" not in text:
        sys.exit(f"{CODEBOOK.name} is missing its PART 1 / PART 2 markers.")
    part1 = text.split("<!-- PART 1 -->", 1)[1].split("<!-- PART 2 -->", 1)[0]
    part2 = text.split("<!-- PART 2 -->", 1)[1]
    return part1.strip(), part2.strip()


def pass1_prompt(query, target, window, page_ref):
    return f"""Code this row with Part 1 (filter pass) of the Marriage Coding Instrument v8.7.
Start with Rule 0: the search engine matched this row to the query; find that hit and code only that hit.
Return one JSON object only, no other text.

SEARCH QUERY: {query}
PAGE REFERENCE: {page_ref}

=== TARGET PAGE ===
{target}

=== FULL WINDOW (preceding page + target page + following page) ===
{window}
"""


def pass2_prompt(query, target, window, page_ref, p1):
    return f"""Code this row with Part 2 (extraction pass) of the Marriage Coding Instrument v8.7.
Code every variable for the practice at the keyword hit below. Do not recode 1_mar_prac.
Return one JSON object only, no other text.

SEARCH QUERY: {query}
PAGE REFERENCE: {page_ref}

FILTER-PASS RESULT (fixed):
  1_mar_prac: {p1["1_mar_prac"]}
  22_discreteness: {p1["22_discreteness"]}
  subject_group: {p1.get("subject_group")}
  hit_text: {p1.get("hit_text")}

=== TARGET PAGE ===
{target}

=== FULL WINDOW (preceding page + target page + following page) ===
{window}
"""


def to_int(v, default=None):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def get_json(text):
    """Parse the model's JSON; repair common slips (unescaped quotes, trailing commas)."""
    t = re.sub(r"```(?:json)?", "", text)
    m = re.search(r"\{.*\}", t, re.S)
    if not m:
        raise ValueError("no JSON in response")
    raw = m.group(0)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        if json_repair is None:
            raise
        d = json_repair.loads(raw)
        if not isinstance(d, dict) or not d:
            raise ValueError("JSON could not be repaired")
        d["_repaired"] = True
        return d


def parse1(text):
    d = get_json(text)
    code, disc = to_int(d.get("1_mar_prac")), to_int(d.get("22_discreteness"))
    if code not in (1, 2, 3, 4) or disc not in (0, 1, 2, 3):
        raise ValueError(f"bad codes: 1_mar_prac={code}, 22_discreteness={disc}")
    d["1_mar_prac"], d["22_discreteness"] = code, disc
    d["1_mar_prac_conf"] = to_int(d.get("1_mar_prac_conf"), 3)
    d["22_nondiscrete_ref"] = to_int(d.get("22_nondiscrete_ref"))
    om = d.get("other_marriage_in_window")
    d["other_marriage_in_window"] = (om if isinstance(om, bool)
                                     else str(om).strip().lower() == "true" if om is not None else None)
    extra = []
    rule = str(d.get("rule_applied", "")).strip()
    if rule not in RULES:
        extra.append("invalid_rule")
    # every Rule 0/1 outcome is N/A: correct it and flag
    if rule == "0_no_hit" or rule.startswith("1"):
        want_disc = 0 if rule in ("0_no_hit", "1e") else 3
        if code != 4 or disc != want_disc:
            extra.append("rule_code_corrected")
            d["1_mar_prac"], d["22_discreteness"] = 4, want_disc
            if want_disc == 0:
                d["22_nondiscrete_ref"], d["22_nd_type"] = None, None
    elif {"2": 2, "3": 3, "4": 1}.get(rule, code) != code:
        extra.append("rule_code_mismatch")
    d["_extra_flags"] = extra
    return d


def parse2(text):
    d = get_json(text)
    for k in ("0_subject", "2_mar_diff", "3_pol_struc", "5_soc_stat", "6_obs_type",
              "7_obs_location", "9_moral_op", "21_rel_context", "11_code_conf"):
        d[k] = to_int(d.get(k))
    return d


def call(client, system, prompt, parser, max_tokens):
    last_err = None
    for attempt in range(5):
        try:
            msg = client.messages.create(
                model=MODEL, max_tokens=max_tokens, temperature=TEMPERATURE,
                system=system, messages=[{"role": "user", "content": prompt}])
        except Exception as e:                      # API trouble: wait, then retry
            last_err = str(e)
            time.sleep(2 ** attempt * 3)
            continue
        try:
            return parser(msg.content[0].text), None
        except Exception as e:                      # bad output: retry straight away
            last_err = f"parse: {e}"
            if attempt >= 2:
                break
    return None, last_err


def txt(v):
    return "" if pd.isna(v) else str(v)


def flat(v):
    """Lists become '; '-joined strings so every variable is one CSV column."""
    if isinstance(v, list):
        return "; ".join(str(x) for x in v)
    return v


def join_flags(*vals):
    out = []
    for v in vals:
        items = v if isinstance(v, list) else [x.strip() for x in txt(v).replace(";", ",").split(",")]
        for x in items:
            x = str(x).strip()
            if x and x not in out:
                out.append(x)
    return "; ".join(out)


def run_coding(s):
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit("Set ANTHROPIC_API_KEY first (see top of script).")
    client = anthropic.Anthropic(api_key=key)
    part1, part2 = load_codebook()

    done = pd.read_csv(RESULTS) if RESULTS.exists() else pd.DataFrame()
    if len(done):
        done = done[done["error"].isna()]          # retry failed rows
    done_ids = set(done["run_id"]) if len(done) else set()
    rows = done.to_dict("records") if len(done) else []
    todo = s[~s["run_id"].isin(done_ids)]
    print(f"Step 2: {len(done_ids)} rows already coded, {len(todo)} to go")

    for n, (_, r) in enumerate(todo.iterrows(), 1):
        q, t, w, pr = (txt(r[COLUMNS["query"]]), txt(r[COLUMNS["target"]]),
                       txt(r[COLUMNS["window"]]), r[COLUMNS["page_ref"]])
        out = {"run_id": r["run_id"], "guid": r[COLUMNS["guid"]], "page_ref": pr,
               "search_query": q, "window_chars": len(w)}
        for c in KEEP_EXTRA:
            if c in s.columns:
                out[c] = r[c]
        for f in PASS1_FIELDS + PASS2_FIELDS:
            out[f] = None

        p1, err = call(client, part1, pass1_prompt(q, t, w, pr), parse1, 900)
        p2 = None
        if p1:
            for f in PASS1_FIELDS:
                out[f] = flat(p1.get(f))
            ok = (p1["1_mar_prac"] in (1, 2, 3)) == (p1["22_discreteness"] in (1, 2))
            out["consistent"] = ok
            out["relevance_applicable"] = p1["22_discreteness"] in (1, 2)
            if out["relevance_applicable"] and ok:
                p2, err = call(client, part2, pass2_prompt(q, t, w, pr, p1), parse2, 1400)
                if p2:
                    for f in PASS2_FIELDS:
                        if f != "12_validation_flags":
                            out[f] = flat(p2.get(f))
            flags = [p1.get("12_validation_flags"), p2.get("12_validation_flags") if p2 else ""]
            flags += p1.get("_extra_flags", [])
            if p1.get("_repaired") or (p2 and p2.get("_repaired")):
                flags.append("json_repaired")
            if not ok:
                flags.append("inconsistent_codes")
            out["12_validation_flags"] = join_flags(*flags)
        out["error"] = err
        rows.append(out)
        if n % 10 == 0 or n == len(todo):
            pd.DataFrame(rows).to_csv(RESULTS, index=False)
        print(f"  {len(done_ids) + n}/{len(s)}  code={out['1_mar_prac']}  "
              f"disc={out['22_discreteness']}  "
              f"{'extracted' if p2 else ''}  {'ERROR ' + err[:60] if err else ''}")

    res = pd.DataFrame(rows)
    res.to_csv(RESULTS, index=False)
    n_err = res["error"].notna().sum()
    print(f"Step 2: done -> {RESULTS.name}  (errors: {n_err}"
          f"{'; rerun the script to retry them' if n_err else ''})")
    return res, n_err


def main():
    if INPUT is None:
        sys.exit("Usage: python v8_7_run.py YOUR_FILE.csv   (add --all to code every row)")
    if not INPUT.exists():
        sys.exit(f"Can't find {INPUT.name} in this folder. Check the name with:  ls *.csv")
    if not CODEBOOK.exists():
        sys.exit(f"Missing {CODEBOOK.name} (must sit next to this script)")
    s = draw_sample(INPUT)
    res, n_err = run_coding(s)
    ok = res[res["error"].isna()]
    print("\nSummary:")
    print("  1_mar_prac:", ok["1_mar_prac"].value_counts().sort_index().to_dict())
    print("  22_discreteness:", ok["22_discreteness"].value_counts().sort_index().to_dict())
    print("  other marriage content in window:",
          ok["other_marriage_in_window"].value_counts(dropna=False).to_dict())
    print("  rows extracted in pass 2:", ok["0_subject"].notna().sum())
    fl = ok["12_validation_flags"].fillna("")
    for f in ("rule_code_corrected", "rule_code_mismatch", "invalid_rule", "inconsistent_codes"):
        print(f"  {f}: {fl.str.contains(f).sum()}")
    if n_err:
        print("Some rows failed - rerun the same command to retry them.")


if __name__ == "__main__":
    main()
