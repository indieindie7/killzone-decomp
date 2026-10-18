# Killzone (PlayStation 2, Guerrilla Games / SCE, 2004) reverse-engineering notes and symbols

Hand-named function map, review inputs and tools for **Killzone**, PlayStation 2 main program `SCUS_974.02`
(MIPS R5900 "Emotion Engine", ee-gcc). Round 1 (one naming pass over every function):

- 16,608 functions found by Ghidra 12.1.4 (loaded as generic MIPS64: R5900 MMI / VU0 macro instructions decode badly and are noted, not chased);
- 16,544 hand-named, 0 placeholders left, 4,798 still marked `provisional` (a second review round with callers is running and will be pushed as round 2).

Game: first-person shooter; levels streamed from FILES.DAT packs; four relocatable overlays (BLGFX, NETWORK, ONLINE, DNASMC .REL, not yet covered); Logitech USB keyboard/mouse/headset drivers on the IOP.

Same method as [pandemonium-decomp](https://github.com/indieindie7/pandemonium-decomp) and
[ducatiworld-decomp](https://github.com/indieindie7/ducatiworld-decomp): a hinted, trimmed decompile is cut into slices,
each slice is named from its code and strings (prompt in `ghidra/naming/prompt_r1.txt`), names are deduplicated
across slices and applied as USER_DEFINED labels, then every provisional name is re-read with up to three callers
(prompt in `ghidra/review/`). Non-commercial, done for study and preservation.

**No game data is included**: no disc image, no ELF, no overlays, no unpacked data, no decompiled C,
no game text, no Ghidra database. You need your own copy of the game to use any of this.

## What is here

| Path | Content |
|---|---|
| `NOTES.md` | ELF layout, Ghidra setup, the naming round, what comes next |
| `ghidra/hand_SCUS.txt` | hand names: `0x<addr> func <name> hand <comment>` (apply with ApplyNames.java from the Scorcher / AMOK repos, hand mode) |
| `ghidra/funcinfo_SCUS.tsv` | per-function export: `F` address name source size, `C` callees (string rows removed) |
| `ghidra/naming/prompt_r1.txt`, `ghidra/review/` | the round-1 naming prompt and the provisional-review prompt |
| `ghidra/scripts/` | `CsDumpAll.java` (decompile dump with headers), `SeedMipsBlocks.java` |
| `tools/` | `elfinfo.py`, `fihints.py` + `injecthints.py` (size/callee/string hints into the dump), `trimdump.py`, `slice.py`, `dedupnames.py`, `provctx.py` (review contexts with callers), `srprovapply.py` (apply review verdicts), `pubfuncinfo.py` |

## Licence

Notes, names and tools: MIT (see `LICENSE`). Killzone belongs to its rights holders; nothing from the
game is distributed here.
