import sys

def get_ids(text):
    
    ids = list()
    
    lines = text.split('\n')
    
    for line in lines:

        if "We did not" in line or\
                'Missing File' in line:
            continue

        id_info = line.split()

        if len(id_info) > 0 and id_info[0] == 'Store:':
            if len(id_info) > 1:
                ids.append(id_info[1])
    str = ''
    for id in ids:
        str += '\'{0}\', '.format(id)

    return(len(ids), str[:-2])
        
