# Killzone (PS2, Guerrilla 2004) decomp notes (names + notes only; no game data)

## Disc and ELF (2026-10-18)
- NTSC US disc (SCUS-97402), 4,624,285,696 bytes. SYSTEM.CNF: BOOT2 = cdrom0:\SCUS_974.02;1, VER 1.00.
- SCUS_974.02 (4,311,692 B): ELF32 LE MIPS, entry 0x00146f30, one PT_LOAD vaddr 0x00140000 filesz 0x41a674 memsz 0x4513f8. Sections: .text 0x00140000 size 0x3d3340 (file offset 0x1000), .data 0x00513380 (0x295d0), .rodata 0x0053c980 (0x1c5e0), .sdata 0x00558f80, .sbss 0x0055a680, .bss 0x0055b500 (0x35ef8), .data.spad_used 0x70003a00 (scratchpad), two .DVP.overlay VU sections.
- LOADER.ELF: entry 0x00100be8, .text 0x00100000 size 0x6ded8 (boot loader). MODULES: BLGFX.REL 346 KB, DNASMC.REL 657 KB, NETWORK.REL 1.28 MB, ONLINE.REL 5.8 MB (relocatable overlays, later). IOP: standard Sony IRX + LGAUD / LGKBM (Logitech) + P*_R.IRX (Guerrilla IOP drivers: file, input, sound). FILES.DAT..FILES04.DAT = asset packs (4.6 GB).
- `tools/elfinfo.py <elf>` prints the headers and sections.

## Ghidra (12.1.4)
- Imported with the ElfLoader as MIPS:LE:64:default (no R5900 variant): 378 analysis WARN/ERROR lines, mostly "Pcode error ... does not contain referenced instruction" = EE MMI / VU0 macro ops; expected, left alone. Such functions are named as vector math / DMA packet builders from context.
- 16,608 functions after analysis; ExportFuncInfo gives the funcinfo table (F / C / S rows; S rows are not published).

## Naming round 1 (2026-10-18)
- CsDumpAll decompile dump (16,548 functions, 15.3 MB) -> `fihints.py` + `injecthints.py` (size, callee count, strings as a hint line per function) -> `trimdump.py` (bodies cut to 45 head + 8 tail lines) -> `slice.py 32` (411-653 functions per slice).
- One naming agent per slice with `ghidra/naming/prompt_r1.txt`. Rule at the end of the prompt: every function is named by reading its code, never by a script or by shape. Per-slice check: line count equals the function count of the slice and every line matches `0x<8 hex> func <name> hand <comment>`.
- `dedupnames.py` made names unique across slices (98 cross-slice duplicates got _2.. suffixes) and confirmed every FUN_ address is covered (0 missing, no gap pass needed).
- ApplyNames (hand mode, USER_DEFINED): 16,544 named; export `ghidra/funcinfo_SCUS.tsv`: 16,608 functions, 0 FUN_, 4,798 provisional.

## Next
- Round 2: every provisional name re-read with its callers (`tools/provctx.py` builds the contexts, prompt `ghidra/review/prompt_r1_kz.txt`, verdict lines `<PROG> 0x<addr> <old> CONFIRM|RENAME|UNSURE <new> <reason>`, applied with `tools/srprovapply.py`), then re-apply and re-export.
- The four .REL overlays (BLGFX, NETWORK, ONLINE, DNASMC) and LOADER.ELF.
