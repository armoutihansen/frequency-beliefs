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
