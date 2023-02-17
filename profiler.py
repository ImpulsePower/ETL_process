'''profiler'''
def print_result():
    '''Printing results'''
    f_log = open('profile.log', 'r')
    rows = []
    for row in f_log:
        rows.append(row)
    f_log.close()
    i = 4
    print('==================================================================')
    print(rows[i - 1], end='')
    while i + 1 < len(rows):
        if rows[i] and rows[i].strip():
            print(rows[i], end='')
            i += 1
        else:
            break

def go():
    '''Start profiler'''
    from cProfile import run    
    run('main()', 'profile.dmp')
    out_stream = open('profile.log', 'w')
    from pstats import Stats, SortKey
    p = Stats('profile.dmp', stream = out_stream)
    p.strip_dirs()
    p.sort_stats(SortKey.PCALLS)
    p.print_callers('main.py')
    out_stream.close()
    print_result()
