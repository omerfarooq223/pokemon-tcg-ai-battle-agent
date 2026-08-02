# How to Build V9 Yourself

This guide is intentionally practical. You do not need to understand the whole agent before making a useful experiment.

## 1. Start From a Safe Copy

Never edit a submitted agent. Create V9 from the strongest stable starting point:

```bash
cp -R agents/v8_candidate agents/v9_candidate
```

Work only inside `agents/v9_candidate/`. Its two important files are:

- `deck.csv`: the exact 60-card deck.
- `main.py`: the decision policy.

Keep a small `README.md` in the folder with your idea and every test result. This prevents repeating failed experiments.

## 2. Choose One Clear Idea

Change only one main idea at a time. Good examples:

- Replace one Trainer with another.
- Change the number of one Pokémon.
- Prefer a different attacker in a specific board state.
- Search for a backup Basic when only one Pokémon is in play.
- Heal only after a useful damage threshold.

Avoid changing the deck and ten policy rules together. If the result improves, you will not know which change helped.

Before editing, write a one-sentence hypothesis:

> “Adding one more recovery card should reduce board-exhaustion losses without making setup slower.”

That sentence tells you what matchup to test and what failure to watch for.

## 3. Editing the Deck

Each line of `deck.csv` is one card ID. The file must contain exactly 60 lines.

Check the size:

```bash
wc -l agents/v9_candidate/deck.csv
```

Find a card in the English card data:

```bash
rg -i "card name" competition_data/EN_Card_Data.csv
```

After changing the deck, update `EXPECTED_DECK` inside `agents/v9_candidate/main.py` to the same 60 IDs. The embedded list protects the Kaggle agent from loading the wrong deck.

Do not add opponent names, replay IDs, or rules that activate against one particular player. Use card properties and visible game state instead.

## 4. Editing the Policy

The most useful sections of `main.py` are:

- `ATTACKS`: attack costs and damage for important Pokémon.
- `POKEMON_ROLE`: general value of each Pokémon.
- `score_play_from_hand`: which cards to play.
- `score_attach_or_evolve`: where Energy and evolutions should go.
- `score_target_selection`: which Pokémon or card to select.
- `score_attack`: which attack to use.
- `bounded_setup_choice`: the few actions allowed before a legal attack.

Important safety rule: if the agent can attack, it must not keep performing setup until the turn ends. Preserve the repeated-menu attack guard unless a replacement is tested very carefully.

Ask Codex for a narrow change when you have quota. A useful request looks like:

> “In `agents/v9_candidate`, add this one general rule: when we have only one Pokémon in play, prefer searching for a Basic backup. Do not modify any submitted version. Run 200 swapped-seat games against V8 and report attack safety.”

## 5. Test in Layers

### A. Quick legality check

```bash
python3 -m py_compile agents/v9_candidate/main.py
python3 tools/run_local_matches.py --matches 20 --agent-dir agents/v9_candidate --opponent random --swap-seats
```

Stop immediately if there is an invalid choice, timeout, crash, or wrong deck size.

### B. Small comparison

```bash
python3 tools/run_local_matches.py --matches 200 --agent-dir agents/v9_candidate --opponent-dir agents/v8_candidate --opponent agent --swap-seats --quiet
```

The result format is:

```text
summary primary=104 opponent=94 draws=2
```

Here, V9 won 104 and V8 won 94. A small lead is only a signal, not proof.

### C. Compare with important older agents

```bash
python3 tools/run_local_matches.py --matches 1000 --agent-dir agents/v9_candidate --opponent-dir agents/v5_candidate --opponent agent --swap-seats --quiet
python3 tools/run_local_matches.py --matches 1000 --agent-dir agents/v9_candidate --opponent-dir agents/v7_candidate --opponent agent --swap-seats --quiet
```

Always use `--swap-seats`. Going first or second can otherwise distort the result.

### D. Stress the known weaknesses

```bash
python3 tools/run_local_matches.py --matches 500 --agent-dir agents/v9_candidate --opponent-dir experiments/stress_agents/alakazam --opponent agent --swap-seats --quiet
python3 tools/run_local_matches.py --matches 500 --agent-dir agents/v9_candidate --opponent-dir experiments/stress_agents/grimmsnarl --opponent agent --swap-seats --quiet
```

A change should solve the problem it targets without collapsing the normal comparison.

### E. Audit attack safety

```bash
python3 - <<'PY'
from pathlib import Path
from tools.compare_v5_v6_v7 import head_to_head
print(head_to_head(Path("agents/v9_candidate"), Path("agents/v8_candidate"), 1000))
PY
```

Require `abandoned_attack_turns: 0`. The displayed `attack_rate` counts repeated menus, so abandoned attack turns are the more important safety number.

## 6. Decide Whether the Change Is Real

Use these minimum promotion rules:

- Zero crashes, invalid actions, and timeouts.
- Zero abandoned attack-capable turns.
- At least 52.5% of decisive games over 5,000 swapped-seat games against the chosen incumbent for a claimed policy improvement.
- No major regression against known stress decks.
- A clear reason for the improvement, not only one lucky result.

Local replay simulations are rejection tools, not leaderboard predictions. They can prove that an idea is broken, but a 95% local result does not guarantee a high Kaggle rating.

If a 200-game result looks promising, rerun it at 1,000. If that still looks promising, run 5,000. Do not spend time on 5,000 games for every idea.

## 7. Build the Upload File

Only package V9 after it passes the tests:

```bash
python3 tools/build_submission.py --agent-dir agents/v9_candidate --output artifacts/submission_9.tar.gz
tar -tzf artifacts/submission_9.tar.gz
```

The archive should contain only:

```text
main.py
deck.csv
```

The build tool checks Python startup, raw Kaggle loading without `__file__`, the 60-card deck, and archive contents.

Do not upload immediately after packaging. First record the final test results and file hashes in `AGENTS.md`. Uploading is a separate decision.

## 8. Learn From Live Matches

For every V9 replay:

1. Save both wins and losses.
2. Confirm whether V9 attacked whenever a legal attack turn appeared.
3. Identify the actual loss type: setup failure, damage ceiling, Energy denial, board exhaustion, target choice, or matchup structure.
4. Look for the same failure in multiple games before changing policy.
5. Prefer one general fix that helps several decks.

Track four numbers separately:

- Peak score.
- Settled/current score.
- Time active.
- Replay win-loss record.

Do not judge V9 from one screenshot. V5 peaked at 965 while later displaying around 790, and V7 peaked at 914 before settling around 775-800.

## Recommended First V9 Experiment

Do not begin with a completely new 60-card deck. Start from V8 and test one general board-resilience or resource-denial improvement. The Starmie/Cinderace prototype already failed its first direct screen, and the existing Alakazam and Diggersby prototypes also failed broad gates. A careful one-change experiment will teach you more than another large rewrite.

Episode 88527351 gives the first live V8 target. V8 attacked on every one of its six attack-capable turns and took five prizes, so do not alter the attack guard in response. It lost because a Grimmsnarl ex/Munkidori counter engine gradually exhausted a board containing only two Crustle. It also played a late Buddy-Buddy Poffin that could no longer produce useful board progress.

A suitable first hypothesis is:

> “Avoiding no-progress Poffin plays and improving access to one genuinely useful backup Pokémon should reduce counter/spread board-exhaustion losses without filling the Bench with easy prizes.”

Test the two parts separately. Start with the no-progress Poffin rule because it is a narrow policy change. Treat extra Pokémon, changed search counts, or a different Basic as separate deck experiments. Compare each experiment against V8 normally and against the Grimmsnarl stress agent; require zero abandoned attack turns. Do not simply force Poffin earlier or always fill the Bench—the previous broad Poffin-before-disruption experiment already regressed several matchups.
