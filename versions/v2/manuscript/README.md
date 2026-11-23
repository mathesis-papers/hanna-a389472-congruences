# Integral-product extensions for OEIS A389472, revision 7, COMMENT 3

The congruence `3 | a(3n-1)` for every integer `n > 1` was proved by
Horace Dong (2026), Section 3, Theorem 4, archived on September 26, 2026:
<https://doi.org/10.5281/zenodo.22970816>.
This note gives an alternative recurrence proof, with
`a(0)=0`, `a(1)=a(2)=1` and `A(x²+x³)=x²(1+A(x))`.
The note also proves the parity companion, the factor-six consequence,
the radius `(sqrt(5)-1)/2`, the inverse-series and iterated-substitution
identities, and the relation `A(x)=x+H(x)²` to A350432.
The parity conclusion was proved by Adrian Perez Fontelles in his manuscript
dated August 31, 2026, Section 4:
<https://github.com/astrafala/Conjectures/blob/58cf4596af4541652fb191e177ef9b7771388d53/paper-sources/01001-01500/01042-PROOF.tex>.
The product gives all integer solutions `A_b=x+bH²`. The general family
`Q=x^d(1+epsilon*x)^s` supplies the functional, inverse and positive-radius
identities in A369545--A369549 and A369552--A369556, and the signed product
identities of A350433 and A350434. In A273162, revision 12, the second
FORMULA's product is the inverse series, not the sequence's generating
function; the coefficient comparison is `+1` versus `-1` at degree two.

## Files and reproduction

- `note.tex`: complete mathematical arguments and references.
- `note.pdf`: typeset note.
- `metadata.json`: title, creators, license and scientific coverage.
- `verify.py`: standard-library Python 3 exact-arithmetic checks.
- `checks.json`: expected output at degree 1000.
- `source-prefixes.json`: source coefficient prefixes, entry versions and URLs.

Build with **Tectonic 0.17.0**:

```sh
tectonic note.tex
```

Or use a standard LaTeX installation (the bibliography is embedded):

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

Run the finite checks:

```sh
python3 verify.py > actual-checks.json
diff -u checks.json actual-checks.json
```

The two coefficient constructions use different formulas: binomial recurrence
and multiplication of iterated polynomial factors. They agree through degree
1000. The checks reproduce the displayed source prefixes, all congruence
instances in that range, and the base-three binomial lemma for upper index
at most 300. The extended checks use exact arithmetic through degree 64,
compare all displayed coefficients of fifteen related entries, check 28
functional/inverse identities, and test fourteen two-sided series reversions.
The all-index conclusions follow from the written proofs.

## Sources and mathematical scope

- Primary posing source: <https://oeis.org/history/view?seq=A389472&v=7>,
  COMMENT 3 (modulo three), COMMENT 2 (parity), COMMENT 1 (radius),
  FORMULAS (1)--(3).
- Hanna's product for A350432:
  <https://oeis.org/history/view?seq=A350432&v=13>, FORMULA (3).
- Modulo-three Lean declaration:
  <https://github.com/the-omega-institute/trureturing/blob/074df09ddbbef1843ddb383577bfaa827f753e36/D5/S1/Recurrence/Parity/SquareCubeSubstitutionThreeIndexModThree.lean>,
  `D5.S1.Recurrence.Parity.SquareCubeSubstitutionThreeIndexModThree.result`.
- Normalization, recurrence and parity declarations:
  <https://github.com/the-omega-institute/trureturing/blob/074df09ddbbef1843ddb383577bfaa827f753e36/D5/S1/Recurrence/Parity/SquareCubeSubstitutionOddIndexParity.lean>,
  `generating_equation`, `generating_unique`, `coeff_recurrence`,
  `hanna_conjecture` in namespace
  `D5.S1.Recurrence.Parity.SquareCubeSubstitutionOddIndexParity`.
- Dong's earlier declaration for every integer solution of the functional equation:
  <https://github.com/Horace-Maxwell/ai4math-results/blob/4c9a4c2b6945ed4f12ba8bdd66c398869081b4f6/lean/Research/Oeis389472Mod3.lean>,
  `Oeis389472Mod3.integer_conjecture`; it does not prescribe the second coefficient.

The product, analytic radius, inverse-series and iteration results are written
proofs in the note. The same product argument also proves the radius and
inverse-series identity stated in A350432. The factor-six statement follows
from the two congruences.
The EXAMPLE field's decimal evaluations are outside the finite-check coverage.
The cross-referenced entries and exact versions are listed in
`source-prefixes.json`. Their products are Hanna's stated constructions;
the note proves the specified identities and gives the corrected inverse
assignment in A273162. No assertion of priority accompanies the extensions.

## Creators and license

1. Haobo Ma — ChronoAI Pte Ltd, Singapore.
2. Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore.

CC BY 4.0: <https://creativecommons.org/licenses/by/4.0/>.
The source ZIP contains the TeX, this README, metadata, checker and expected
output and source prefixes; the PDF is supplied separately.
