// SeedMipsBlocks: seed function entries in every memory block of a raw MIPS image (N64 segments, PSX RAM):
// every jal target inside the block plus every 'addiu/daddiu sp,sp,-N' prologue. Run as -postScript then analyse.
//@category Analysis
import java.util.*;
import ghidra.app.cmd.disassemble.DisassembleCommand;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.*;
import ghidra.program.model.mem.*;

public class SeedMipsBlocks extends GhidraScript {
	@Override
	protected void run() throws Exception {
		Memory m = currentProgram.getMemory();
		TreeSet<Long> seeds = new TreeSet<>();
		int jal = 0, pro = 0;
		for (MemoryBlock blk : m.getBlocks()) {
			long lo = blk.getStart().getOffset(), size = blk.getSize();
			for (long o = 0; o + 4 <= size; o += 4) {
				int w = m.getInt(blk.getStart().add(o));
				if ((w >>> 26) == 3) {
					long t = (lo & 0xf0000000L) | ((w & 0x03ffffffL) << 2);
					if (t >= lo && t < lo + size) { seeds.add(t); jal++; }
				}
				if ((w & 0xffff8000) == 0x27bd8000 || (w & 0xffff8000) == 0x67bd8000) { seeds.add(lo + o); pro++; }
			}
		}
		TreeSet<Long> keep = new TreeSet<>();
		for (long s : seeds) {
			Long last = keep.isEmpty() ? null : keep.last();
			if (last != null && s - last <= 8 && (m.getInt(toAddr(s)) & 0xbfff8000) == 0x27bd8000) continue;
			keep.add(s);
		}
		int made = 0;
		for (long s : keep) {
			if (monitor.isCancelled()) break;
			Address a = toAddr(s);
			if (getFunctionAt(a) != null) continue;
			new DisassembleCommand(a, null, true).applyTo(currentProgram, monitor);
			if (createFunction(a, null) != null) made++;
		}
		println("SeedMipsBlocks: jal refs " + jal + ", prologues " + pro + ", seeds " + keep.size() + ", functions " + made);
	}
}
