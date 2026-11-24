# African Marriage Structures

**Polygamy and marriage structures in pre-colonial Africa, reconstructed from European travel writing with a historical codebook and large language models.**

This repository accompanies the working paper:

> Querci, P. and Coetzee, L. (forthcoming). *Elites, Coercion, and the Slave Trade: Unpacking Pre-Colonial African Polygamy.* Special issue on the Murdock Ethnographic Atlas, *Economic History of Developing Regions*.

It holds the annotation pipeline, the codebook, and the documentation of how both were developed and validated.

---

## Why this project

Most quantitative work on African polygamy draws on two sources: the Demographic and Health Surveys, which begin in the 1980s, and Murdock's *Ethnographic Atlas*. The Atlas gives each society a single value for its marriage system, describing an "ethnographic present" that for most African societies dates to the colonial period. It assumes two kinds of uniformity: within a group over time, and across the members of a group at any one time. It records most African societies simply as "polygamous", with no variation in how common the practice was, who practised it, or the conditions of women within it.

Both sources come long after the slave trade, Christian missions, colonial rule and legal reform had already reshaped marriage on the continent. The "polygamy belt" running from Senegal across to Ethiopia has largely been treated as a deep, stable pattern rather than tested against earlier evidence.

This project tests those assumptions against an earlier, independent body of evidence: European travellers' accounts of Africa written between c.1500 and 1900. Traveller accounts are not ethnographies. They are scattered, often second-hand, and shaped by their authors' religious, political and commercial backgrounds. But each observation can be dated, placed, and attributed to a specific author. They record variation that the Atlas reduces to one value: between ranks, between town and countryside, and across decades.

## Research questions

1. **Distribution:** Where and when do travellers record polygamy, and how does this compare with the static picture in the *Ethnographic Atlas*?
2. **Social stratification:** Was polygamy a general practice or concentrated among political and economic elites, and did this change over time?
3. **Regional variation:** Do the characteristics of polygamy differ across North, West, East, Central and Southern Africa?
4. **Women's conditions:** Were descriptions of wives' status in polygamous marriages different from those in monogamous marriages?
5. **States and polygamy:** Is the presence of historical states associated with the documentation of polygamy?
6. **The slave trade:** Is exposure to the Atlantic slave trade associated with the later documentation of polygamy?

The analysis is ongoing and the results in the paper are still being revised, so findings are not reported here. See the paper once it is published.

## Data

**Source corpus.** The [Time Traveller](https://timetraveller.voyage) corpus of digitised European travel narratives on Africa, 1500–1900 (Kerby, Moradi and Odendaal 2025, *Economic History Review*). Each volume is linked to traveller-level metadata: occupation, nationality, language, journey dates, and countries visited.

**Unit of analysis.** A single keyword hit, together with a three-page context window (the page before the hit, the hit page, and the page after). The study works at the level of the *statement* rather than the group: group-level characterisations are treated as a result to be supported, not a starting premise.

**Keyword search.** A hand-made list of terms (e.g. *polygamy*, *polygyn~*, *first wife*, *chief wife*, *marriage among*, *custom of marriage*) was validated and expanded with [ConceptNet](https://conceptnet.io). The final list has 57 proximity-searched terms, 46 of which returned hits, giving 8,353 coded rows after deduplication.

The source texts remain subject to the Time Traveller Project's terms and are not redistributed here.

## Method: a historical codebook executed by an LLM

A codebook is a written set of variables, each with a fixed set of values, rules for choosing between them, and worked examples. Here it does three jobs:

- **Operationalisation:** it turns contested concepts (polygamy, bride-wealth, the household) into bounded, observable categories, and makes the historian's interpretive choices explicit.
- **Standardisation:** every passage is assessed against the same questions, whether a historian or a model does the coding.
- **Accountability:** every coded value is tied to a passage, a page, a book and a journey, with a record of how reliable it is.

When a language model does the coding, the codebook stops being guidance for a trained reader and becomes the full set of instructions the model executes. Anything the codebook leaves unsaid is filled by the model's everyday sense of a word. So each rule is written out explicitly, with edge cases and worked examples, and the model must quote the text its decision rests on.

### Pipeline (codebook v8.7.1)

| | |
|---|---|
| **Model** | Claude Haiku 4.5 (`claude-haiku-4-5-20251001`) |
| **Temperature** | 0.2, chosen after testing 0.0–1.0 on a stratified 50-row sample: 0.0 was too literal, and 0.4 and above made the model overconfident and flag fewer cases for review |
| **Text** | Full three-page window |
| **Passes** | Two: a filter pass on every row, then an extraction pass on usable observations only |

**Pass 1: filter (every row).** Codes the marriage practice at the hit (`1_mar_prac`: monogamy, polygamy, both, or not applicable) and how usable that content is (`22_discreteness`: substantive, incidental, non-discrete, or none).

A practice is coded only from a **discrete observation**: a named person, an office holder, or a named people whose marriage the text reports. The following are recorded as non-discrete rather than discarded, so the share of unusable marriage material can itself be reported:

- harem scenery with no identified man;
- literary and biblical allusions;
- rhetoric and metaphor;
- index entries;
- "married" with no type given.

**Pass 2: extraction (usable observations only).** Codes who is married (`0_subject`), plus:

- prevalence, polygamy structure, social status, and observation type (direct witness, long-term resident, hearsay, or general statement);
- ethnic groups, locations, kingdoms, and geographic features;
- number of wives, concubines, bride-wealth, stated laws, and wives' status;
- the author's moral stance, and the religious context.

Names, places and quotations are copied verbatim. Religion is coded as linked to the practice only when the text connects the two, not when a mosque or mission simply appears nearby. When a passage contrasts monogamy with polygamy, all variables describe the polygamous side. There are no "unclear" codes: uncertain variables get the best-fitting code and are flagged for human review.

### Validation

- **Gold standard:** a stratified sample of 360 passages, by region and period, hand-coded by the two authors using the full three-page window. Each author coded 130 alone, and 100 were coded by both.
- **Out-of-sample testing:** from v8.5 onward, codebook rules were derived from the 260 single-coder rows and tested on the 100 shared rows, which were held out.
- **Errors reported both ways:** false positives and false negatives are reported separately, and error rates are checked by region and period for systematic bias.

### Development principle

When the model and the human coders disagreed, the **instructions were revised, not the model settings**. Each error was traced to a rule the coders applied without stating it, and that rule was written into the codebook.

When a wider context window performed worse on some variables, the response was to state which variables may draw on the wider window and to anchor every code on the keyword hit, not to shrink the window to fit this dataset. Tuning parameters to one corpus would produce a method that works under one configuration and transfers to no one else's data. It would also repeat, in the method, the flattening of evidence that the paper criticises in the *Ethnographic Atlas*.

The full version history (v0 to v8.7.1), with the rationale and test results for each change, is documented in the paper's web appendix.

## Repository contents

| File | Description |
|---|---|
| `haiku_marriage_classifier_twostage_v5.ipynb` | Early pipeline, historical codebook v1 |
| `haiku_marriage_classifier_twostage_v6.ipynb` | Two-stage pipeline with the v2 codebook revisions |

*To be added:* the v8.7.1 codebook (filter and extraction passes), the v8.x run scripts, and the codebook development appendix.

## Reproducibility

An LLM-based instrument can only be reproduced if the model version, its settings, the prompts and the raw outputs are recorded. This repository archives the codebook versions and the pipeline code. Model outputs will be released alongside the paper.

To run the notebooks, you need your own Anthropic API key. Store it as an environment variable or a Colab secret; never hard-code it in a notebook.

## Authors

- **Pietro Querci**: Free University of Bozen-Bolzano; University of Trento
- **Lauren Coetzee**: Centre for Contemporary and Digital History (C²DH), University of Luxembourg · [ORCID 0000-0002-0829-1936](https://orcid.org/0000-0002-0829-1936)

## Citation

If you use the codebook or pipeline, please cite the paper (forthcoming) and this repository:

```
Coetzee, L. and Querci, P. (2026). African Marriage Structures: historical codebook
and LLM annotation pipeline, v8.7.1. GitHub.
https://github.com/laurencoetzee001/african_marriage_structures
```

## License

Code in this repository is released under the [MIT License](LICENSE).
