# Context for Claude

This repo is Josh Li's long-running learning project: building computing and machine-learning skills for
bioengineering (disease diagnostics and drug development). **ROADMAP.md is the plan and the record of progress.**

## Background (snapshot as of October 2026; update as things change)
- UCLA first-year (started Fall 2026), Biophysics major, interested in diagnostics and drug development;
  considering a bioinformatics minor.
- **Summer 2026:** Python basics (strings, loops, conditionals) and `CLI_project/reader.py`, a DNA → mRNA → protein
  translator; then basic HTML/CSS (`survey.html`, `cafe_menu.html`).
- **Still learning:** functions, dictionaries in practice, NumPy/pandas, plotting, command-line git.
- Learns best with **short, visual tasks on real biological data**. Time is limited during the quarter.
- **Goal:** join a UCLA lab during 2026–27; take linear algebra, statistics, and programming courses in year 2.

## How to help
- **Teach, don't just solve.** On exercises, give hints and explain the *why* before giving full solutions. If Josh
  explicitly asks for the full code, give it and explain it line by line.
- Pitch explanations at a beginner level and connect concepts to biology whenever possible.
- Prefer tasks that end in something visible: a plot, a table, a model score.
- Each project gets its own folder with a README (what it does, how to run it, a result figure). This GitHub
  doubles as a portfolio for lab applications.
- Use Python 3. Use Jupyter/Colab notebooks for data exploration and `.py` scripts for reusable tools.

## Tracking system
Each kind of information has exactly **one** home. Don't create other trackers or tracking files.

| What | Home |
|---|---|
| The plan, and which items are done (IDs like `P0-05`) | `ROADMAP.md` |
| Weekly history of coding and learning | Progress log at the bottom of `ROADMAP.md` |
| This week's tasks, week mode, Sunday check-in, Parking lot | Josh's private Notion page **"Coding Now"** |
| Saved explanations ("save this") | Notion subpages under Josh's **Coding** page |
| Daily habits, classes, assignments, reflections | Josh's existing Notion pages (**read-only** for Claude) |
| Lab outreach and hard deadlines | Private (Notion / Google Calendar). **Never in this repo.** |

### Commands Josh may use
- **"start"**: pull the latest `main`. Read ROADMAP.md (the current phase is the first one with unchecked items) and,
  if the Notion connector is available, "Coding Now". Reply in 5 lines or fewer: phase progress, tonight's goal,
  what "done" looks like. Skip this for quick standalone questions.
- **"wrap up"**: propose which ROADMAP items to check off (by ID) and a one-line progress-log entry, then wait for
  Josh's "yes". Before checking off a build item, ask one quick "explain why this works" question. It's a teaching
  moment, not a gate. Commit the bookkeeping together with the session's work, never as a separate
  bookkeeping-only PR. If the work is on a branch, ask whether to open a PR so Josh can merge it before the session
  ends. Then update Claude's sections of "Coding Now": tick finished tasks, set the next 15-minute step, and update
  "Last updated".
- **"plan my week"**: refill "Coding Now" using the mode Josh picked in the Sunday check-in
  (Normal / Light / Exam / Break; ROADMAP section 4 defines them; the page's quarter map is the fallback) and
  the next unchecked ROADMAP items. Each task gets an ID, a time estimate, and a first step. Move last week's tasks
  into the "Last week" toggle.
- **"save this"**: create a Notion subpage under **Coding** titled `Python: <topic> — Reference Notes`, in the
  same style as the existing HTML/CSS reference notes.
- **"park this"**: add the question to the Parking lot on "Coding Now".

### Rules
- Never check off an item Josh didn't confirm. IDs are never renumbered or reused; dropped items are ~~struck
  through~~.
- On "Coding Now", edit only Claude's sections. Never delete or overwrite Josh's check-in or Parking-lot text,
  and avoid full-page rewrites. Never change the schema of Josh's existing Notion databases.
- If "Coding Now" can't be found, ask. Never create a duplicate. If its "Last updated" is more than 8 days old,
  say so and offer to re-plan.
- No Notion connector (e.g. a local session)? Work from ROADMAP.md and `git log`, and give Josh a short
  paste-ready update for the page instead.
- **This repo is public. Write everything as if a professor will read it.** Leave out grades, exam dates,
  schedules, academic plans, personal notes, and anything that ties a named professor to outreach status, notes,
  or emails. The progress log covers coding and learning only.
- Professor emails go out from Josh's UCLA account, so give paste-ready text and don't create Gmail drafts.
