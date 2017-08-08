import sys

'''
Construct and return Mutual Funds CSP model.
'''

# take in user input, that specifies the constraints they want
# generate satisfying tuples based on said constraints
# csp_data {'Ticker': {'price': int, 'price_open': float, 'price_close': float},
#  'max_spending_limit': int, 'max_stock_price', int, 'min_stock_price': int, 'green_stocks': set(), 'tech_stocks', set()}
user_dict = {}
vars_ = []
def generate_vars(n = user_dict['requested_volume']):
    vars_ = []
    for i in range(n):
        var = Variable("stock_"+str(i), csp_data.keys())
        vars_.append(var)
    return vars_

def green_constraint(requested_green = user_dict['requested_green']):
    con = Constraint("green_constraint", vars_)
    con.add_satisfying_tuples(csp_data['green_stocks'])
    return con

def max_spending_limit_constraint():
    con = Constraint("max_spending_limit", vars_)
    con.add_satisfying_tuples(user_dict['max_spending_limit']) # this checked by a formula
    return con

def max_stock_price_constraint():
    con = Constraint("max_stock_price_constraint", vars_)
    con.add_satisfying_tuples(user_dict['max_stock_price']) # this checked by a formula
    return con

def min_stock_price_constraint():
    con = Constraint("min_stock_price_constraint", vars_)
    con.add_satisfying_tuples(user_dict['min_stock_price']) # this checked by a formula
    return con




# more contraints here


def mutual_funds_csp_model(csp_data, user_dict):
  '''Returns a CSP object representing a Stocks CSP problem along with an array
  of variables for the problem.
  '''
  volume = user_dict['volume_to_buy']
  stocks_csp = CSP('StocksCSP', vars_)
  constraints = [min_stock_price_constrain(), max_stock_price_constrain(), max_spending_limit_constrain(), green_constrain()]
  [stocks_csp.add_constraint(c) for c in constraints]
  # actual csp model here
  return stocks_csp, vars_
