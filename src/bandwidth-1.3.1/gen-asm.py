from random import shuffle

print 'bits 64'
print 'cpu ia64'
print 'global CacheMisses'
print 'global _CacheMisses'

print '; Note:'
print '; Unix ABI says integer param are put in these registers in this order:'
print '; rdi, rsi, rdx, rcx, r8, r9'
print '        section .text'


print ';------------------------------------------------------------------------------'
print '; Name:         CacheMisses'
print '; Purpose:      Generates cache misses (adapted from Reader)'
print '; Params:       rdi = ptr to memory area'
print ';------------------------------------------------------------------------------'
print '        align 64'
print 'CacheMisses:'
print '_CacheMisses:'
print '        mov    rax, [rdi]'

x = [i for i in range(1000000)]
shuffle(x)
for i in x:
  print '        mov    rax, [' + str(i*64) + '+rdi]'

print '      ret'
