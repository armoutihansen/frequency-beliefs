Run a citation and literature-risk pass.

Steps:

1. Read:
   - `_context/current_status.md`
   - `_context/current_issues.md`
   - `_context/related_literature/README.md`
   - `_context/exploration/literature_scan_log.md`
   - `paper/references.bib`

2. Inspect the requested paper section.
   If no section is specified, start with:
   - `paper/sections/01_introduction.tex`
   - `paper/sections/03_scoring_rules.tex`
   - `paper/sections/06_risk_attitudes.tex`

3. Use the `literature-reviewer` agent.

4. Report:
   - claims needing citation;
   - citations that may not support the claim;
   - missing citations;
   - uncertain bibliographic details;
   - novelty risks;
   - suggested edits.

Do not invent citations or page numbers.
Do not edit bibliography unless explicitly asked.