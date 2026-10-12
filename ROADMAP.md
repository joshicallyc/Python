# Learning Roadmap: Computing & Machine Learning for Bioengineering

*Started October 2026. This is a living document: check boxes off, cross things out, and add a line to the
[progress log](#progress-log) at the bottom every week.*

**Goal:** build real computing/ML skills for disease diagnostics and drug development. Join a UCLA lab during
the 2026–27 school year, then take linear algebra, statistics, and programming courses in year 2.

---

## 1. The short answer: is Python the starting point?

**Yes.** For what you want to do, it isn't close:

- **ML runs on Python.** scikit-learn (classical ML) and PyTorch (deep learning) are Python libraries.
- **Biology runs on Python too.** Biopython (sequences), scanpy (single-cell), scikit-image and Cellpose (microscopy),
  RDKit and DeepChem (drug molecules), and AlphaFold tooling are all Python.
- **Most lab code you'll inherit is Python** (some genomics and biostatistics labs use R; see the note in Phase 5).
- **You've already started.** Your DNA translator is a real bioinformatics task.

**Change how you learn it, though.** Python got boring because you were learning the language with nothing to
apply it to. Web dev showed you results right away, but it was the wrong field and took too long. The fix is to
use Python on biological data from day one, in Jupyter notebooks, where a plot or table shows up as soon as you
run a cell. **Every week should end with something you can see:** a figure, a table, or a model's score.

**About ML roadmaps (including the one in the video):** most of them say *Python → math → classical ML → deep
learning → projects*. This plan keeps that order but **learns the math alongside the code instead of all up front.**
You'll see why linear algebra matters (your data *is* a matrix) before you take Math 33A, and the course will
make more sense because of it.

---

## 2. What "computing" in a bio lab actually means

When a lab says it does "computational" or "ML" work, it usually means some mix of these:

| Kind of work | What it looks like day to day | Main tools | Fit for you |
|---|---|---|---|
| **Data analysis & scripting** | Cleaning instrument/assay output, statistics, making figures for papers | Python, pandas, matplotlib, Jupyter | **The most common undergrad job.** Everything else builds on it |
| **Image analysis** | Counting/measuring cells in microscopy, analyzing test-strip or sensor images | scikit-image, Cellpose, napari, CNNs | Central to **diagnostics** |
| **Sequence / genomics bioinformatics** | Processing sequencing data, finding variants, gene expression | command line, Biopython, R/Bioconductor, scanpy | Core of the **bioinformatics minor** |
| **Machine learning modeling** | Predicting disease from data, predicting molecule properties | scikit-learn, PyTorch | Both **diagnostics and drug development** |
| **Simulation & modeling** | ODE models of biological systems, molecular dynamics of proteins | NumPy/SciPy, OpenMM, GROMACS | Where **biophysics** shows up |

**Takeaway:** ML sits on top of data analysis. Someone who can reliably load, clean, plot, and analyze data in
Python is already useful to a lab, and that's the person who gets handed the ML project later.

---

## 3. The plan at a glance

| Phase | When | Focus | What you'll have built |
|---|---|---|---|
| **0** | Oct 2026 (≈2 weeks) | Set up tools; fix the DNA translator | A working translator, checked against Biopython |
| **1** | Oct–Dec 2026 (fall) | Python for biology | Rosalind solutions, a sequence toolkit, your first plots |
| **2** | Jan–Mar 2027 (winter) | Data analysis, statistics, command line | 2 notebooks on real data (one of them imaging) |
| **3** | Apr–Jun 2027 (spring) | Classical ML (scikit-learn) | A diagnostic classifier and a drug-property predictor |
| **4** | Summer 2027 | Intro to deep learning | A medical-image classifier |
| **5** | 2027–28 and beyond | UCLA courses formalize the math/CS; specialize through your lab | Research-grade work in a lab |

**The lab search runs alongside all of this** (see [section 10](#10-getting-into-a-lab-this-year)). Start emailing
in late fall or the first week or two of winter. **Don't wait until you feel "ready."**

---

## 4. Weekly rhythm (about 5–6 hours/week during the quarter)

| Session | Length | What |
|---|---|---|
| **Learn** | ~1 hr | One video or reading (StatQuest, a tutorial chapter, etc.) |
| **Build ×2** | ~2 hr each | Write code: an exercise or a piece of the current project |
| **Log** | 10 min | Add one line to the progress log: what you did and what confused you |

Rules that make this stick:

1. **Consistency beats intensity.** 30 minutes during finals week is better than zero. Breaking the streak is how
   the last two attempts ended.
2. **Results first.** If you've gone a week without producing a plot, table, or number, change what you're doing.
3. **Type the code yourself**, even when copying from a tutorial. Your fingers learn the syntax.
4. **Got stuck? Use the 20-minute rule:** try for 20 minutes, then ask (Claude, Stack Overflow, a classmate, a TA).
5. **Commit to GitHub every build session.** Your GitHub is your lab résumé (see section 10).

---

## 5. Phase 0: Set up your workbench and fix the translator (≈2 weeks, now)

### Setup
- [ ] Install **Python with Miniconda** (or Anaconda) so you can create environments and install packages.
      For zero setup, **[Google Colab](https://colab.research.google.com)** runs notebooks in the browser and is
      enough for Phases 1–4.
- [ ] Install **VS Code** with the Python and Jupyter extensions.
- [ ] Learn the **basic git loop** from your own computer: `git add` → `git commit -m "..."` → `git push`, instead of
      uploading files on the GitHub website.
      ([Software Carpentry: Git](https://swcarpentry.github.io/git-novice/), episodes 1–7)
- [ ] Organize the repo so it reads well to a professor (suggested):
      ```
      Python/
        README.md            ← portfolio front page: link each project + one figure
        ROADMAP.md           ← this file
        CLI_project/         ← Phase 0
        web/                 ← move the HTML/CSS projects here
        01_python_bio/       ← Phase 1
        02_data_analysis/    ← Phase 2
        03_ml/               ← Phase 3
        04_deep_learning/    ← Phase 4
      ```

### Fix the DNA translator (`CLI_project/reader.py`)
Right now the script only writes the FASTA header to `codon.txt`; **no amino acids come out.** That makes it a
good first debugging exercise. Work through these hints in order, and try each one before asking for the answer:

- [ ] **The real bug:** `for codon in output:` loops over the string **one letter at a time**, so a single letter
      can never equal `'AUG'`. How do you loop over 3-letter chunks? (Hint: you already wrote the
      `range(0, len(output), 3)` loop. It just throws away each codon it makes.)
- [ ] `elif codon == ('GUU', 'GUC', ...)` compares a string to a tuple, so it's always `False`. What operator did
      you use correctly on the lines above it?
- [ ] **FASTA sequences span several lines.** Translating line by line splits codons across line breaks. Collect all
      sequence lines into one string first, then translate.
- [ ] **A biology question to settle and document:** your code builds the *complement* (A→U, T→A, C→G, G→C).
      GenBank FASTA records are usually the *coding (sense) strand*, and its mRNA is the same sequence with T→U.
      Which strand is in your file, and which conversion is correct?
- [ ] Replace the `elif` chain with a **dictionary** holding all 64 codons (your README already says the program uses
      dictionaries), and stop at stop codons.
- [ ] Use `with open(...) as f:` so files close properly, and add an `--output` argument instead of hard-coding
      `codon.txt`.
- [ ] Split the code into **functions**: `read_fasta()`, `transcribe()`, `translate()`.
- [ ] **Check your answer** against Biopython: `from Bio.Seq import Seq; Seq(dna).translate()`.
      Professionals test their code against a trusted reference like this all the time.
- [ ] Rename `humandna.fasta.html` to `humandna.fasta` (it's a FASTA file, not a web page) and run the translator on
      it too.

---

## 6. Phase 1: Python for biology (Oct–Dec 2026)

**Skills:** functions, lists and dictionaries, loops over files, string methods, list comprehensions, importing
modules, reading documentation, writing a small module that other scripts import.

**Main resource: [Rosalind](https://rosalind.info).** It's a set of bioinformatics problems with instant
auto-grading. It feels like puzzles instead of lectures, and each problem is real biology.

- [ ] **Python Village** (INI1–INI6): fast review of what you know, plus files and dictionaries
- [ ] **Bioinformatics Stronghold**, roughly in this order:
  - [ ] DNA (counting nucleotides)
  - [ ] RNA (transcription)
  - [ ] REVC (reverse complement)
  - [ ] FIB (recurrence relations)
  - [ ] GC (GC content)
  - [ ] HAMM (point mutations)
  - [ ] PROT (translation, which redoes your translator properly)
  - [ ] SUBS (finding a motif)
  - [ ] IPRB (Mendel's first law)
  - [ ] CONS (consensus and profile)
  - [ ] PRTM (protein mass)
  - [ ] REVP (restriction sites)
  - [ ] SPLC (RNA splicing)
  - [ ] ORF (open reading frames)
- [ ] **[Biopython](https://biopython.org)** tutorial: `SeqIO` for reading FASTA/GenBank, `Seq` objects, and
      `Entrez` for downloading a sequence from NCBI by accession number

**Project: sequence toolkit** (`01_python_bio/`)
- [ ] Write `seqtools.py` with functions you wrote for Rosalind: `gc_content`, `reverse_complement`, `transcribe`,
      `translate`, `find_orfs`
- [ ] Write a script that imports it, reads a multi-gene FASTA, and **plots GC content per gene** with
      matplotlib. This is your first figure.
- [ ] Stretch: a **sliding-window GC plot** along a whole small genome (e.g., a bacteriophage or SARS-CoV-2,
      downloaded from NCBI). This is a real bioinformatics figure.
- [ ] Write a README with what it does, how to run it, and the figure

**Math alongside:** none required yet. If you're curious, start
[3Blue1Brown's *Essence of Linear Algebra*](https://www.3blue1brown.com/topics/linear-algebra) (short videos with
strong visuals).

---

## 7. Phase 2: Data analysis, statistics, and the command line (Jan–Mar 2027)

**Skills:** Jupyter notebooks; NumPy arrays; pandas DataFrames (load CSV, filter, `groupby`, merge); matplotlib and
seaborn plots; descriptive statistics; t-tests, p-values, and why testing many genes at once needs a
multiple-testing correction; basic Unix shell.

**Resources**
- [Kaggle Learn](https://www.kaggle.com/learn): *Pandas* and *Data Visualization* (short, browser-based, free)
- [Software Carpentry: Plotting and Programming in Python](https://swcarpentry.github.io/python-novice-gapminder/)
- [StatQuest](https://statquest.org) statistics videos (p-values, t-tests, distributions). Josh Starmer was a
  genetics researcher, so the examples often use biology.
- [Software Carpentry: The Unix Shell](https://swcarpentry.github.io/shell-novice/) and
  [MIT's Missing Semester](https://missing.csail.mit.edu). Bioinformatics happens on the command line.
- [Data Carpentry: Image Processing with Python](https://datacarpentry.org/image-processing/) for the imaging
  project
- **UCLA QCBio Collaboratory workshops:** free for UCLA students. They regularly run Intro to Python and other
  computational-biology workshops. Check the
  [workshop schedule](https://qcb.ucla.edu/collaboratory/schedule-of-workshops/) each quarter; registration means
  committing to every session.

**Projects** (do at least two, in `02_data_analysis/`)
- [ ] **A. Diagnostic data exploration:** load scikit-learn's built-in **Breast Cancer Wisconsin (Diagnostic)**
      dataset (`sklearn.datasets.load_breast_cancer`). Its features were measured from microscope images of
      biopsies. Plot how each feature differs between benign and malignant samples, and find which features
      separate them best. *This sets up Phase 3.*
- [ ] **B. Microscopy image analysis:** count and measure nuclei with scikit-image (threshold → segment → label →
      measure). Start with the built-in `skimage.data.human_mitosis()` image, then try a real set from the
      [Broad Bioimage Benchmark Collection](https://bbbc.broadinstitute.org). *This is exactly how many diagnostics
      labs use code.*
- [ ] **C. Gene expression:** download a disease-vs-control dataset from [NCBI GEO](https://www.ncbi.nlm.nih.gov/geo/),
      test each gene for differences, correct for multiple testing, and make a **volcano plot**.

**Math alongside:** finish *Essence of Linear Algebra*. Watch for this idea: a dataset with 500 samples and 30
features is a 500×30 matrix, and much of ML is matrix operations.

---

## 8. Phase 3: Classical machine learning (Apr–Jun 2027)

**Concepts to understand:**
- Supervised vs unsupervised learning; features and labels
- Train/validation/test splits; **overfitting**; cross-validation
- Models: linear and logistic regression, k-nearest neighbors, decision trees and random forests, PCA, clustering
- **Evaluation:** confusion matrix, **sensitivity, specificity**, precision, ROC curves and AUC. These are the same
  numbers used to evaluate real diagnostic tests (for example, a UCLA-developed COVID-19 testing device reported 98%
  sensitivity and 100% specificity on 100 clinical samples). You'll understand diagnostics papers better after this phase.
- Data leakage, class imbalance, and why a model that's "95% accurate" can be useless

**Resources**
- [StatQuest machine learning videos](https://statquest.org): watch the video before coding each model
- Kaggle Learn: *Intro to Machine Learning* → *Intermediate Machine Learning*
- Andrew Ng's [Machine Learning Specialization](https://www.coursera.org/specializations/machine-learning-introduction),
  courses 1–2 (check for audit/financial-aid options)
- Reference book: Aurélien Géron, *Hands-On Machine Learning with Scikit-Learn and PyTorch* (O'Reilly, 2025),
  Part I. Check UCLA Library for free e-book access.
- [scikit-learn user guide](https://scikit-learn.org/stable/user_guide.html)

**Projects** (`03_ml/`)
- [ ] **Diagnostic classifier (diagnostics track):** on the Breast Cancer Wisconsin data, train logistic regression and
      a random forest, then report sensitivity, specificity, and ROC-AUC with cross-validation. Then answer: *in
      cancer screening, is a false negative or a false positive worse? How would you move the decision threshold?*
      Write the README like a mini paper: question, data, methods, results figure, limitations.
- [ ] **Molecular property predictor (drug-development track):** predict a drug-relevant property such as aqueous
      solubility from molecular structure. Get the data from [Therapeutics Data Commons](https://tdcommons.ai)
      (ADME datasets; `pip install PyTDC`), turn SMILES strings into fingerprints with [RDKit](https://www.rdkit.org),
      and train a random forest.
- [ ] **Unsupervised:** PCA + clustering on a gene expression dataset (e.g., cancer subtypes). Do the clusters match
      the known labels?

**Math alongside:** probability basics (Khan Academy or StatQuest). Also the idea of a derivative as "which
direction is downhill." That idea, **gradient descent**, is how models learn.

---

## 9. Phase 4: Intro to deep learning (Summer 2027)

**Resources**
- [3Blue1Brown: Neural Networks](https://www.3blue1brown.com/topics/neural-networks) to understand what's happening
- [fast.ai: Practical Deep Learning for Coders](https://course.fast.ai). It's **top-down**: you train a working
  image classifier in lesson 1 and learn the theory afterward, which suits how you like to learn.
- [PyTorch: Learn the Basics](https://pytorch.org/tutorials/beginner/basics/intro.html)
- Géron, Part II
- Use **Google Colab's free GPU**; no special hardware needed

**Projects** (`04_deep_learning/`)
- [ ] **Medical image classifier:** use [MedMNIST](https://medmnist.com) (small, standardized medical image datasets
      such as blood cells, pathology, and skin lesions). Train a small CNN, then a pretrained model (transfer
      learning), and compare both against a simple baseline. Report sensitivity and specificity per class.
- [ ] *(Drug track)* A neural network on molecules with [DeepChem](https://deepchem.io) tutorials, compared with
      your Phase 3 random forest
- [ ] *(Biophysics tie-in)* Pick a disease-relevant protein, get its predicted structure from the
      [AlphaFold Database](https://alphafold.ebi.ac.uk), and view it in ChimeraX or PyMOL. Learn what the
      confidence score (pLDDT) means.

---

## 10. Getting into a lab this year

### What professors actually look for in a first-year
- **Reliability and time:** about 10+ hours/week, consistently, for multiple quarters
- **Curiosity and coachability:** you read their work and ask good questions
- **Coding skills are a bonus that sets you apart.** Most first-years have none. A GitHub with 2–3 clean,
  well-documented biology-data projects stands out.

**Hybrid route (very common):** join a diagnostics lab in a wet-lab role and volunteer to help with data analysis.
Many people move into the computational side this way.

### Timeline
- [ ] **Now–November:** finish Phase 0 and start Phase 1. List **10–15 labs**. For each, read 1–2 recent paper
      abstracts and write one sentence in your own words about what they do.
- [ ] **Late Nov / weeks 0–2 of winter:** email PIs in batches of about 5. Follow up once after about 7–10 days.
      Also try emailing a grad student or postdoc in the lab; they often manage undergrads and reply faster.
- [ ] **Once someone says yes:** set up **SRP 99** credit through the
      [Undergraduate Research Center–Sciences](https://sciences.ugresearch.ucla.edu). It's for lower-division
      students. You need a faculty mentor first, and the contract is due **Friday of week 2** of the quarter.
- [ ] **Later:** the bioinformatics minor lets research units (CS/Bioinformatics 194/199) count as electives

### Where to look (diagnostics / drug development / computational)
- **[Ozcan lab](https://innovate.ee.ucla.edu)** (ECE + Bioengineering): computational imaging and deep learning for
  diagnostics, including virtual staining, smartphone microscopy, and deep-learning-enhanced point-of-care tests
- **[Di Carlo lab](https://samueli.ucla.edu/people/dino-di-carlo/)** (Bioengineering): microfluidics and single-cell
  diagnostics. Its deformability cytometry became an FDA-cleared sepsis test, and the lab co-authors on ML for
  point-of-care testing.
- **[Bioengineering: Biomedical Data Sciences track](https://www.bioeng.ucla.edu/biomedical-data-sciences/):** faculty
  and courses applying ML to biomedical problems
- **[Department of Computational Medicine](https://compmed.ucla.edu):** bioinformatics, genomics, and ML on health
  data
- **[UCLA Medical Imaging Informatics](https://mii.ucla.edu):** ML on medical images
- **QCBio-affiliated faculty** ([qcb.ucla.edu](https://qcb.ucla.edu)): computational biology across campus
- **Summer programs:** [B.I.G. Summer](https://qcb.ucla.edu/big-summer/) (Bruins-in-Genomics), an 8-week
  computational-biology research program. As of 2026 it focuses on students **sponsored by a UCLA faculty member**,
  which is one more reason to get into a lab early. Deadlines have been around March–May.
- **Clubs** for peers and project experience: DataRes (free quarter-long data-science courses), Data Science Union,
  National Student Data Corps (aimed at newer students)

### Email template
> **Subject:** First-year interested in [specific topic] research
>
> Dear Professor [Name],
>
> I'm a first-year Biophysics major at UCLA interested in [disease diagnostics / drug development]. I read your
> [year] paper on [topic], and I was especially interested in [one specific point, in your own words].
>
> I've been teaching myself Python for biological data analysis. For example, I [one-line project 1] and
> [one-line project 2] (github.com/joshicallyc/python). I'd be glad to contribute on the computational side or at
> the bench, and I can commit about [10] hours/week starting [winter quarter].
>
> Would you have time for a short meeting, or is there a graduate student or postdoc I could talk with? My CV is
> attached.
>
> Thank you,
> Josh Li

Keep it under about 150 words. The specific sentence about their paper is the part that gets replies.

---

## 11. Phase 5: Year 2 and beyond. UCLA courses formalize everything

*Course numbers are from UCLA pages as of 2026. **Confirm with the catalog and your advisor**, because
requirements change.*

| Need | UCLA course(s) | Notes |
|---|---|---|
| Linear algebra | **Math 33A** | Likely already in your major's preparation (it is for Physics); also required to apply to the bioinformatics minor |
| Probability / statistics | **Stats 100A** (or the other options listed by the minor) | Required for ML theory |
| Programming | **PIC 10A → 10B → 10C** or **CS 31 → 32** | These are in **C++**, not Python. That's fine: the concepts transfer, and C++ teaches what the computer is actually doing. The minor requires CS 32 or PIC 10C. |
| Discrete math | **Math 61** | Bioinformatics minor prerequisite |
| Biology | **LS 7A** (or LS 3) | Bioinformatics minor prerequisite |
| Bioinformatics core | **CM121** (intro), **CM122** (algorithms), **CM124** (computational genetics) | Plus a gateway seminar, an algorithms course, and an elective. See the [minor's page](https://www.seasoasa.ucla.edu/bioinf/) for the current count. |
| Machine learning | **CS M146** (Intro to ML) | Past offerings expected linear algebra, multivariable calculus, probability, and algorithms |

> **Heads-up about your major:** in April 2026, UCLA Physics & Astronomy announced it will **suspend admission to the
> Biophysics BS** (Fall 2026 for continuing students, Fall 2027 for new admits). It also plans to propose
> discontinuing the major. Students who entered as new Biophysics majors in Fall 2026 **can continue in the
> major**. Since you're also aiming at bioengineering, it's worth one meeting with a Physics & Astronomy advisor
> this year to confirm your path. ([department page](https://www.pa.ucla.edu/majors-and-requirements.html),
> [Daily Bruin](https://dailybruin.com/2026/04/13/ucla-physics-and-astronomy-department-to-suspend-admission-to-biophysics-major/))

**Self-study that pairs with those courses**
- [*An Introduction to Statistical Learning with Python* (ISLP)](https://www.statlearning.com): free and the standard
  text. Read it alongside Stats 100A / Math 33A.
- [*Mathematics for Machine Learning*](https://mml-book.github.io): free. It shows how linear algebra and probability
  turn into ML.
- Géron, cover to cover; Andrew Ng's Deep Learning Specialization

**Specialize, guided by your lab:**
- **Diagnostics:** image analysis (CNNs, segmentation, Cellpose), sensor/signal data, and evaluation (ROC,
  calibration, validation on independent patient groups)
- **Drug development:** cheminformatics (RDKit, molecular fingerprints, graph neural networks), protein structure
  (AlphaFold), and molecular dynamics (OpenMM), which is where biophysics pays off
- **Bioinformatics / genomics:** sequencing pipelines on the command line, RNA-seq, single-cell (scanpy). **R note:**
  many genomics labs use R (DESeq2, Seurat). Don't learn it now. If your lab uses it, your Python foundation lets
  you pick it up in a few weeks.

---

## 12. Using AI tools (including Claude) without stunting your learning

- **Try first** (20–30 minutes), then ask.
- On exercises, **ask for hints and explanations**, not full solutions: "What's wrong with my loop and why?"
- **Be able to explain every line** you commit. In a lab, someone will ask, and you'll need to fix it when it breaks.
- **Use AI as a code reviewer:** paste your working code and ask how a professional would improve it.
- Labs increasingly use AI coding tools. They want people who can **check whether the output is right**, and that
  takes the fundamentals this plan builds.

---

## 13. Resource index

| Area | Resource |
|---|---|
| Python + biology | [Rosalind](https://rosalind.info) · [Biopython](https://biopython.org) |
| Notebooks / setup | [Google Colab](https://colab.research.google.com) · Miniconda · VS Code |
| Data skills | [Kaggle Learn](https://www.kaggle.com/learn) · [Software Carpentry](https://software-carpentry.org/lessons/) · [Data Carpentry Image Processing](https://datacarpentry.org/image-processing/) |
| Command line / git | [Missing Semester](https://missing.csail.mit.edu) · [SWC Shell](https://swcarpentry.github.io/shell-novice/) · [SWC Git](https://swcarpentry.github.io/git-novice/) |
| Statistics + ML intuition | [StatQuest](https://statquest.org) |
| Math intuition | [3Blue1Brown](https://www.3blue1brown.com) (linear algebra, neural networks) |
| ML courses | [Andrew Ng ML Specialization](https://www.coursera.org/specializations/machine-learning-introduction) · [fast.ai](https://course.fast.ai) · [PyTorch tutorials](https://pytorch.org/tutorials/) |
| Books | Géron, *Hands-On ML with Scikit-Learn and PyTorch* (2025) · [ISLP](https://www.statlearning.com) (free) · [Mathematics for ML](https://mml-book.github.io) (free) |
| Bio datasets | [NCBI GEO](https://www.ncbi.nlm.nih.gov/geo/) · [BBBC images](https://bbbc.broadinstitute.org) · [MedMNIST](https://medmnist.com) · [AlphaFold DB](https://alphafold.ebi.ac.uk) |
| Drug discovery | [TDC](https://tdcommons.ai) · [RDKit](https://www.rdkit.org) · [DeepChem](https://deepchem.io) |
| UCLA | [QCBio Collaboratory](https://qcb.ucla.edu/collaboratory/schedule-of-workshops/) · [URC–Sciences](https://sciences.ugresearch.ucla.edu) · [Bioinformatics minor](https://www.seasoasa.ucla.edu/bioinf/) · [BioE Biomedical Data Sciences](https://www.bioeng.ucla.edu/biomedical-data-sciences/) · [B.I.G. Summer](https://qcb.ucla.edu/big-summer/) |

---

## Progress log

*One line per week. Patterns in the "stuck on" column show what to review.*

| Week of | What I did | What I learned / got stuck on |
|---|---|---|
| 2026-10-12 | Wrote this roadmap | |
