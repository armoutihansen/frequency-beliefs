Revise a specified paper section.

Required input:
- target section;
- revision goal.

If no target section is specified, ask for one.

Steps:

1. Read:
   - `_context/current_status.md`
   - `_context/current_issues.md`
   - `_context/exploration/direction_memos.md`
   - `paper/main.tex`
   - target section

2. Determine whether the revision is:
   - current-framing revision; or
   - adoption of an explored direction.

3. If adopting an explored direction, first run the academic-claim-discipline skill.

4. Use:
   - `paper-editor` for prose;
   - `theory-auditor` for formal claims;
   - `literature-reviewer` for citation claims.

5. Make minimal coherent edits unless broad rewriting is explicitly requested.

Rules:

- Preserve notation.
- Do not invent citations.
- Do not add unsupported claims.
- Avoid broad rewrites unless requested.
- Keep claims calibrated.
- Preserve the mechanism → optimal reports → inverse regions → bounds → design comparison → implementation/risk attitudes pipeline unless the user explicitly approves a direction change.

After editing, summarize:

1. files changed;
2. substantive changes;
3. claims softened or clarified;
4. remaining risks.