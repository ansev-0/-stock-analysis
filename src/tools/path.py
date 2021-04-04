import sys, re
def get_financial_path():
    for path in sys.path:
        if 'financialworks' in path:
            return re.match("(.*?)financialworks", path)[0]
    return None
