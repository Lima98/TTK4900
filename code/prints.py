tl = '╭'
tr = '╗'
bl = '╚'
br = '╝'
h = '─'
v = '│'


print(tl + 'Table'.center(48, '═'	) + tr)
print(v , 'First'.center(10),  end='')
print(v , 'Second'.center(10), end='')
print(v , 'Third'.center(10), end='')
print(v , 'Fourth' .center(10), v)
print(v + ''.ljust(11, '─') + '╫' + ''.ljust(11, '─') + '╫' + ''.ljust(11, '─') + '╫' + ''.ljust(12, '─') + '╢')

print(v , '1'.center(10),  end='')
print(v , '2'.center(10), end='')
print(v , '4'.center(10), end='')
print(v , '7' .center(10), v)
print(v , '1'.center(10),  end='')
print(v , '2'.center(10), end='')
print(v , '4'.center(10), end='')
print(v , '7' .center(10), v)
print(v , '1'.center(10),  end='')
print(v , '2'.center(10), end='')
print(v , '4'.center(10), end='')
print(v , '7' .center(10), v)

print(bl + ''.ljust(11, h) + '╩' + ''.ljust(11, h) + '╩' + ''.ljust(11, h) + '╩' + ''.ljust(12, h) + '╝')

