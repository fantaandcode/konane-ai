def clean_move(move):
    a = str(move)[6:-3]
    index = a.find(':')
    start = a[:index][1:-1]
    end = a[index + 1:][1:-1]

    index = start.find(',')
    start = (int(start[:index]), int(start[index + 1:]))

    index = end.find(',')
    end = (int(end[:index]), int(end[index + 1:]))

    return (start, end)

def parse_move(move):
    return bytes('Move['+str(move[0][0])+','+str(move[0][1])+']:['+str(move[1][0])+','+str(move[1][1])+']\n', 'utf8')

mv = b'Move[17,17]:[17,17]\n'
print(clean_move(mv))
print(parse_move(clean_move(mv)))
print(mv==parse_move(clean_move(mv)))