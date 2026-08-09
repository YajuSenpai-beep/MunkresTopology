import os

BACKSLASH = bytes([0x5C])
S_SPACE = BACKSLASH + b'S '
S_BS_SPACE = BACKSLASH + b'S' + BACKSLASH + b' '

total = 0
files = [os.path.join('chapters', f) for f in os.listdir('chapters') if f.startswith('Chapter_')]
files.append('TopologyBook.sty')

for path in files:
    with open(path, 'rb') as f:
        data = f.read()

    count = 0
    result = bytearray()
    i = 0
    while i < len(data):
        # Check for \S + space + digit (3 bytes: 5C 53 20)
        if (i + 4 <= len(data)
            and data[i:i+3] == S_SPACE
            and bytes([data[i+3]]).isdigit()):
            # This is \S N - convert to \S\ N
            # But check it's not already \S\ N or preceded by backslash
            if not (i >= 3 and data[i-3:i+3] == S_BS_SPACE):
                if not (i >= 1 and data[i-1:i] == BACKSLASH):
                    result.extend(S_BS_SPACE)
                    i += 3
                    count += 1
                    continue
        result.append(data[i])
        i += 1

    if count:
        with open(path, 'wb') as f:
            f.write(bytes(result))
        print(f'{os.path.basename(path)}: {count}')

print(f'Total: {total}')
