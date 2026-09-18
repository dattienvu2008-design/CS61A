class Pair:
    """A pair has two instance attributes: first and rest. rest must be a Pair or nil

    >>> s = Pair(1, Pair(2, nil))
    >>> s
    Pair(1, Pair(2, nil))
    >>> print(s)
    (1 2)
    >>> print(s.map(lambda x: x+4))
    (5 6)
    """
    def __init__(self, first, rest):
        self.first = first
        self.rest = rest

    def __repr__(self):
        return 'Pair({0}, {1})'.format(repr(self.first), repr(self.rest))

    def __str__(self):
        s = '(' + repl_str(self.first)
        rest = self.rest
        while isinstance(rest, Pair):
            s += ' ' + repl_str(rest.first)
            rest = rest.rest
        if rest is not nil:
            s += ' . ' + repl_str(rest)
        return s + ')'

    def __len__(self):
        n, rest = 1, self.rest
        while isinstance(rest, Pair):
            n += 1
            rest = rest.rest
        if rest is not nil:
            raise TypeError('length attempted on improper list')
        return n

    def __eq__(self, p):
        if not isinstance(p, Pair):
            return False
        return self.first == p.first and self.rest == p.rest

    def map(self, fn):
        """Return a Scheme list after mapping Python function FN to SELF."""
        mapped = fn(self.first)
        if self.rest is nil or isinstance(self.rest, Pair):
            return Pair(mapped, self.rest.map(fn))
        else:
            raise TypeError('ill-formed list (cdr is a promise)')
    
    def exclude_tail_map(self, fn):
        mapped = fn(self.first)
        if self.rest.rest is nil or isinstance(self.rest, Pair):
            return Pair(mapped, self.rest.map(fn))
        else:
            raise TypeError('ill-formed list (cdr is a promise)')

    def flatmap(self, fn):
        """Return a Scheme list after flatmapping Python function FN to SELF."""
        from scheme_builtins import scheme_append
        mapped = fn(self.first)
        if self.rest is nil or isinstance(self.rest, Pair):
            return scheme_append(mapped, self.rest.flatmap(fn))
        else:
            raise TypeError('ill-formed list (cdr is a promise)')

def to_list(pair):
    """
    Create a deepcopy version of pair in Python list data type
    (self-defined function)
    Parameters
    ----------
    pair : Pair object
    Returns
    -------
    final_lst: list
    
    >>> pair = Pair(1, Pair(Pair(2, nil), Pair(3, nil)))
    >>> str(pair)
    (1 (2) 3)
    >>> to_list(pair)
    [1, [2], 3]
    """
    a = pair
    final_lst = []
    if pair is nil:
        return []
    while not a is nil:
        if not isinstance(a.first, Pair):
            final_lst.append(a.first)
        else:
            final_lst.append(to_list(a.first))
        a = a.rest
    return final_lst

def shallow_copy(pair):
    """
    Create a copy version of pair in Python list data type
    (self-defined function)
    Parameters
    ----------
    pair : TYPE
        DESCRIPTION.

    Returns
    -------
    None.
    >>> pair = Pair(1, Pair(Pair(2, nil), Pair(3, nil)))
    >>> str(pair)
    (1 (2) 3)
    >>> shallow_copy(pair)
    [1, Pair(2, nil), 3]
    """
    if pair is nil:
        return []
    if isinstance(pair.rest, Pair):
        return [pair.first] + shallow_copy(pair.rest)
    return [pair.first]

def pair_iter(pair):
    """
    Return an iterator from a Scheme list
    (self-defined function)
    Parameters
    ----------
    pair : Scheme list
    ------
    """
    if not pair is nil:
        yield pair.first
        if isinstance(pair.rest, Pair):
            iterator = pair_iter(pair.rest)
            yield from iterator
            
# def pairlst_append(lst1, lst2):
#     """
#     Append 2 scheme list. May mutate if lst1/lst2 change (not a deepcopy append version)
#     Parameters
#     ----------
#     lst1 : Pair (scheme list)
#     lst2 : Pair (scheme list)
#     Returns
#     -------
#     lst1 + lst2 (Pair - scheme list) 
#     """
#     if lst1 is nil:
#         return lst2
#     elif lst2 is nil:
#         return lst1
#     if lst1.rest is nil:
#         return Pair(lst1.first, lst2)
#     return Pair(lst1.first, pairlst_append(lst1.rest, lst2))
            
class nil:
    """The empty list"""

    def __repr__(self):
        return 'nil'

    def __str__(self):
        return '()'

    def __len__(self):
        return 0

    def map(self, fn):
        return self

    def flatmap(self, fn):
        return self

nil = nil() # Assignment hides the nil class; there is only one instance

def repl_str(val):
    """Should largely match str(val), except for booleans and undefined."""
    if val is True:
        return "#t"
    if val is False:
        return "#f"
    if val is None:
        return "undefined"
    if isinstance(val, str) and val and val[0] == "\"":
        return "\"" + repr(val[1:-1])[1:-1] + "\""
    return str(val)
# Those are wrong code lol
# def add_list(*args):
#     lists = filter(lambda x: not x is nil, args)
#     return sum(lists, [])
    
# def to_python_list(pair):
#     if pair is nil:
#         return []
#     elif not isinstance(pair, Pair):
#         return pair
#     return add_list([to_python_list(pair.first)], to_python_list(pair.rest))



