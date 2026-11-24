#!/usr/bin/env python3
"""
v8.7.1 targeted re-run: harem rows coded N/A
Beyond Murdock - Coetzee & Querci

Re-codes (both passes) only the rows where search_query is "harem" and v8.7 gave
1_mar_prac = 4, using the v8.7.1 codebook (harem tied to an identified man or
office = Polygamy, incidental). Every other row is copied unchanged.

HOW TO RUN (VS Code terminal, in the same folder as before):
    Needs next to this script:
        v8_7_run.py                              (the parallel version)
        Marriage_Coding_Instrument_v8_7_1_full.md
        final_data_combined_V2.csv
        final_data_combined_V2_v8_7_results.csv
    export ANTHROPIC_API_KEY=sk-ant-...
    caffeinate -i python v8_7_1_rerun_harem.py

Output: final_data_combined_V2_v8_7_1_results.csv  (the full dataset, updated)
        harem_rerun_v8_7_1.csv                     (the re-coded rows only; lets a
                                                    stopped run resume)
New columns: rerun_v8_7_1 (True for re-coded rows), prev_1_mar_prac, prev_22_discreteness
"""

import sys, os, time, threading, signal, importlib.util
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = Path(__file__).resolve().parent
CORPUS = HERE / "final_data_combined_V2.csv"
OLD = HERE / "final_data_combined_V2_v8_7_results.csv"
NEW = HERE / "final_data_combined_V2_v8_7_1_results.csv"
PART = HERE / "harem_rerun_v8_7_1.csv"
CODEBOOK = HERE / "Marriage_Coding_Instrument_v8_7_1_full.md"
WORKERS = 5

for p in (HERE / "v8_7_run.py", CODEBOOK, CORPUS, OLD):
    if not p.exists():
        sys.exit(f"Missing {p.name} (must sit next to this script)")

# load the main script's functions, in --all mode so run_ids match the full run
sys.argv = ["v8_7_run.py", CORPUS.name, "--all"]
spec = importlib.util.spec_from_file_location("v87", HERE / "v8_7_run.py")
v87 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v87)
v87.CODEBOOK = CODEBOOK
pd = v87.pd


def main():
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit("Set ANTHROPIC_API_KEY first.")
    client = v87.anthropic.Anthropic(api_key=key, max_retries=4)
    part1, part2 = v87.load_codebook()

    s = v87.draw_sample(CORPUS)                       # same run_ids as the full run
    old = pd.read_csv(OLD, low_memory=False)
    target = old[(old["search_query"].astype(str).str.strip() == "harem")
                 & (old["1_mar_prac"] == 4)]["run_id"]
    print(f"Harem rows coded N/A in v8.7: {len(target)}")

    done = pd.read_csv(PART) if PART.exists() else pd.DataFrame()
    if len(done):
        done = done[done["error"].isna()]
    done_ids = set(done["run_id"]) if len(done) else set()
    rows = done.to_dict("records") if len(done) else []
    todo = s[s["run_id"].isin(set(target) - done_ids)]
    print(f"{len(done_ids)} already re-coded, {len(todo)} to go ({WORKERS} at a time)")
    extra = [c for c in v87.KEEP_EXTRA if c in s.columns]

    def save():
        df = pd.DataFrame(rows).drop(columns=["_extracted"], errors="ignore")
        tmp = PART.with_suffix(".tmp"); df.to_csv(tmp, index=False); os.replace(tmp, PART)

    pool = ThreadPoolExecutor(max_workers=WORKERS)
    futs = [pool.submit(v87.code_one, client, part1, part2, r, extra) for _, r in todo.iterrows()]
    n = 0
    try:
        for f in as_completed(futs):
            out = f.result(); rows.append(out); n += 1
            if n % 10 == 0:
                save()
            print(f"  {len(done_ids) + n}/{len(target)}  {out['run_id']}  code={out['1_mar_prac']}  "
                  f"disc={out['22_discreteness']}  {'extracted' if out['_extracted'] else ''}"
                  f"{'  ERROR ' + out['error'][:60] if out['error'] else ''}")
    except KeyboardInterrupt:
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        save()
        print("\nStopped and saved. Run the same command again to continue.")
        pool.shutdown(wait=False, cancel_futures=True); os._exit(1)
    pool.shutdown(wait=True)
    save()

    new = pd.read_csv(PART)
    n_err = new["error"].notna().sum()
    if n_err:
        print(f"{n_err} rows failed - run the same command again to retry them.")
        return
    # merge into the full dataset
    old = old.set_index("run_id")
    old["rerun_v8_7_1"] = False
    old["prev_1_mar_prac"] = old["1_mar_prac"]
    old["prev_22_discreteness"] = old["22_discreteness"]
    new = new.set_index("run_id")
    for c in new.columns:
        if c not in old.columns:
            old[c] = None
    old[new.columns] = old[new.columns].astype(object)
    old.loc[new.index, new.columns] = new
    old.loc[new.index, "rerun_v8_7_1"] = True
    out = old.reset_index().sort_values("run_id")
    out.to_csv(NEW, index=False)

    flipped = out[out["rerun_v8_7_1"] & (out["1_mar_prac"] != 4)]
    print(f"\nDone -> {NEW.name}")
    print(f"  re-coded: {len(new)}   now Polygamy/Monogamy/Both: {len(flipped)}")
    print("  new codes for re-coded rows:", new["1_mar_prac"].value_counts().sort_index().to_dict())
    print("  full dataset 1_mar_prac:", out["1_mar_prac"].value_counts().sort_index().to_dict())


if __name__ == "__main__":
    main()
