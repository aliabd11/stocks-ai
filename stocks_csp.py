import csv
from cspbase import *
from propagators import *
import _thread
import time
'''
Construct and return Mutual Funds CSP model.
'''

# take in user input, that specifies the constraints they want
# generate satisfying tuples based on said constraints
# csp_data {'TICKER': {'price': int, 'price_open': float, 'price_close': float},
#  'max_spending_limit': int, 'max_stock_price', int, 'min_stock_price': int, 'green_stocks': set(), 'tech_stocks', set()}

def get_all_tickers():
    tickers = []
    reader = csv.DictReader(open(fname))

    for row in reader:
        tickers.append(row['TICKER'])
    return tickers

def generate_vars(n):
    tickers = get_all_tickers()
    # print("tickers: ", tickers)
    for i in range(n):
        var = Variable("stock_"+str(i), tickers)
        vars_.append(var)
    return vars_

# Spending Constraints

def max_spending_limit_constraint():
    spend_limit = user_dict['max_spending_limit']

    cons = []
    tickers = get_all_tickers()
    sat_tuples = []
    for x in range(len(tickers)):
        for y in range(x+1, len(tickers)):
            # INCOMPLETE
            if (tickers[x] < int(spend_limit) or tickers[y] < int(spend_limit)):
                sat_tuples.append((tickers[x], tickers[y]),)
    for i in range(len(vars_)):
        for j in range(i+1, len(vars_)):
            var1 = vars_[i]
            var2 = vars_[j]
            name = "alldiff"
            scope = [var1, var2]
            con = Constraint(name, scope)
            cons.append(con)
    return cons

    # con = Constraint("max_spending_limit", vars_)
    # max_ = user_dict['max_spending_limit']
    # con.add_satisfying_tuples(((max_,),)) # this checked by a formula
    # return con

def max_stock_price_constraint():
    # con = Constraint("max_stock_price_constraint", vars_)
    # reader = csv.DictReader(fname)
    # max_ = user_dict['max_stock_price']
    # for row in reader:
    #     if row["CLOSE"] < max_:
    #         con.add_satisfying_tuples(row['TICKER'])
    # return con

    max_price = user_dict['max_stock_price_constraint']

    cons = []
    tickers = get_all_tickers()
    sat_tuples = []
    for x in range(len(tickers)):
        for y in range(x+1, len(tickers)):
            # INCOMPLETE
            if (tickers[x] < int(spend_limit) or tickers[y] < int(spend_limit)):
                sat_tuples.append((tickers[x], tickers[y]),)
    for i in range(len(vars_)):
        for j in range(i+1, len(vars_)):
            var1 = vars_[i]
            var2 = vars_[j]
            name = "alldiff"
            scope = [var1, var2]
            con = Constraint(name, scope)
            cons.append(con)
    return cons


def min_stock_price_constraint():
    # con = Constraint("min_stock_price_constraint", vars_)
    # reader = csv.DictReader(fname)
    # min_ = user_dict['min_stock_price']
    # for row in reader:
    #     if row["CLOSE"] > min_:
    #         con.add_satisfying_tuples(row['TICKER'])
    # return con

    min_price = user_dict['min_stock_price_constraint']

    cons = []
    tickers = get_all_tickers()
    sat_tuples = []
    for x in range(len(tickers)):
        for y in range(x+1, len(tickers)):
            # INCOMPLETE
            if (tickers[x] < int(spend_limit) or tickers[y] < int(spend_limit)):
                sat_tuples.append((tickers[x], tickers[y]),)
    for i in range(len(vars_)):
        for j in range(i+1, len(vars_)):
            var1 = vars_[i]
            var2 = vars_[j]
            name = "alldiff"
            scope = [var1, var2]
            con = Constraint(name, scope)
            cons.append(con)
    return cons

# Green constraints, industry constraints, region constraints

def green_constraint():
    g_cons = []
    for var in vars_:
        con = Constraint("green_constraint", [var])
        #print("con scope: ", con.scope)

        if(int(user_dict['green'])):
            sat_tuples = get_satisfying_tickers("GREEN", "True")
        else:
            sat_tuples = get_satisfying_tickers("GREEN", "False")
        #print("sat_tuples: ", sat_tuples)
        con.add_satisfying_tuples(sat_tuples)
        g_cons.append(con)
    return g_cons

def industry_constraint(desired_industry):
    industry_constraints = []
    for var in vars_:
        con = Constraint("industry_constraint", [var])
        sat_tuples = get_satisfying_tickers("INDUSTRY", desired_industry)

        con.add_satisfying_tuples(sat_tuples)
        industry_constraints.append(con)
    return industry_constraints

def region_constraint(region):
    region_constraints = []
    for var in vars_:
        con = Constraint("industry_constraint", [var])
        sat_tuples = get_satisfying_tickers("REGION", region)

        con.add_satisfying_tuples(sat_tuples)
        region_constraints.append(con)
    return region_constraints

# Generate the actual mutual funds model

def mutual_funds_csp_model(user_dict):
  '''Returns a CSP object representing a Stocks CSP problem along with an array
  of variables for the problem.
  '''
  volume = user_dict['volume_to_buy']
  generate_vars(int(volume))
  stocks_csp = CSP('StocksCSP', vars_)

  g_cons = green_constraint()
  industry_cons = industry_constraint(user_dict['industry'])
  region_cons = region_constraint(user_dict['region'])
  all_diff_cons = get_all_diff_constraints()
  #min_stock_price_cons = min_stock_price_constraint()
  #max_stock_price_cons = max_stock_price_constraint()
  #spending_cons =  max_spending_limit_constraint()

  [stocks_csp.add_constraint(c) for c in g_cons]
  [stocks_csp.add_constraint(c) for c in industry_cons]
  [stocks_csp.add_constraint(c) for c in region_cons]
  [stocks_csp.add_constraint(c) for c in all_diff_cons]
  #[stocks_csp.add_constraint(c) for c in spending_cons]
  #[stocks_csp.add_constraint(c) for c in spending_cons]
  #[stocks_csp.add_constraint(c) for c in spending_cons]

  return stocks_csp, [vars_]

def print_kenken_soln(var_array):
    for row in var_array:
        print([var.get_assigned_value() for var in row])

def get_satisfying_tickers(field, acceptable_value, calculated = {}):
    if (field, acceptable_value) not in calculated:
        sat_tuples = []
        with open(fname) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if (row[field] == acceptable_value):
                    sat_tuples.append((row['TICKER'],))
        calculated[(field, acceptable_value)] = sat_tuples
    return calculated[(field, acceptable_value)]

#n-ary constraint

def get_all_diff_constraints():
    cons = []
    tickers = get_all_tickers()
    sat_tuples = []
    for x in range(len(tickers)):
        for y in range(x+1, len(tickers)):
            sat_tuples.append((tickers[x], tickers[y]),)
    for i in range(len(vars_)):
        for j in range(i+1, len(vars_)):
            var1 = vars_[i]
            var2 = vars_[j]
            name = "alldiff"
            scope = [var1, var2]
            con = Constraint(name, scope)
            cons.append(con)
    return cons


def print_time(delay):
    count = 0
    start = time.time()
    while not main_thread_not_done:
        time.sleep(delay)
        current = time.time()
        print("Working on solution, Time Elapsed: %d" % int(current - start) )
    new_thread_ended = True


if __name__ == '__main__':
    input_file = csv.DictReader(open("user_data.csv"))

    user_data = []
    for row in input_file:
        user_data.append(row)

    for user in user_data:
        print("Finding portfolio for User: {0}".format(user['name']))
        user_dict = user

        #user_dict = {'volume_to_buy': 30, 'green': 0, 'industry': 'Technology',
        #'spending_limit': 1, 'min_stock_price': 25, 'max_stock_price': 500,'region': 'Canada'}

        fname = "output.csv" #input("Enter your stocks data file: ")
        vars_ = []
        main_thread_not_done = False
        _thread.start_new_thread( print_time, (5,) )
        csp, var_array = mutual_funds_csp_model(user_dict)
        solver = BT(csp)
        solver.bt_search(prop_BT)
        main_thread_not_done = True
        new_thread_ended = False
        if new_thread_ended:
            print("Solution")
            print_kenken_soln(var_array)
