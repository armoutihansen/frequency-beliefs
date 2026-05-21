# Risk neutrality in the body; binary-lottery extension in the discussion

The body of the paper analyzes optimal reporting and identified sets under the maintained assumption that the subject is risk-neutral, and the discussion shows that the same analysis carries through to risk-averse subjects under expected utility when the scoring rule is implemented via the binary-lottery / probabilistic-payment scheme (Roth–Malouf 1979, Karni 2009). We chose this exposition order — risk-neutrality first, binary-lottery extension second — because the analytical content (optimal-report correspondence, identified set, bounds) is identical under either framing, but the risk-neutral framing keeps the body's setup lean and matches conventional scoring-rule exposition; the binary-lottery extension is then a familiar move in the elicitation literature rather than a foundational mechanism choice imposed in the setup.

## Considered Options

- **Binary-lottery payment as maintained frame from the start.** Front-loads mechanism complexity, requires the reader to reason about a probabilistic-payment compound lottery before the theorems begin, and partially offsets the paper's separate cognitive-load argument for frequency reports. Rejected in favor of the cleaner exposition order.
- **Risk neutrality in body, risk aversion handled only via a brief mention in discussion.** Too thin for venue B — a referee will ask about risk aversion and expect a substantive engagement.
- **Risk neutrality in body, binary-lottery extension as a substantive discussion (sub)section.** Adopted.

## Consequences

- Setup (`paper/sections/02_setup.tex`) states risk neutrality as the maintained assumption and does not introduce binary-lottery payment.
- The introduction and abstract make scope claims under risk-neutral optimal reporting only; the EU + binary-lottery extension is described separately. No "robust to risk aversion" claim appears in the abstract without the qualifier.
- The risk-aversion section becomes part of the discussion (or a short Implementation section), structured as: (a) the binary-lottery transformation, (b) citations to Roth–Malouf, Karni, and an experimental treatment (Berg et al. 1986 or Selten et al. 1999), (c) the statement that the body's analysis extends under EU + binary-lottery, (d) departures from EU flagged as out of scope.
- Bibliography must include Roth–Malouf (1979), Karni (2009 Econometrica), and one of Berg–Daley–Dickhaut–O'Brien (1986) or Selten–Sadrieh–Abbink (1999). Citation pass should verify these exist in `paper/references.bib`.
- The CLAUDE.md interpretation-risk note — "Do not claim distance rules are robust to risk aversion under direct monetary payments" — is preserved by construction: the body never claims direct-monetary + risk-averse robustness, and the discussion claims robustness only under EU + binary-lottery. Future edits must preserve this scope distinction; the danger is a sloppy edit that elides the framing.
- The discussion paragraph or subsection on the binary-lottery extension must be written tightly enough that it cannot be misread as claiming direct-monetary risk-aversion robustness.
