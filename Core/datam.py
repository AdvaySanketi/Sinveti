def reset(prev, user, passwd):
    import pickle as p
    f = open('entries.dat','rb+')
    record = {}
    try:
        while True:
            pos = f.tell()
            record = p.load(f)
            if record['user'] == prev:
                record['user'] = user
                record['password'] = passwd
                f.seek(pos)
                p.dump(record, f)
    except EOFError:
        f.close()

def delete(user):
    import pickle as p
    lst = []
    with open('entries.dat', 'rb') as file:
        try:
            while True:
                content = p.load(file)
                lst.append(content)
        except:
            file.close()
    with open('entries.dat', 'ab') as file:
        found = False
        for content in lst:
            if content['user'] != user:
                continue
            else:
                found = True
                break
        if found == False:
            text = " not found"
        else:
            with open('entries.dat', 'wb') as f:
                for line in lst:
                    if line['user'] != user:
                        p.dump(line, f)
                    else:
                        text  = " deleted successfully"
            file.close()
    return text
