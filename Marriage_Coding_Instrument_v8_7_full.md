# Marriage Coding Instrument v8.7 (full)

Beyond Murdock (Coetzee & Querci), September 2026.

The instrument runs in two passes.

- **Part 1, filter pass (every row):** codes `1_mar_prac` and Variable 22 (discreteness).
- **Part 2, extraction pass (only rows with `22_discreteness` = 1 or 2):** codes `0_subject` and variables 2 to 21, with overall confidence and validation flags.

## Why v8.7

v8.3 silently redefined several extraction variables, although its changelog said they were "unchanged from v7.1". The hand-coded validation sample follows v7.1. v8.7 therefore restores the v7.1 definitions in Part 2 and keeps only the deliberate changes made since.

## Changes from v7.1 (Part 2)

| Change | Status |
|---|---|
| Definitions of `2_mar_diff`, `3_pol_struc`, `5_soc_stat`, `6_obs_type`, `13_wives_no`, `14_concubines`, `15_dowry`, `16_gender_roles`, `17_legality`, `18_kingdoms`, `19_geo_features`, `20_historian_flag` and `21_*` | **Restored to v7.1** (v8.3 had changed them) |
| `4_ethnic_group` lists only groups party to the custom | Kept from v8.0 (deliberate) |
| Confidence and flags coded last | Kept from v8.0 (deliberate) |
| Rule 0 anchoring on the keyword hit, replacing v8.3's target-practice rule | v8.6 ruling |
| Polygamy anchor rule when `1_mar_prac` = 3 | v7.1, unchanged |
| Europeans and other non-African subjects: `0_subject` = 4; `4_ethnic_group` as named, or `["European"]` | v8.6 ruling |
| `2_mar_diff`: a single named person's marriage with no statement about the wider society = 2 | Clarification (v7.1 Sultan Bello example already codes it so) |
| `11_code_conf`: confidence 1 not allowed when any variable is flagged or inferred | New (v8.5 validation showed confidence carried almost no information) |
| Example 2 (Turks and Greeks): `4_ethnic_group` ["Turks", "Greeks"] → ["Turks"] | Brought into line with v7.1's own anchor rule |
| Contents-page example dropped | These rows are filtered out in Part 1 |

## Changes in Part 1 since the 1,000-row run

| Change | Evidence from the run |
|---|---|
| Rule 0: trust the search engine's match; if the exact phrase is not visible, anchor on the nearest passage with the query's terms; N/A for a missing hit only if none of the terms appear | 9 rows coded N/A because the model said the hit was absent, including a detailed marriage case |
| `other_marriage_in_window` is a required true/false field (it replaces the optional `other_marriage_content` flag) | The flag was used once in 1,000 rows |
| Part 1 output: `1_mar_prac_conf` and `12_validation_flags` moved to the end, matching the v8.0 decision to code confidence and flags last | v8.6 had placed them in the middle of the Part 1 output |
| Rule 1e (non-marital use) added; every Rule 1 outcome must be `1_mar_prac` = 4; permitted `rule_applied` values listed | 4 index entries coded Polygamy under Rule 1a; the model invented rule values "0", "1" and "1_non_marital_use" |

## Decisions still running on defaults (confirm with Pietro)

- A generic "a wife" in a group's custom (rows 143 and 311) is coded type unspecified (N/A).
- Anchoring is strict (row 222).
- Variables 2–21 are not coded for non-discrete rows.
- `18_kingdoms` stays limited to **African** kingdoms and rulers, as in v7.1. Non-African rulers now coded in Part 1 (an Ottoman sultan, say) will have a null `18_kingdoms`.
- `13_wives_no` for monogamy rows is left to the v7.1 rule ("record the stated number"). The hand coders entered 1 on 18 of 52 monogamy rows and left it blank on the rest.

<!-- PART 1 -->
# Part 1: Filter pass

You are coding passages from European travel accounts (1500–1900) for the marriage practice they record. Each row gives you:

- a **search query**: the keyword search that extracted this row;
- the **target page**;
- the **full window**: the preceding page, the target page and the following page.

For each row, return one code for `1_mar_prac` and one for `22_discreteness`, following the rules below **in order**. Stop at the first rule that fits.

**Core principle:** a practice is coded only from a **discrete observation**, meaning an identifiable practising subject (a named person, an office holder, or a named people or group) whose marriage practice the text reports. When in doubt, prefer N/A. A false positive is worse than a missed row.

## Codes

| `1_mar_prac` | Meaning |
|---|---|
| 1 | Monogamy |
| 2 | Polygamy (polygyny, concubinage, harem households) |
| 3 | Both (explicit contrast only) |
| 4 | N/A: no discrete marriage practice |

| `22_discreteness` | Meaning | Allowed `1_mar_prac` |
|---|---|---|
| 0 | No marriage content at the hit | 4 |
| 1 | Substantive: identified subject, and the text reports the practice itself (how many wives, customs, rules, rank of wives) | 1, 2, 3 |
| 2 | Incidental: identified subject and codable practice, but a passing mention with no further detail | 1, 2, 3 |
| 3 | Non-discrete: marriage content present, but no identifiable subject or no stated type | 4 |

These two fields must agree. `1_mar_prac` is 1–3 **if and only if** `22_discreteness` is 1 or 2.

## Rule 0: code the keyword hit

1. **The search engine has already matched this row to the query.** Find that match. Queries such as `"many wives"~10` mean both words within about 10 words of each other; `polygyn~` means any word starting with that stem.
2. **Do not second-guess the match.** OCR errors, hyphenation, line breaks and page boundaries often hide the exact phrase. If you cannot see an exact match, anchor on the nearest passage that contains the query's key terms (for `"house wife"~10`, a passage with "wife" near "house", or failing that the nearest "wife"). Only if **none** of the query's terms appear anywhere in the window do you code `1_mar_prac` = 4, `22_discreteness` = 0, `rule_applied` = "0_no_hit". Never code 4 merely because the exact phrase or distance is not visible.
3. If the hit is not on the target page, use the surrounding pages and add the flag `context_only`.
4. Code **only the practice attached to that hit**: the sentence containing it and the sentences around it about the same subject. Use the rest of the window only to interpret the hit, for example to identify who "he" is or to see whether the harem is in use.
5. **Do not code other marriage content in the window.** It is coded in its own row from its own hit. But you must report whether it exists: set `other_marriage_in_window` to `true` if the window contains any marriage content about a **different** subject or practice from the hit, and `false` otherwise. This field is required for every row.

Example: the hit is "the harem was empty", and the same page says the merchant married one wife. Code the hit (Rule 1b, absence, so 4), not the marriage, and set `other_marriage_in_window` = true.

## Rule 1: N/A screens (`1_mar_prac` = 4)

If any of the following applies to the hit, code `1_mar_prac` = 4. Unless stated otherwise, set `22_discreteness` = 3 and fill `22_nondiscrete_ref` and `22_nd_type`.

**1a Apparatus** (`22_nd_type` = apparatus). The hit sits in an index, a table of contents, a chapter or letter summary, a list of plates, or a bibliographic note. Examples: "Letter XXXIX. Constantinople. Harems. Polygamy. Page 189"; "the King of Spain Ferdinand, and his wife Elizabeth" in a book citation. Add the flag `index`.

**1b Non-discrete reference.** Marriage content is present, but no identifiable subject's practice is reported.

- **Scenery** (`scenery`): harem women or harem spaces seen in passing, with no man identified. Examples: "the richly-dressed, closely-veiled women of the harem" in a street scene; "veiled harem ladies" in carriages; "slaves… destined for the harem" at a market; a generic house layout with "the harem door"; a building "once used for a harem, now for a powder-magazine".
- **Allusion** (`allusion`): historical, legendary, biblical, ancient or literary figures mentioned in passing, where the passage is not reporting their marriage practice. Examples: an aqueduct attributed to "Zobeid, the favorite wife of… Haroun al Raschid"; "Thutmose I, his wife, the royal sister" in temple inscriptions; Uriah refusing to see his wife, used as a moral lesson; Lot's wife; a poem's "light of the Harem".
- **Rhetoric** (`rhetoric`): marriage used in an argument, a joke or a general reflection, rather than reported as a practice. Examples: "if it is not the polygamy and not the drink that makes the West African as useless…"; a traveller braced "for death, or the Koran, or even for plural wives"; a writer's "apology for polygamy".
- **Metaphor** (`metaphor`): for example, the "harem" of a holy man's devotees, or "our harem-camp".
- **Absence** (`absence`): the hit says there is no harem or no wife, or that the harem is empty or unused. Examples: "the harem was empty"; "there is no harem to intrude upon".

**1c Type unspecified** (`type_unspecified`). A subject is identified, but the text does not say whether the practice is monogamous or polygamous.

- "Marriage" or "married" with no type: "Marriage being general among them"; "They are all now civilized and married".
- Plural "wives" spread across a group of men, where each man might have one wife or several: "soldiers… accompanied by their wives and children"; "food for themselves and wives"; "letters… from their fathers and mothers and wives"; "slaves who are married with wives and children"; "Many slave wives are thus bought"; "Many of the Europeans had married Abyssinian or Galla wives".
- A generic singular wife inside a group's custom, where the text never says a man has only one: "a wife is not delivered in her husband's house"; merchants who have a stranger "deflower the wife". Add the flag `ambiguous_practice`.

**1d Illegible** (`illegible`). OCR near the hit is too damaged to tell who is married to whom. Add the flag `ocr`. If a decisive phrase is still clearly legible ("He had two wives"), do not use 1d; code it under Rule 2 or 4 and add `ocr`.

**1e Non-marital use** (`rule_applied` = "1e"). The words are not about marriage at all: "wise laws" misread as "wife", "housewife" as an occupation, "harem" as the name of a street. Code `1_mar_prac` = 4 and `22_discreteness` = 0; leave `22_nondiscrete_ref` and `22_nd_type` null.

**Every Rule 1 outcome (1a to 1e) is `1_mar_prac` = 4, without exception.** If a Rule 1 screen applies, do not also code a practice; an index entry that names polygamy is still 1a and 4.

## Rule 2: Polygamy (`1_mar_prac` = 2)

Code 2 when the hit shows that an **identified man, office holder, or the men of a named group** have, had, or may have more than one wife or concubine. Any one of these is enough:

- **Plural wives of one man:** "the Kabaka's wives"; "he had two wives"; "Muhammad had nine wives" when reported as a practice rather than an allusion.
- **A group statement that explicitly gives more than one wife per man:** "every man there marries as many wives as he can keep"; "the rich have two wives, the chief wife and the second"; a Pahouin man's property listed as "his goods, his house, his land, his wives". Plural "wives" across a group **without** such a statement is 1c, not 2.
- **Concubines or concubine slaves** of an identified man or a named group.
- **Polygamy described as practised or permitted** among a named people or group: "polygamy is practised on a very large scale"; "countenanced in Polygamy".
- **A harem, seraglio or zenana tied to an identified man or office**, even when only the building is described: "his harem was desolate"; "the sultan and his harem"; "the palace of a Bey… apart is the Harem"; "the Royal Cascine and Harem of Mto-ni" (the Sayyid's palace); "a retinue of servants and well-selected harem" (Arabi Pasha); an Arab "savage… at our intention of penetrating into his harem". If no man or office is identified, use 1b scenery.
- **Wives ranked against other wives:** "the chief wife and the second"; "second wife"; "senior wife"; "co-wives"; "head wife" alongside other wives.
- **Non-monogamous arrangements of a named group**, even when the author says it is "not marriage" or moralises about it. Example: Maasai chiefs who "claim young girls as tribute" and give their servants captive women. The author's judgement belongs in the moral-opinion and stance variables, not in this code.

**Status adjectives are not rank.** "Great", "royal", "queen" or "lady" describe a wife's standing, not the existence of co-wives. "The great wife of Brac, who is like the queen sultana" is Monogamy under Rule 4.

**Permitted but uncommon still counts as Polygamy.** "The law allows a man four wives, though most have only one or two" is 2, not 3.

Use `22_discreteness` = 1 when the passage reports the practice itself (numbers, rules, ranks, customs). Use 2 for a passing reference: "his harem", or "the Kabaka's wives" in a sentence about something else.

## Rule 3: Both (`1_mar_prac` = 3)

Code 3 **only** when the author explicitly compares or contrasts monogamy and polygamy **as systems** in the passage around the hit. Examples: Christian monogamy set against Muslim polygamy in one argument; two named groups with opposite practices.

Mere co-occurrence of a "wife" and "wives" is not enough. Code 3 is rare. If in doubt, apply Rules 2 and 4 to the hit instead.

## Rule 4: Monogamy (`1_mar_prac` = 1)

Code 1 when the hit shows an **identified person with a single spouse** and nothing near the hit indicates other wives, or when monogamy is stated as the practice of a named person or group.

- **Incidental mentions count:** "two Basutos… ill treated his wife" (Swanepoel's wife); "the captain… had his wife with him"; "the wife and children of our friend Mr. Kishori". Set `22_discreteness` = 2.
- **Europeans count:** "the first mate, and his wife… Colonel James and his lady"; "Madame Goleau, wife of the First President"; missionary weddings; "the wife of a non-commissioned officer". Record them as European in `subject_group` and add the flag `non_african_subject`.
- **Rulers with one named wife count:** "the great wife of Brac"; "the wife of so great a Monarch".
- **Serial marriage is Monogamy:** "assisted by his first wife… the present wife".
- **Stated monogamy:** "confined themselves to one wife"; "sixteen children by one wife". Set `22_discreteness` = 1.

## Rule 5: Otherwise

If no rule above applies, code `1_mar_prac` = 4. Use `22_discreteness` = 0 if the hit has no marriage content, or 3 with `22_nd_type` = type_unspecified if it does.

## Non-discrete detail (only when `22_discreteness` = 3)

| Field | Values |
|---|---|
| `22_nondiscrete_ref` | 1 monogamy · 2 polygamy · 3 unspecified: the practice the text gestures at. "Veiled harem ladies" = 2; "marriage being general" = 3. |
| `22_nd_type` | apparatus · scenery · allusion · rhetoric · metaphor · absence · type_unspecified · illegible |

When `22_discreteness` is not 3, set both fields to null.

## Confidence in the practice code (`1_mar_prac_conf`)

| Code | Use when |
|---|---|
| 1 | The hit itself states the practice explicitly ("he had three wives", "polygamy is general among them", "his wife" of a named man). |
| 2 | The code is inferred: polygamy from a harem tied to a man, monogamy with no statement that there are no other wives, or a ranked wife. |
| 3 | Any of: OCR damage near the hit, subject unclear, the hit found only in the surrounding pages, or the code depends on text outside the hit's own passage. |

Confidence 1 must never be used for an inferred code. Use 3 whenever one of its conditions holds, even if you feel sure.

## Validation flags (`12_validation_flags`)

Use any that apply, comma-separated, or an empty string: `index`, `ocr`, `context_only`, `subject_unclear`, `non_african_subject`, `ambiguous_practice`.

## Output

Return **one JSON object and nothing else**. `rule_applied` must be exactly one of: `0_no_hit`, `1a`, `1b`, `1c`, `1d`, `1e`, `2`, `3`, `4`, `5`. `other_marriage_in_window` must be `true` or `false`. Assess `1_mar_prac_conf` and `12_validation_flags` last, after all codes and the reasoning, as in Part 2.

```json
{
  "1_mar_prac": 2,
  "22_discreteness": 1,
  "22_nondiscrete_ref": null,
  "22_nd_type": null,
  "subject_group": "who practises it, e.g. 'Gold Coast merchants', 'Ottoman elite', 'European traveller'; empty if none",
  "hit_text": "the words of the keyword hit you coded, max 30 words",
  "evidence_quote": "the shortest decisive phrase, max 25 words",
  "rule_applied": "0_no_hit|1a|1b|1c|1d|1e|2|3|4|5",
  "other_marriage_in_window": true,
  "internal_reasoning": "one or two sentences",
  "1_mar_prac_conf": 1,
  "12_validation_flags": ""
}
```


---

<!-- PART 2 -->
# Part 2: Extraction pass (variables 0 and 2–21)

This part runs only for rows that passed the filter (`22_discreteness` = 1 or 2, `1_mar_prac` = 1, 2 or 3). You receive the search query, the target page, the full window, and the filter-pass result: `1_mar_prac`, `22_discreteness`, `subject_group` and `hit_text`.

Variable definitions follow **codebook v7.1**, the version used for the hand-coded validation sample.

## Task

Code the remaining variables for **the practice at the keyword hit** identified by the filter pass.

- **Do not recode `1_mar_prac`.** It is fixed by the filter pass.
- Use ONLY information present in the text. Do NOT apply external cultural or historical knowledge.
- Apply codes based on what the author reports, not what you infer about the society.
- String fields must be copied VERBATIM, preserving original spelling, transliteration and capitalisation.
- Where a conditional rule requires null, output null. Otherwise always output a code.

## Core rule: no uncertain codes

There are no "unclear" or "unspecified" codes in this part. When you are uncertain, you MUST still select the single best-fit code based on the evidence, AND add that variable's name to `12_validation_flags` to request human review. Do not leave coded variables blank, and do not invent new codes.

## Scope in the three-page window

**Anchor on the hit.** Every variable describes the practice attached to `hit_text`: the same subject and the same practice. Other marriage content in the window has its own row. Do not merge it in.

**Anchor rule: code the polygamous practice.** When `1_mar_prac` = 3, anchor ALL variables to the POLYGAMOUS practice:

- `0_subject`: the parties of the polygamous marriage(s);
- `4_ethnic_group`, `8_cited_loc`, `18_kingdoms`, `19_geo_features`: groups and places attached to the polygamous practice;
- `2_mar_diff`, `5_soc_stat`, `13_wives_no`, `14_concubines`, `15_dowry`, `17_legality`, `21_rel_context`: prevalence, status, wives, dowry, legality and religious framing OF the polygamous practice.

If an ethnic group or location attaches ONLY to the monogamous side, do NOT list it; record the contrast in `11_conf_note` (for example, "monogamy attributed to the coastal Christians; excluded from arrays per anchor rule"). When `1_mar_prac` = 1, the variables describe the monogamous practice as usual.

**Narrative continuity.** If the hit sits inside one continuous account of the same household or group across pages, treat that account as one observation and use details from anywhere in it.

**Variables that may use the whole window**, provided the information concerns the hit's subject: `4_ethnic_group`, `7_obs_location`, `8_cited_loc`, `18_kingdoms`, `19_geo_features`, `21_rel_context` and `21_rel_cited`. Moral opinion, gender roles and the historian flag are extracted once, from wherever they are most complete.

**Variables coded from the hit's own passage:** `2_mar_diff`, `3_pol_struc`, `5_soc_stat`, `13_wives_no`, `14_concubines`, `15_dowry`, `17_legality`.

**Deduplication and conflicts.** Code a repeated fact once, from the hit's passage if it appears there, otherwise from the most detailed statement; add `"cross_page_extraction"` to `12_validation_flags`. If statements conflict across pages, code from the hit's passage, flag the variable, and explain in `11_conf_note`.

---

## VARIABLE 0 — `0_subject`: who are the individuals in this marriage?

Use ONLY explicit textual evidence. When the text does not name the parties, select the most plausible code AND add `"0_subject"` to `12_validation_flags`.

| Code | Label | Apply when |
|---|---|---|
| 1 | african_african | Both parties African, same ethnic group or location |
| 2 | african_african_diff | Both parties African, different ethnic groups or locations |
| 3 | african_foreign | One party African, one European or foreign traveller |
| 4 | foreign_foreign | Both parties European or foreign (this includes Ottoman, Arab, Indian and biblical subjects, and European couples) |

When in doubt: if the extract is about an African group's customs, code 1. If the author describes their own marriage to a local, code 3. Always flag if inferred rather than explicit.

## VARIABLE 2 — `2_mar_diff`: prevalence of the practice

| Code | Label | Apply when |
|---|---|---|
| 1 | widespread | General, common, normal or universal in the population |
| 2 | rare_exception | Exceptional, rare, or limited to specific individuals |

When in doubt: a custom or norm of a group is 1; a practice limited to a few individuals is 2. Always flag. A single named person's marriage (a chief's wives, a traveller's wife) with no statement about the wider society is 2.

## VARIABLE 3 — `3_pol_struc`: polygamy structure

Null UNLESS `1_mar_prac` = 2 or 3. When `1_mar_prac` = 3, code the POLYGAMOUS union only.

| Code | Label | Apply when |
|---|---|---|
| 1 | fixed_spouses | A normalised fixed number is described ("each man takes two wives") |
| 2 | varied | A variable number with implied limits ("richer man, more wives"); always flag |
| 3 | unlimited | No restriction on number stated or implied |

When in doubt, and the text mentions a harem or polygamy with no numeric detail, code 3 and flag.

## VARIABLE 4 — `4_ethnic_group`: ethnic group(s) practising the custom

STRING ARRAY, verbatim from the text, no normalisation; null if none is named. Preserve archaic transliterations exactly ("Bechuanas", "Wanyamwesi", "Kafirs").

List ONLY groups described as party to (practising or undergoing) the marriage custom being coded, not neighbouring peoples, trading partners or historical references. Non-African subjects are recorded as the text names them (`["Turks"]`, `["English"]`). If they are plainly European but no group is named (for example, "the first mate and his wife" on a British ship), use `["European"]` and flag `4_ethnic_group`.

## VARIABLE 5 — `5_soc_stat`: social status of practitioners

| Code | Label | Apply when |
|---|---|---|
| 1 | general_pop | Applies throughout the general population |
| 2 | elite_wealthy | Explicitly limited to elite, wealthy, noble or chiefly individuals |
| 3 | eth_restric | Limited to a specific ethnic subgroup within a larger population |

When in doubt: a group custom without qualification is 1; wealth or rank as a condition is 2. Always flag.

## VARIABLE 6 — `6_obs_type`: type of observation

| Code | Label | Apply when |
|---|---|---|
| 1 | auth_direct | The author explicitly states direct personal witnessing |
| 2 | auth_second_res | A named or described long-term resident of the area is the source |
| 3 | auth_hearsay | An unnamed informant, "it is said", "they say", "I was told" |
| 4 | auth_gen | A general statement with no attribution to a person or source |

## VARIABLE 7 — `7_obs_location`: geographic location present

| Code | Apply when |
|---|---|
| 1 | A named geographic location or place identifier attached to the practice is present in the window |
| 2 | No such location is present |

## VARIABLE 8 — `8_cited_loc`: location name(s)

STRING ARRAY, verbatim; null if `7_obs_location` ≠ 1. Preserve original spellings ("Timbuctoo", "the Zambeze", "Dahomey"). List all named places attached to the practice.

## VARIABLE 9 — `9_moral_op`: moral opinion present

| Code | Label | Apply when |
|---|---|---|
| 1 | moral_judge | An explicit moral, religious or evaluative judgement about the practice |
| 2 | no_judge | No moral judgement present |

Indicators for code 1: "barbarous", "degrading", "sinful", "uncivilised", "revolting", "commendable"; religious framing; a comparative moral claim; a desire for reform. The judgement must be about this practice, not about another topic in the window.

## VARIABLE 10 — `10_stance`: verbatim moral remark

STRING, verbatim; null if `9_moral_op` ≠ 1.

## VARIABLE 13 — `13_wives_no`: number of wives stated

INTEGER or null. Record the stated maximum, minimum or typical number as an integer. If a range is given ("two or three"), record the UPPER bound. If the description is only qualitative ("many wives", "a great number"), record null.

**`13_wives_no_notes`:** STRING (40 words or fewer) or null. Context on wife-number limits, e.g. "maximum of four by Islamic law; in practice most take one or two". May be filled even when `13_wives_no` is null ("as many as he can afford").

## VARIABLE 14 — `14_concubines`: concubines mentioned

STRING: `"yes"`, `"no"` or null.

- `"yes"`: concubines explicitly mentioned as permitted or present.
- `"no"`: the text explicitly states concubines are NOT permitted.
- null: concubines not mentioned at all. Do not infer from absence.

**`14_concubines_notes`:** STRING (40 words or fewer) or null. Fill when `14_concubines` = "yes" with extra detail (legal status of children, upper limit, source of the rule).

## VARIABLE 15 — `15_dowry`: dowry or bride-wealth mentioned

STRING: `"yes"`, `"no"` or null.

- `"yes"`: a dowry, bride-price, bride-wealth or payment for a wife is explicitly mentioned.
- `"no"`: the text explicitly states no such payment exists.
- null: the topic is not mentioned. Do not infer from absence.

**`15_dowry_notes`:** STRING (40 words or fewer) or null. Fill when `15_dowry` = "yes" and a price, goods or conditions are given ("ten cattle and a bolt of cloth", "paid to father of bride").

## VARIABLE 16 — `16_gender_roles`: extreme subservience of the wife

STRING (60 words or fewer) or null. ONLY fill when the text EXPLICITLY describes a wife's status as near-slave level: confined, not allowed to leave, compared to property, described as bought or owned, or entirely without autonomy. For ordinary gender difference or mild inequality, leave null. Quote or closely paraphrase the passage.

## VARIABLE 17 — `17_legality`: stated laws or rules governing marriage

STRING (60 words or fewer) or null. ONLY fill when the text explicitly states a law, a chief's decree, a religious rule, or a named ethnic norm governing marriage, wife number, divorce or spousal dynamics. Paraphrase concisely ("Islamic law permits up to four wives"). Do NOT fill for informal customs described without legal framing.

## VARIABLE 18 — `18_kingdoms`: African kingdoms, chiefdoms or royal references

STRING ARRAY, verbatim, or null. List any named African kingdoms, chiefdoms, sultanates, or named rulers and royals. Preserve archaic spellings ("Dahomey", "the Sultan of Zanzibar", "Mutesa's court").

## VARIABLE 19 — `19_geo_features`: geographic features

STRING ARRAY, verbatim, or null. Geographic features only: rivers, lakes, mountains, ports, valleys, coasts, islands ("the Limpopo", "Lake Nyassa", "the Bight of Benin"). Named settlements go in `8_cited_loc`, not here.

## VARIABLE 20 — `20_historian_flag`: case-study flag

STRING (50 words or fewer) or null. Flag ONLY when the text contains unusually rich, specific detail warranting close reading:

- a detailed bride-wealth price list (specific goods, animals or sums);
- a first-hand account of a marriage ceremony or negotiation with procedural detail;
- an explicitly described legal dispute or court ruling about marriage;
- a named economic or political marriage alliance between kingdoms or chiefs;
- unusually detailed harem organisation, hierarchy or daily life;
- quantitative data on marriage (number of wives per man across a community).

Write a short note explaining WHY it is flagged. Do NOT flag merely because polygamy is mentioned or a moral judgement is present.

## VARIABLE 21 — `21_rel_context`: religious context of the marriage practice

| Code | Label | Apply when |
|---|---|---|
| 1 | religion_linked | The text connects the practice to a religion, religious law, doctrine, institution, ritual or religious actor |
| 2 | no_religion | No religious framing of the practice |

Code 1 indicators:

- religious law governing marriage ("allowed by the law of their Prophet", "the Koran permits");
- religious actors engaging with the practice (missionaries condemning polygamy, priests or marabouts officiating, converts renouncing wives);
- religious ritual or obligation tied to the practice;
- an explicit contrast between religious communities ("the Mahommedans take several wives, whilst the Christians take but one").

**CRITICAL: connection, not co-occurrence.** The window spans three pages, so religion may appear near but unconnected to the marriage content. A mosque, mission or religious festival mentioned in passing does NOT make code 1; the religious reference must attach to the practice itself.

Moral judgement alone is not religious context: "a degrading custom" gives `9_moral_op` = 1 but `21_rel_context` = 2, whereas "a custom contrary to Christian teaching" gives both = 1. Generic descriptors ("heathens", "pagans", "Mahommedan tribes") without a belief linked to the practice are code 2. When the link is implicit or ambiguous, pick the best fit and flag `21_rel_context`.

**`21_rel_cited`:** STRING ARRAY or null; null if `21_rel_context` ≠ 1. Standardised label FIRST, then the text's own term in parentheses where it differs: `["Islam (Mahommedan)"]`, `["Christianity (missionary)"]`, `["Indigenous/traditional (fetish worship)"]`, `["Judaism"]`. List all religions, in order of prominence. If religious context is clear but the tradition unnamed, use `["Unspecified (<actor verbatim>)"]`.

**`21_rel_quote`:** STRING or null; null if `21_rel_context` ≠ 1. Copy VERBATIM the sentence(s) connecting religion to the practice. Prefer the full sentence to a fragment; join several passages with " ... ".

**`21_rel_notes`:** STRING (60 words or fewer) or null; null if `21_rel_context` ≠ 1. Record the context not already in the quote:

- WHO invokes religion (the author, a missionary, a local informant, a religious official, a convert);
- WHAT it governs (wife limit, divorce, concubinage, conversion or baptism, inheritance, ceremony);
- the stated rule detail;
- whether the rule is described as followed or ignored in practice.

## VARIABLE 11 — `11_code_conf`: overall coding confidence

| Code | Label | Apply when |
|---|---|---|
| 1 | high | 95% or more confidence in all coded variables |
| 2 | medium | 60–94%: one or more variables uncertain |
| 3 | low | Below 60%: substantial ambiguity throughout |

Confidence 1 is not allowed when any variable is flagged in `12_validation_flags`, inferred rather than explicit, or drawn from another page.

**`11_conf_note`:** STRING (30 words or fewer), or null only if nothing below applies. ALWAYS fill it when any of these apply:

- polyandry is present;
- the behaviour is exceptional or anomalous;
- the marriage is mixed-race or cross-ethnic;
- the marriage involves religious figures, enslaved persons or captives;
- information was drawn from other pages;
- `1_mar_prac` = 3 (note the monogamous side).

## VARIABLE 12 — `12_validation_flags`: per-variable human validation flags

Always required; return `[]` if there are no flags. Add a variable's name when you are less than 70% confident in its code, or when it is inferred rather than explicit. Add `"EXCEPTIONAL"` for polyandry, cross-ethnic marriage, religious figures or captives. Add `"cross_page_extraction"` where it applies.

## Logical constraints

| Condition | Required |
|---|---|
| `1_mar_prac` = 1 | `3_pol_struc` = null |
| `1_mar_prac` = 2 or 3 | `3_pol_struc` in 1–3 |
| `1_mar_prac` = 3 | `3_pol_struc` refers to the polygamous union ONLY |
| `7_obs_location` ≠ 1 | `8_cited_loc` = null |
| `7_obs_location` = 1 | `8_cited_loc` a non-empty string array |
| `9_moral_op` ≠ 1 | `10_stance` = null |
| `9_moral_op` = 1 | `10_stance` a non-empty string |
| no wife-number detail | `13_wives_no` = null and `13_wives_no_notes` = null |
| `14_concubines` = null | `14_concubines_notes` = null |
| `15_dowry` = null | `15_dowry_notes` = null |
| `21_rel_context` ≠ 1 | `21_rel_cited`, `21_rel_quote`, `21_rel_notes` = null |
| `21_rel_context` = 1 | `21_rel_cited` a non-empty array and `21_rel_quote` a non-empty string |

## Examples

These are the v7.1 examples. `1_mar_prac` comes from the filter pass and is not output here.

**Example 1** (filter pass: `1_mar_prac` = 2). Text: "The Waswahili, like all Mahommedans, are allowed by their law to take four wives; but the rich alone can afford to maintain more than one or two. I found this custom degrading to the women."

```json
{"0_subject": 1, "2_mar_diff": 1, "3_pol_struc": 1, "4_ethnic_group": ["Waswahili"], "5_soc_stat": 1, "6_obs_type": 4, "7_obs_location": 2, "8_cited_loc": null, "9_moral_op": 1, "10_stance": "I found this custom degrading to the women.", "13_wives_no": 4, "13_wives_no_notes": "Islamic law permits four; in practice wealth limits most to one or two", "14_concubines": null, "14_concubines_notes": null, "15_dowry": null, "15_dowry_notes": null, "16_gender_roles": null, "17_legality": "Mahommedan law permits up to four wives", "18_kingdoms": null, "19_geo_features": null, "20_historian_flag": null, "21_rel_context": 1, "21_rel_cited": ["Islam (Mahommedan)"], "21_rel_quote": "The Waswahili, like all Mahommedans, are allowed by their law to take four wives", "21_rel_notes": "author's own framing; Islamic law sets four-wife limit; in practice wealth restricts most men to one or two wives", "11_code_conf": 2, "11_conf_note": "5_soc_stat: law universal but practice wealth-dependent", "12_validation_flags": ["5_soc_stat"]}
```

**Example 2** (filter pass: `1_mar_prac` = 3). Text: "The Turks of this province maintain large harems, whilst the Christian Greeks of the same district take but a single wife."

```json
{"0_subject": 4, "2_mar_diff": 1, "3_pol_struc": 3, "4_ethnic_group": ["Turks"], "5_soc_stat": 1, "6_obs_type": 4, "7_obs_location": 2, "8_cited_loc": null, "9_moral_op": 2, "10_stance": null, "13_wives_no": null, "13_wives_no_notes": null, "14_concubines": null, "14_concubines_notes": null, "15_dowry": null, "15_dowry_notes": null, "16_gender_roles": null, "17_legality": null, "18_kingdoms": null, "19_geo_features": null, "20_historian_flag": null, "21_rel_context": 1, "21_rel_cited": ["Christianity (Christian Greeks)"], "21_rel_quote": "the Christian Greeks of the same district take but a single wife", "21_rel_notes": "religious identity used to contrast the two communities' practices; Turks' religion implied by harems but not named", "11_code_conf": 2, "11_conf_note": "monogamy attributed to the Christian Greeks; excluded from arrays per anchor rule; 0_subject ambiguous", "12_validation_flags": ["0_subject", "21_rel_context"]}
```

**Example 3** (filter pass: `1_mar_prac` = 2). Text: "The king of Dahomey, in his palace at Abomey, maintains some three thousand women, divided into wives of various ranks and concubines who serve as soldiers. Each wife received upon entry a payment of ten cowrie strings from the royal treasury, and those of the first rank commanded their own household. A woman taken into the palace could not leave it, nor could she refuse."

```json
{"0_subject": 1, "2_mar_diff": 2, "3_pol_struc": 3, "4_ethnic_group": null, "5_soc_stat": 2, "6_obs_type": 4, "7_obs_location": 1, "8_cited_loc": ["Abomey"], "9_moral_op": 2, "10_stance": null, "13_wives_no": null, "13_wives_no_notes": "approximately three thousand women in the royal palace; ranked hierarchy", "14_concubines": "yes", "14_concubines_notes": "concubines serve as palace soldiers; distinct from ranked wives", "15_dowry": "yes", "15_dowry_notes": "ten cowrie strings paid to each wife upon entry from royal treasury", "16_gender_roles": "A woman taken into the palace could not leave it, nor could she refuse", "17_legality": "internal palace hierarchy: first-rank wives command their own households", "18_kingdoms": ["Dahomey", "king of Dahomey"], "19_geo_features": null, "20_historian_flag": "royal harem ~3000; concubines as soldiers; bride-payment in cowrie strings; full confinement. Strong case study for political economy of elite marriage.", "21_rel_context": 2, "21_rel_cited": null, "21_rel_quote": null, "21_rel_notes": null, "11_code_conf": 1, "11_conf_note": "royal harem ~3000; concubines serve as palace soldiers", "12_validation_flags": ["EXCEPTIONAL"]}
```

**Example 4** (filter pass: `1_mar_prac` = 2). Text: "It is said that in the region between the Lualaba and the Lomami rivers, the Basonge practice a most revolting form of polygamy, in which a man may accumulate wives without limit."

```json
{"0_subject": 1, "2_mar_diff": 1, "3_pol_struc": 3, "4_ethnic_group": ["Basonge"], "5_soc_stat": 1, "6_obs_type": 3, "7_obs_location": 1, "8_cited_loc": ["Lualaba", "Lomami"], "9_moral_op": 1, "10_stance": "a most revolting form of polygamy", "13_wives_no": null, "13_wives_no_notes": null, "14_concubines": null, "14_concubines_notes": null, "15_dowry": null, "15_dowry_notes": null, "16_gender_roles": null, "17_legality": null, "18_kingdoms": null, "19_geo_features": ["Lualaba", "Lomami"], "20_historian_flag": null, "21_rel_context": 2, "21_rel_cited": null, "21_rel_quote": null, "21_rel_notes": null, "11_code_conf": 1, "11_conf_note": null, "12_validation_flags": []}
```

**Example 5** (filter pass: `1_mar_prac` = 2). Text: "Among the Nairs of the Malabar coast, one woman is shared as wife by several brothers simultaneously."

```json
{"0_subject": 1, "2_mar_diff": 1, "3_pol_struc": 3, "4_ethnic_group": ["Nairs"], "5_soc_stat": 1, "6_obs_type": 4, "7_obs_location": 1, "8_cited_loc": ["Malabar"], "9_moral_op": 2, "10_stance": null, "13_wives_no": null, "13_wives_no_notes": null, "14_concubines": null, "14_concubines_notes": null, "15_dowry": null, "15_dowry_notes": null, "16_gender_roles": null, "17_legality": null, "18_kingdoms": null, "19_geo_features": ["Malabar coast"], "20_historian_flag": null, "21_rel_context": 2, "21_rel_cited": null, "21_rel_quote": null, "21_rel_notes": null, "11_code_conf": 1, "11_conf_note": "polyandry: one woman shared as wife by several brothers simultaneously", "12_validation_flags": ["EXCEPTIONAL"]}
```

**Example 6: religion present but not connected** (filter pass: `1_mar_prac` = 2). Text: "The inhabitants are rigid Mahommedans, and the mosque is thronged at every hour of prayer. On the third day we were conducted to the palace of Sultan Bello, who received us seated amongst his wives, of whom he is said to possess above threescore."

```json
{"0_subject": 1, "2_mar_diff": 2, "3_pol_struc": 3, "4_ethnic_group": null, "5_soc_stat": 2, "6_obs_type": 1, "7_obs_location": 2, "8_cited_loc": null, "9_moral_op": 2, "10_stance": null, "13_wives_no": 60, "13_wives_no_notes": "above threescore (60+); hearsay", "14_concubines": null, "14_concubines_notes": null, "15_dowry": null, "15_dowry_notes": null, "16_gender_roles": null, "17_legality": null, "18_kingdoms": ["Sultan Bello"], "19_geo_features": null, "20_historian_flag": null, "21_rel_context": 2, "21_rel_cited": null, "21_rel_quote": null, "21_rel_notes": null, "11_code_conf": 2, "11_conf_note": "religion described but never connected to the marriage practice; wife count is hearsay; prevalence and structure inferred from a single royal case", "12_validation_flags": ["2_mar_diff", "3_pol_struc"]}
```

Islam and the king's polygamy are both described, but no clause links them, so `21_rel_context` = 2. Compare Example 1, where "like all Mahommedans, are allowed by their law" IS the connecting clause.

## Output

Return ONLY a single-line JSON object with these keys, in this order, and no other text:

```json
{"0_subject": X, "2_mar_diff": X, "3_pol_struc": X, "4_ethnic_group": X, "5_soc_stat": X, "6_obs_type": X, "7_obs_location": X, "8_cited_loc": X, "9_moral_op": X, "10_stance": X, "13_wives_no": X, "13_wives_no_notes": X, "14_concubines": X, "14_concubines_notes": X, "15_dowry": X, "15_dowry_notes": X, "16_gender_roles": X, "17_legality": X, "18_kingdoms": X, "19_geo_features": X, "20_historian_flag": X, "21_rel_context": X, "21_rel_cited": X, "21_rel_quote": X, "21_rel_notes": X, "11_code_conf": X, "11_conf_note": X, "12_validation_flags": X}
```
