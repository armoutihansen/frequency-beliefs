# Hamming Interior Single-Transfer Sufficiency -- Exact Search

Step 0a of the Hamming-first plan (`_context/next_steps.md`). Exact rational-arithmetic search for an interior counterexample to: *single-unit-transfer optimality implies global optimality for strictly interior beliefs*.

- Mode: `quick`.
- Arithmetic: exact `fractions.Fraction`; no floating point.
- Random-belief seed: `20260521`.

- self-check 1 (known boundary counterexample n=2,k=3,p=(0,0,1)): PASS -- detected [((0, 2, 0), (0, 0, 2)), ((2, 0, 0), (0, 0, 2))]
- self-check 2 (interior uniform n=8,k=4): PASS -- 0 counterexample(s)

## Search coverage

- k=4: 2800 (belief, n) classifications, 0 interior counterexample(s).
- k=5: 1983 (belief, n) classifications, 85 interior counterexample(s).
- k=6: 863 (belief, n) classifications, 601 interior counterexample(s).
- Total: 5646 (belief, n) classifications, 222345 report-optimality checks.
- Elapsed: 1.6 s.

## Result

REFUTED: 686 interior counterexample(s) found. Single-unit-transfer optimality is NOT sufficient for Hamming at strictly interior beliefs. The interior conjecture is dead; per the Hamming-first plan the fallback is to ship the 3-rule paper unless the simulation spike (Step 0b) still succeeds.

### Counterexamples (first 20)

- n=3, k=5, p=(1/5, 1/5, 1/5, 1/5, 1/5): report r=(0, 0, 0, 0, 3) is single-transfer optimal with G(r)=257/125, but s=(0, 0, 1, 1, 1) has G(s)=272/125 > G(r). All p_i > 0: True.
- n=3, k=5, p=(1/5, 1/5, 1/5, 1/5, 1/5): report r=(0, 0, 0, 3, 0) is single-transfer optimal with G(r)=257/125, but s=(0, 0, 1, 1, 1) has G(s)=272/125 > G(r). All p_i > 0: True.
- n=3, k=5, p=(1/5, 1/5, 1/5, 1/5, 1/5): report r=(0, 0, 3, 0, 0) is single-transfer optimal with G(r)=257/125, but s=(0, 0, 1, 1, 1) has G(s)=272/125 > G(r). All p_i > 0: True.
- n=3, k=5, p=(1/5, 1/5, 1/5, 1/5, 1/5): report r=(0, 3, 0, 0, 0) is single-transfer optimal with G(r)=257/125, but s=(0, 0, 1, 1, 1) has G(s)=272/125 > G(r). All p_i > 0: True.
- n=3, k=5, p=(1/5, 1/5, 1/5, 1/5, 1/5): report r=(3, 0, 0, 0, 0) is single-transfer optimal with G(r)=257/125, but s=(0, 0, 1, 1, 1) has G(s)=272/125 > G(r). All p_i > 0: True.
- n=3, k=5, p=(2/9, 1/9, 2/9, 2/9, 2/9): report r=(0, 3, 0, 0, 0) is single-transfer optimal with G(r)=1373/729, but s=(0, 0, 1, 1, 1) has G(s)=193/81 > G(r). All p_i > 0: True.
- n=2, k=5, p=(2/9, 2/9, 2/9, 1/6, 1/6): report r=(0, 0, 0, 0, 2) is single-transfer optimal with G(r)=137/54, but s=(0, 1, 1, 0, 0) has G(s)=145/54 > G(r). All p_i > 0: True.
- n=2, k=5, p=(2/9, 2/9, 2/9, 1/6, 1/6): report r=(0, 0, 0, 2, 0) is single-transfer optimal with G(r)=137/54, but s=(0, 1, 1, 0, 0) has G(s)=145/54 > G(r). All p_i > 0: True.
- n=2, k=5, p=(65/226, 35/226, 3/113, 27/113, 33/113): report r=(0, 0, 2, 0, 0) is single-transfer optimal with G(r)=58811/25538, but s=(1, 0, 0, 0, 1) has G(s)=156515/51076 > G(r). All p_i > 0: True.
- n=2, k=5, p=(49/222, 15/74, 13/74, 23/111, 43/222): report r=(0, 0, 2, 0, 0) is single-transfer optimal with G(r)=10483/4107, but s=(2, 0, 0, 0, 0) has G(s)=10853/4107 > G(r). All p_i > 0: True.
- n=2, k=5, p=(215/801, 212/801, 19/267, 203/801, 38/267): report r=(0, 0, 2, 0, 0) is single-transfer optimal with G(r)=507713/213867, but s=(1, 1, 0, 0, 0) has G(s)=209425/71289 > G(r). All p_i > 0: True.
- n=2, k=5, p=(27/116, 25/116, 15/116, 23/116, 13/58): report r=(0, 0, 2, 0, 0) is single-transfer optimal with G(r)=143/58, but s=(1, 0, 0, 0, 1) has G(s)=36617/13456 > G(r). All p_i > 0: True.
- n=2, k=5, p=(1/34, 4/17, 4/17, 4/17, 9/34): report r=(2, 0, 0, 0, 0) is single-transfer optimal with G(r)=1327/578, but s=(0, 0, 0, 1, 1) has G(s)=3307/1156 > G(r). All p_i > 0: True.
- n=2, k=5, p=(7/114, 29/114, 29/114, 4/19, 25/114): report r=(2, 0, 0, 0, 0) is single-transfer optimal with G(r)=7630/3249, but s=(0, 1, 1, 0, 0) has G(s)=18665/6498 > G(r). All p_i > 0: True.
- n=3, k=5, p=(5/22, 5/22, 2/11, 3/22, 5/22): report r=(0, 0, 0, 3, 0) is single-transfer optimal with G(r)=10299/5324, but s=(1, 1, 0, 0, 1) has G(s)=292/121 > G(r). All p_i > 0: True.
- n=2, k=5, p=(2/9, 2/9, 5/18, 1/18, 2/9): report r=(0, 0, 0, 2, 0) is single-transfer optimal with G(r)=379/162, but s=(0, 0, 1, 0, 1) has G(s)=923/324 > G(r). All p_i > 0: True.
- n=2, k=5, p=(140/807, 40/807, 73/269, 212/807, 196/807): report r=(0, 2, 0, 0, 0) is single-transfer optimal with G(r)=1519579/651249, but s=(0, 0, 1, 1, 0) has G(s)=1916323/651249 > G(r). All p_i > 0: True.
- n=4, k=5, p=(1/6, 1/6, 1/3, 1/6, 1/6): report r=(0, 0, 4, 0, 0) is single-transfer optimal with G(r)=629/324, but s=(0, 1, 1, 1, 1) has G(s)=293/144 > G(r). All p_i > 0: True.
- n=2, k=5, p=(1/4, 1/5, 1/4, 1/5, 1/10): report r=(0, 0, 0, 0, 2) is single-transfer optimal with G(r)=483/200, but s=(1, 0, 1, 0, 0) has G(s)=71/25 > G(r). All p_i > 0: True.
- n=3, k=5, p=(3/17, 5/17, 3/17, 3/17, 3/17): report r=(0, 3, 0, 0, 0) is single-transfer optimal with G(r)=653/289, but s=(0, 1, 0, 1, 1) has G(s)=11176/4913 > G(r). All p_i > 0: True.

