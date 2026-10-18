# elfinfo.py <file.elf> : print ELF32 header, program headers and section headers (little-endian MIPS/PS2).
import struct, sys
d = open(sys.argv[1], 'rb').read()
assert d[:4] == b'\x7fELF', 'not ELF'
ei_class, ei_data = d[4], d[5]
e = '<' if ei_data == 1 else '>'
(e_type, e_machine, e_version, e_entry, e_phoff, e_shoff, e_flags, e_ehsize, e_phentsize, e_phnum,
 e_shentsize, e_shnum, e_shstrndx) = struct.unpack(e + 'HHIIIIIHHHHHH', d[16:52])
print('class %d data %d type %d machine %d entry 0x%08x flags 0x%x ph %d sh %d size %d' %
      (ei_class, ei_data, e_type, e_machine, e_entry, e_flags, e_phnum, e_shnum, len(d)))
for i in range(e_phnum):
    o = e_phoff + i * e_phentsize
    p_type, p_off, p_vaddr, p_paddr, p_filesz, p_memsz, p_flags, p_align = struct.unpack(e + '8I', d[o:o + 32])
    print('PH%d type %d off 0x%x vaddr 0x%08x filesz 0x%x memsz 0x%x flags %d' %
          (i, p_type, p_off, p_vaddr, p_filesz, p_memsz, p_flags))
names = b''
if e_shnum and e_shstrndx < e_shnum:
    o = e_shoff + e_shstrndx * e_shentsize
    sh = struct.unpack(e + '10I', d[o:o + 40])
    names = d[sh[4]:sh[4] + sh[5]]
for i in range(e_shnum):
    o = e_shoff + i * e_shentsize
    sh_name, sh_type, sh_flags, sh_addr, sh_off, sh_size, sh_link, sh_info, sh_align, sh_entsize = struct.unpack(e + '10I', d[o:o + 40])
    nm = names[sh_name:names.find(b'\0', sh_name)].decode('latin1') if names else '?'
    print('SH%-2d %-16s type %-2d addr 0x%08x off 0x%x size 0x%x' % (i, nm, sh_type, sh_addr, sh_off, sh_size))
