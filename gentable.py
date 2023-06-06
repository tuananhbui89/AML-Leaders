from numpy import NaN
import pandas as pd

def avoid_nan(d): 
    if d is NaN: 
        return ''
    else: 
        return d 

def clean(d): 
    d = avoid_nan(d)
    d.rstrip()
    d.rstrip('\n')
    return d 

def main():
    filename = "AML-People-Group.csv"
    data = pd.read_csv(filename)
    output_file = open("table.md", "w")

    KEYS = ['Name', 'Affilation', 'Resources']
    K_N = KEYS[0]
    K_A = KEYS[1]
    K_R = KEYS[2]
    K_L = 'Links'
    K_W = 'Website'

    num_lines = len(data['Resources'])

    redata = dict()

    prev_name = data[K_N][0]
    for i in range(num_lines): 
        if clean(data[K_N][i]) == '':
            data[K_N][i] = prev_name 
        else: 
            prev_name = data[K_N][i]
        if data[K_N][i] in redata: 
            redata[data[K_N][i]][K_R].append(clean(data[K_R][i]))
            redata[data[K_N][i]][K_L].append(clean(data[K_L][i]))
            if clean(data[K_W][i]) != '': 
                redata[data[K_N][i]][K_W] = clean(data[K_W][i])
            if clean(data[K_A][i]) != '': 
                redata[data[K_N][i]][K_A] = clean(data[K_A][i])            
        else: 
            redata[data[K_N][i]] = dict()
            redata[data[K_N][i]][K_N] = clean(data[K_N][i])
            redata[data[K_N][i]][K_A] = clean(data[K_A][i])
            redata[data[K_N][i]][K_W] = clean(data[K_W][i])
            redata[data[K_N][i]][K_R] = [clean(data[K_R][i])]
            redata[data[K_N][i]][K_L] = [clean(data[K_L][i])]
    
    def gen_header(fid):
        entry = '' 
        for i, k in enumerate(KEYS): 
            if i == len(KEYS) - 1: 
                entry += f"|{k} | \n"
            else: 
                entry += f"|{k} "
        fid.write(entry)

        entry = ''
        for i, k in enumerate(KEYS): 
            if i == len(KEYS) - 1:
                entry += f"|{'-'*len(KEYS[i])}| \n"
            else: 
                entry += f"|{'-'*len(KEYS[i])}"
        fid.write(entry)
    
    def gen_one(fid, author): 
        assert(type(author) is dict)
        
        if author[K_W] != '':
            entry = f"|[{clean(author[K_N])}]({author[K_W]}) "
        else: 
            entry = f"|{clean(author[K_N])} "
        fid.write(entry)

        entry = f"|{clean(author[K_A])} "
        fid.write(entry)

        for i, (link, resource) in enumerate(zip(author[K_L], author[K_R])): 

            if link != '': 
                entry = f'[{resource}]({link})'
            else:
                entry = f'{resource}'

            if i == 0:
                entry = "|" + entry

            if i > 0: 
                entry = '<br> ' + entry 

            if i == len(author[K_R]) - 1: 
                entry = entry + '| \n'

            fid.write(entry)

    gen_header(output_file)
    for author in redata.keys(): 
        gen_one(output_file, redata[author])

    output_file.close()

if __name__ == "__main__":
    main()