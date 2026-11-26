# CHANGES_StripIII_v2: the release copy of the proof trees StripIII, StripIIIM1 and StripIIIM2

These sources are the archived sources of the proof trees StripIII, StripIIIM1 and StripIIIM2 with recorded changes to comments and
docstrings only. No line of code changed: the module names, the declaration names, every statement and every proof are those of the
archived trees. SCRUBBED_FILES.tsv lists every file of src/ with the sha256 of its archived original and of the shipped copy.

## The StripIII part
The 21 StripIII files start from the earlier release copy of this tree, made for a previous version of the paper. Four docstrings
change in content: the module docstrings of StripIII.Core (line 3) and StripIII.Statement (lines 2 and 3) name the paper by its title
and DOI and part (f) of Theorem 6.34, in place of a conjecture label that the paper no longer has; the docstring of hBoxAll5 in
StripIII.Small5Statement (line 31) states the orbit step; and the module docstring of StripIII.FinalIII (line 5) points to this file.
Every citation of the paper gives its printed number (see below). Each file's comment-stripped text equals that of its earlier copy.

## The StripIIIM1 and StripIIIM2 parts
- Form: for each file, a list of exact replacements of whole comment lines, each with its count of occurrences, and two replacements
  inside comments that follow code on their line. Every replacement lies inside one comment and keeps its number of lines and its
  comment delimiters, so every file keeps its line count and every declaration keeps its position.
- Content:
  - internal names, working paths, the names of other working documents and notes of the build history are removed or replaced by the
    role they name ("the converter", "an independent enumeration of the to-do pairs");
  - the records are cited by their paths in this package and the sha256 of the shipped files (first 8 hex digits, or all 64 in the
    first comment line of each list fragment); the comment lines of each list fragment are the lines its converter prints on the
    shipped records, so the checksums they quote are those of the shipped files;
  - the paper's results are cited by their printed numbers: Theorem 6.34 (f) and Theorem 1.4 (i), Propositions B.22 and B.24 (with the
    checks of the proof of Proposition B.24), Lemma B.23, Propositions B.17 and B.18, Lemma 6.2, Theorem 3.2 and
    Appendix B.

## Citations of the paper
The paper is "Positive correlation of bond energies in the O(3) and O(4) models" (DOI 10.5281/zenodo.24410344). Every citation of one
of its results gives the number that the paper prints. The numbers were set by one mechanical pass from the paper's final build: each
LaTeX label in these texts was replaced by the number that the build's aux file gives it (a label without a kind word by its kind and
number), inside comments only, with every file's comment-stripped text and line count checked unchanged.

## Checks
1. The transformation's own asserts: every replacement found its count of occurrences inside a comment, and every file kept its line
   count.
2. Comment-stripped equality: with every comment removed (line and nested block comments; string and character literals kept), each
   shipped file equals its archived original. A copy with one numeral changed in code is reported as different.
3. Full rebuild from these sources against G2Kernel_Lb_p13 and Mathlib: every module compiles (lean/rebuild/StripIII_v2_summary.txt).
   Each module's build product equals that of the archived build in its imports, its constant names, and for every constant its kind,
   universe parameters, type and value (Expr.equal); a SAME control and a DIFF control run beside it.
4. The `#print axioms` lines (lean/rebuild/StripIII_v2_axioms.log) are identical to those of the archived builds: only `propext`,
   `Classical.choice` and `Quot.sound` occur.
5. Every hash in a docstring is the sha256 of the shipped file it names, recomputed on the final package.
6. Each list fragment is regenerated from its shipped record by its converter and found verbatim in its module.
7. Scans of the shipped files find no internal names, working paths, host names, stand-in words, open-work markers, names of paper
   drafts or names of earlier copies; every result they cite by number has that number and kind in the paper's final build, every cited
   part is present, and no LaTeX label is left.
