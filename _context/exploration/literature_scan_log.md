# Literature Scan Log

## 2026-05-21 — Targeted scan on the three novelty surfaces (N1/N2/N3) + binary-lottery citations

Mode: exploration. All findings below are from online SEARCH METADATA (publisher
pages, RePEc, Econometric Society, arXiv abstracts). No full PDFs were read in
this pass; bibliographic details are reliable for citation, but claims about
what each paper proves must be checked against the PDFs before entering the
manuscript.

### Search objective

Position the paper's three novelty claims and find the closest prior work:
N2 = four-rule comparison of frequency/count scoring rules by inferential
precision; N1 = partial-identification ("identified set") framing of
scoring-rule inversion; N3 = closed-form inverse region for a count-based
quadratic-distance rule. Plus: verify the binary-lottery payment citations
needed by ADR-0002.

### Search terms used

"binarized scoring rule" Hossain Okui; Roth Malouf 1979 binary lottery;
Karni 2009 mechanism eliciting probabilities; comparison count frequency-report
scoring rules interval bounds multinomial; Lambert Pennock Shoham eliciting
properties probability distributions; Manski partial identification beliefs
elicited; Armantier Treich eliciting beliefs European Economic Review;
Schlag Tremewan simple belief elicitation published; identified set beliefs
scoring rule revealed preference; quadratic distance count vector inverse
region; Berg Daley Dickhaut O'Brien 1986; nondistortionary belief elicitation
arXiv 2025; Dynamic Belief Elicitation Lambert Econometrica.

### Verified bibliographic details (metadata only)

- Schlag, Tremewan & van der Weele, "A Penny for Your Thoughts," Experimental
  Economics 18:457-490 (2015). [bib has "Manuscript 2013" — CORRECT IT]
- Schlag & Tremewan, "Simple belief elicitation: An experimental evaluation,"
  Journal of Risk and Uncertainty (2021), DOI 10.1007/s11166-021-09349-6. An
  earlier 2014 working paper (same main title) had no experiment. [bib has
  "Manuscript 2016" — CORRECT IT; decide which version carries the bounds method]
- Armantier & Treich, "Eliciting Beliefs...," European Economic Review
  62(C):17-40 (2013), EER Best Paper Award 2013. [bib has "Manuscript 2012" —
  CORRECT IT]
- Hossain & Okui, "The Binarized Scoring Rule," Review of Economic Studies
  80(3):984-1001 (2013). [NOT in bib — ADD]
- Karni, "A Mechanism for Eliciting Probabilities," Econometrica
  77(2):603-606 (2009). [NOT in bib — ADD, required by ADR-0002]
- Roth & Malouf, "Game-Theoretic Models and the Role of Information in
  Bargaining," Psychological Review 86:574-594 (1979). [NOT in bib — ADD;
  caveat: this is the bargaining paper that USES binary lotteries; the
  binary-lottery-for-utility-control lineage is Smith (1961) -> Roth-Malouf
  (1979) -> Berg et al. (1986)]
- Berg, Daley, Dickhaut & O'Brien, "Controlling Preferences for Lotteries on
  Units of Experimental Exchange," Quarterly Journal of Economics
  101(2):281-306 (1986). [NOT in bib — ADD]
- Lambert, Pennock & Shoham, "Eliciting Properties of Probability
  Distributions," EC'08, Proc. 9th ACM Conf. on Electronic Commerce,
  pp. 129-138 (2008). [NOT in bib — ADD, relevant to N1]
- Chambers & Lambert, "Dynamic Belief Elicitation," Econometrica
  89(1):375-414 (2021). [NOT in bib — N1 context]
- Pęski & Stewart, "Nondistortionary belief elicitation," arXiv:2506.12167
  (2025), working paper. [recent; competitor-adjacent]

### Direct competitors

- N2 (primary): Schlag & Tremewan is the CLOSEST prior work. Their frequency
  method already "identifies bounds on beliefs" (not point identification),
  robust to risk aversion, trading precision for generality — and the paper's
  discrete-metric rule IS their exact-match mechanism. The paper does not invent
  belief-bounds-from-frequency-reports.
- N1: the belief-identification literature (Chambers-Lambert "Dynamic Belief
  Elicitation"; "Belief identification with state-dependent utilities,"
  arXiv:2203.10505) concerns POINT identification of beliefs by a mechanism and
  impossibility results — adjacent but distinct from a partial-identification
  SET from one count report. Property-elicitation / elicitability
  (Lambert-Pennock-Shoham) is the other adjacent strand.
- N3: no prior count-based quadratic inverse-region result surfaced. The
  quadratic-score / squared-Euclidean-distance link is standard but stated on
  probabilities, not counts.

### Novelty risks

- N2 is the MOST exposed. A referee will ask "what is new beyond
  Schlag-Tremewan?" The answer must be crisp and up front: the four-rule
  comparison, the quadratic closed-form inverse region, the partial-ID framing,
  and the design exercise over (n,k,p). The paper must never claim to have
  invented frequency-report belief bounds.
- N1 medium risk: "identified set" is partly a relabeling. It must do real work
  (sharpness statements, the design exercise as identified-set comparison),
  and must cite the partial-ID anchors (Manski, Tamer, Molinari), none of which
  are currently in the bib.
- N3 low risk pending the proof audit; likely new as a count-based result, but
  do not oversell originality of the rule itself, only of the inverse region.

### Missing literatures

Binarized scoring rule (Hossain-Okui) — directly relevant: the ADR-0002
binary-lottery payment IS the binarized scoring rule; currently uncited.
Binary-lottery lineage (Smith 1961, Roth-Malouf 1979, Berg et al. 1986, Karni
2009) — uncited. Property elicitation / elicitability (Lambert-Pennock-Shoham;
Frongillo-Kash). Partial identification proper (Manski 2003 "Partial
Identification of Probability Distributions"; Tamer 2010 Annual Review;
Molinari 2020 handbook chapter) — all uncited. Schlag-van der Weele "Most
Likely Interval" / interval scoring rule. Recent robust elicitation
(Pęski-Stewart 2025).

### Implications for the paper's direction

The partial-ID reframing is supportable but N1 must cite Manski/Tamer/Molinari
and make the framing load-bearing. N2 positioning must be sharpened explicitly
against Schlag-Tremewan. The binary-lottery discussion (Section 06) currently
attributes the technique only to Armantier-Treich and the Schlag survey — this
is insufficient attribution and must be corrected.

### Recommended next searches

Frongillo-Kash elicitation complexity; Smith (1961) binary-lottery origin;
Tamer (2010) and Molinari (2020) exact citations; partial identification with
experimental/incentivized data; the 2026 follow-up "How to Ask for Belief
Statistics without Distortion?" (arXiv:2602.10474) for competitor overlap.

### Recommended manuscript changes

Bibliography: correct ArmantierTreich (2013, EER), SchlagEtAl (2015, Exp Econ),
SchlagTremewanSimple (2021, JRU); add Hossain-Okui 2013, Karni 2009,
Roth-Malouf 1979, Berg et al. 1986, Lambert-Pennock-Shoham 2008,
Chambers-Lambert 2021, Manski (partial-ID book), Tamer 2010, Molinari 2020.
Introduction/positioning: state the four-rule + quadratic-closed-form +
partial-ID contribution explicitly against Schlag-Tremewan. Section 06: expand
the binary-lottery attribution. All "what the paper proves" claims must be
checked against the PDFs (several relevant PDFs are already local in
_context/related_literature/) before manuscript entry.

---

## Scan 2026-05-22 — related-work expansion (front-matter contrast pass)

Triggered by a request to capture all related papers and contrast the paper's
approach/findings to theirs. `_context/library.bib` was checked: it is a general
Zotero export with almost no belief-elicitation-specific entries, so the scan
relied on substantial web search. A `literature-reviewer` agent ran the search;
all citation details below were independently verified against publisher /
RePEc / Semantic Scholar metadata.

### Papers added to `paper/references.bib` and cited

- Gneiting 2011 (JASA 106(494):746--762) — elicitability; squared loss elicits
  the mean, absolute loss the median. Cited at the mean/median framing.
- Lambert, Pennock & Shoham 2008 (EC '08:129--138) — a functional is elicitable
  iff its level sets are convex. Cited with Gneiting.
- Heinrich 2014 (Biometrika 101(1):245--251) — the mode is not elicitable for
  general continuous distributions. Cited to flag that the discrete-metric
  rule elicits the multinomial mode only because the count space is discrete.
- Schotter & Trevino 2014 (Ann. Rev. Econ. 6:103--128); Charness, Gneezy &
  Rasocha 2021 (JEBO 189:234--256) — belief-elicitation method surveys.
- Trautmann & van de Kuilen 2015 (Econ. J. 125(589):2116--2135) — "horse race"
  among truth serums; contrasted as recovering a point belief vs our identified
  set conditional on optimal reporting.
- Offerman, Sonnemans, van de Kuilen & Wakker 2009 (RES 76(4):1461--1489) —
  ex-post risk-attitude correction of scoring rules; the alternative to our
  rule/implementation choice.
- Danz, Vesterlund & Wilson 2022 (AER 112(9):2851--2883) — behavioural
  incentive compatibility fails; cited as the explicit scope condition.
- Gigerenzer & Hoffrage 1995 (Psych. Review 102(4):684--704) — frequency
  formats aid Bayesian reasoning; suggestive support for the count format.
- Manski 2004 (Econometrica 72(5):1329--1376); Engelberg, Manski & Williams
  2009 (JBES 27(1):30--41); Delavande, Giné & McKenzie 2011 (JDE 94(2):151--163)
  — survey elicitation of subjective distributions / count-format elicitation.
- Harrison, Martínez-Correa & Swarthout 2014 (JEBO 101:128--140) — binary
  lotteries applied to probability elicitation; added to the binarized-rule
  citation list.

Note: the literature agent initially mis-attributed Danz et al. as
"Danz, Vespa, Wilson"; the correct middle author is Lise Vesterlund (verified).

### Manuscript changes made (guardrail mode)

- New "Related literature" block at the end of `01_introduction.tex` (three
  paragraphs): elicitability; elicitation-method/truth-serum/behavioural-IC
  literature; count-format elicitation. Positions the contribution as treating
  the scoring-rule optimality condition as the identifying restriction.
- `03_scoring_rules.tex`: point-of-use Gneiting cites at the quadratic
  "mean-oriented" and Manhattan "median-oriented" interpretations.
- `07_discussion.tex`: Offerman 2009 added as the ex-post-correction
  alternative; Harrison 2014 added to the binary-lottery citation; Danz et al.
  2022 added as an optimal-reporting scope condition in the open-question
  subsection.

### Novelty assessment

No paper was found that set-identifies beliefs by inverting a scoring-rule
optimal-report correspondence. The partial-identification machinery (Manski)
and the elicitability dictionary (Gneiting, Lambert et al.) are not new and are
now cited rather than claimed. The defensible novelty — characterizing the
mechanism-induced identified set P_S(r) for distance-based count rules — is
stated as such. No full papers were read end-to-end in this scan; the contrasts
drawn use well-established results of the cited work.

---

## Scan 2026-05-22 (cont.) — full-text read of cited literature, intro/discussion revision

Followed the request to read and understand all cited papers, then sharpen the
contrasts. PDFs of the citable papers were downloaded into
`_context/related_literature/` (see its README). Read in full or in depth:
Schlag--Tremewan 2021, Schlag et al. 2013, Armantier--Treich 2013,
Danz--Vesterlund--Wilson 2022, Gneiting 2011, Lambert--Pennock--Shoham 2008
(SIGecom highlights), Offerman et al. 2009, Engelberg--Manski--Williams 2009,
Harrison et al. 2014. Four paywalled papers (Heinrich 2014, Schotter--Trevino
2014, Trautmann--van de Kuilen 2015, Delavande et al. 2011) could not be
obtained; positioning of these rests on abstracts and well-established results.

### What the reading changed

- **Schlag--Tremewan is a closer relative than the earlier draft conveyed.**
  They already establish, for frequency guessing: optimal report = multinomial
  mode; the consistent beliefs form a simplex region; the region yields LP
  bounds on probabilities, means, and variances. The whole region-and-bounds
  program exists for that one rule. The honest contribution is to (a) name it
  partial identification with the mechanism's optimality as the identifying
  restriction, (b) extend it to quadratic (closed form) and Manhattan, (c)
  compare. The intro's "Related literature" block was rewritten to lead with
  this and state it precisely.
- **Engelberg--Manski--Williams already bound means/medians/modes from coarse
  interval-probability reports** — so set-valued inference about a belief
  distribution from a coarse report is not new. The difference is the
  identifying restriction: they take reported probabilities at face value;
  here the set is cut out by the scoring rule's optimality condition. This is
  now stated in the intro.
- **Danz--Vesterlund--Wilson directly test the binarized scoring rule** — the
  exact implementation the discussion proposes for distance rules — and find
  centre-biased misreporting driven by the incentive information, *not* by risk
  attitude. **Harrison et al. 2014**, by contrast, find the binary-lottery
  procedure does induce approximately risk-neutral reporting. The discussion's
  risk-aversion subsection was revised to present both: the technique resolves
  the risk-attitude problem but leaves a separate behavioural one open.
- Gneiting/Lambert: the mean/median framing is their elicitability dictionary;
  the mode has maximal elicitation complexity (Lambert et al.) and is not
  elicitable in the continuous case (Heinrich). Stated as "applied, not
  invented."

### Manuscript changes

- `01_introduction.tex`: "Related literature" block rewritten into four
  paragraphs — frequency guessing (Schlag--Tremewan), elicitability
  (Gneiting/Lambert/Heinrich), what a coarse report identifies
  (Engelberg--Manski--Williams, Manski 2004, Delavande et al.), and the
  elicitation-methods/risk-attitude literature (Schlag et al., Schotter--Trevino,
  Charness et al., Armantier--Treich, Trautmann--van de Kuilen, Offerman et al.,
  Danz--Vesterlund--Wilson).
- `07_discussion.tex`: risk-aversion subsection expanded with the Harrison
  (supportive) and Danz et al. (cautionary) evidence on the binary-lottery
  implementation; Harrison 2014 moved out of the technique-origin citation.
  Open-question subsection trimmed to cross-reference rather than repeat.
- Paper compiles cleanly (25 pages, no undefined references).

---

## 2026-05-22 — notation and scoring-rule naming review

A review of the manuscript's notation/definitions against the literature now
read in full. Findings and author decisions:

- "identified set" / "sharp bounds" / $P_S(r)$ (parallels Schlag--Tremewan's
  $P^u_b$) / Manhattan-Hamming-Chebyshev distance names: consistent with the
  literature — kept.
- "exact identified set" vs "sharp bounds": flagged, then judged acceptable
  (exact = the set, sharp = the bounds is a workable distinction; forcing
  "sharp" for both creates redundancy) — kept.
- "quadratic-distance scoring" collided with the *quadratic scoring rule*
  (QSR). Renamed to **squared-distance scoring** manuscript-wide.
- "discrete-metric scoring" was the paper's taxonomic rename of the established
  *frequency guessing* (Schlag--Tremewan). Renamed to **frequency-guessing
  scoring**; the metric $D_0$ is still "the discrete metric".
- "informational efficiency" (title) collided with the EMH sense. Changed to
  **informativeness** throughout, including the title.
- "scoring rule" was never disambiguated from *proper* scoring rules — §2 now
  states these are not proper and that the optimal report is a functional of
  the sampling distribution, with inference by inversion.
- "frequency report" vs "count" — §2 now states a frequency report is a vector
  of counts, not relative frequencies.
- Found and fixed an internal inconsistency: the appendix proof used $S_2$ for
  the squared rule while §3 used $S_Q$; unified on $S_Q$.

Subscripts $S_Q, P_Q, S_0, P_0$ kept (defined labels; renaming risks cross-ref
breakage for no reader benefit). Scripts and `CLAUDE.md` not yet synced.
