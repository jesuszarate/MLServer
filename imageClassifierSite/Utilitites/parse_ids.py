import sys


# We did not receive the RidleysMovement file for ridleys_1171 on 2018-06-04
# Missing File: RidleysMovement
# Store: ridleys_1171
def get_ids(text):
    # if len(sys.argv) > 1:
    #     pass
    # else:
    ids = list()
    # with open('ids.txt', 'r') as file:
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
        str += '{0}, '.format(id)

    return(str[:-2])
        
