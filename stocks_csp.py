import csv
from cspbase import *
from propagators import *
'''
Construct and return Mutual Funds CSP model.
'''

# take in user input, that specifies the constraints they want
# generate satisfying tuples based on said constraints
# csp_data {'TICKER': {'price': int, 'price_open': float, 'price_close': float},
#  'max_spending_limit': int, 'max_stock_price', int, 'min_stock_price': int, 'green_stocks': set(), 'tech_stocks', set()}
def generate_vars(n):
    tickers = []
    reader = csv.DictReader(open(fname))

    for row in reader:
        tickers.append(row['TICKER'])
    #print("tickers: ", tickers)
    for i in range(n):
        var = Variable("stock_"+str(i), tickers)
        vars_.append(var)
    return vars_

def green_constraint():
    g_cons = []
    for var in vars_:
        con = Constraint("green_constraint", [var])
        print("con scope: ", con.scope)
        sat_tuples = get_satisfying_tickers("GREEN","True")
        print("sat_tuples: ", sat_tuples)
        con.add_satisfying_tuples(sat_tuples)
        g_cons.append(con)
    return g_cons

def max_spending_limit_constraint():
    con = Constraint("max_spending_limit", vars_)
    max_ = user_dict['max_spending_limit']
    con.add_satisfying_tuples(((max_,),)) # this checked by a formula
    return con

def max_stock_price_constraint():
    con = Constraint("max_stock_price_constraint", vars_)
    reader = csv.DictReader(fname)
    max_ = user_dict['max_stock_price']
    for row in reader:
        if row["CLOSE"] < max_:
            con.add_satisfying_tuples(row['TICKER'])
    return con

def min_stock_price_constraint():
    con = Constraint("min_stock_price_constraint", vars_)
    reader = csv.DictReader(fname)
    min_ = user_dict['min_stock_price']
    for row in reader:
        if row["CLOSE"] > min_:
            con.add_satisfying_tuples(row['TICKER'])
    return con

def add_industry_constraints():
    reader = csv.DictReader(fname)
    con = Constraint("industry", vars_)
    desired_industry = user_dict['industry']
    for row in reader:
        if row["industry"] == desired_industry:
            con.add_satisfying_tuples(row['TICKER'])
    return con

# more contraints here


def mutual_funds_csp_model(user_dict):
  '''Returns a CSP object representing a Stocks CSP problem along with an array
  of variables for the problem.
  '''
  volume = user_dict['volume_to_buy']
  generate_vars(volume)
  stocks_csp = CSP('StocksCSP', vars_)
  g_cons = green_constraint()
  [stocks_csp.add_constraint(c) for c in g_cons]
  # actual csp model here
  return stocks_csp, [vars_]


def print_kenken_soln(var_array):
    for row in var_array:
        print([var.get_assigned_value() for var in row])

def get_satisfying_tickers(field ,acceptable_value):
    sat_tuples = []
    with open(fname) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print(row)
            # print(row['TICKER'], acceptable_value)
            if (row[field] == acceptable_value):
                sat_tuples.append((row['TICKER'],))
    return sat_tuples

if __name__ == '__main__':
    user_dict = {'volume_to_buy': 200, 'green': 1, 'industry': 'Technology',
    'spending_limit': 10000, 'min_stock_price': 25, 'max_stock_price': 500}
    fname = "output.csv" #input("Enter your stocks data file: ")
    vars_ = []

    csp, var_array = mutual_funds_csp_model(user_dict)
    solver = BT(csp)
    solver.TRACE = True
    solver.bt_search(prop_GAC)
    print("Solution")
    print_kenken_soln(var_array)
