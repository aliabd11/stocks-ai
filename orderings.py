import random

'''
This file will contain the MRV variable ordering heuristic to be used within
bt_search.

var_ordering == a function with the following template
    ord_type(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    ord_type returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
'''


def ord_mrv(csp):
    '''
    ord_mrv(csp):
    A var_ordering function that takes CSP object csp and returns Variable object var,
    according to the Minimum Remaining Values (MRV) heuristic as covered in lecture.
    MRV returns the variable with the most constrained current domain
    (i.e., the variable with the fewest legal values).
    '''
    md = -1
    mv = None
    for v in csp.get_all_unasgn_vars():
        if md < 0:
            md = v.cur_domain_size()
            mv = v
        elif v.cur_domain_size() < md:
            md = v.cur_domain_size()
            mv = v
    return mv


