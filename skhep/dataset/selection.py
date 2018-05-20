# Licensed under a 3-clause BSD style license, see LICENSE.
"""
***********************
Module for Selection
***********************
"""

# -----------------------------------------------------------------------------
# Import statements
# -----------------------------------------------------------------------------
from ..utils.py23 import *
from ..utils.dependencies import softimport


numpy = softimport("numpy")
pyparsing = softimport("pyparsing")

# -----------------------------------------------------------------------------
# Selection class
# -----------------------------------------------------------------------------
class Selection(object):
    """
    Class for dataset selections.
    """
    
    def __init__(self, selection=""):
        
        selection = selection.replace( "&&", "&")
        selection = selection.replace( "||", "|")
        self._selection = selection
      
    @property  
    def parsed(self):
        """
        Return the parsed selection
        """
        
        Optional           = pyparsing.Optional
        Suppress           = pyparsing.Suppress
        Literal            = pyparsing.Literal
        Word               = pyparsing.Word
        nums               = pyparsing.nums
        alphas             = pyparsing.alphas 
        oneOf              = pyparsing.oneOf
        OneOrMore          = pyparsing.OneOrMore
        Group              = pyparsing.Group
        opAssoc            = pyparsing.opAssoc
        operatorPrecedence = pyparsing.operatorPrecedence

        openpar    = Literal("(")
        closepar   = Literal(")")
        comma      = Literal(",")
        expop      = Literal('^')
        signop     = Literal('-')
        multop     = oneOf('* /')
        plusop     = oneOf('+ -')
        
        number     = Word(nums+".")
        variable   = Word(alphas+nums+"."+"-"+"_")
        operations = operatorPrecedence( number | variable , [("^", 2, opAssoc.RIGHT), (signop, 1, opAssoc.RIGHT), (multop, 2, opAssoc.LEFT), (plusop, 2, opAssoc.LEFT),])
        min_max    = Group(oneOf("min max") + Suppress(openpar) + Group(OneOrMore( ( operations | variable ) + Suppress(Optional(comma)))) + Suppress(closepar))
        identifier = min_max | operations | number | variable
        
        operator   = oneOf("> < >= <= != ==")
        subexpr = identifier.setResultsName("lhs") + operator.setResultsName("operator") + identifier.setResultsName("rhs")
        
        _and = Literal("&")
        _or = Literal("|")
        
        exp = operatorPrecedence( Group(subexpr), [(_and, 2, opAssoc.LEFT), (_or, 2, opAssoc.LEFT),])
        
        return exp.parseString(self._selection)[0]
        
    def evaluateselection(self, dataset, operators, _min, _max):
        """
        Evaluate the selection for a given dataset, taking operators, min and max functions
        according to the type of the dataset.
        """
                
        def operation(lhs=None , operator=None, rhs=None):
            if lhs is None and operator == "-":
                return -rhs
            else:
                return operators[operator] (lhs, rhs)
                
        def operand(_operand):
            #Return instance of the operand
    
            if len(_operand) == 1:
                _operand = _operand[0]
            elif len(_operand) > 1 and isinstance(_operand, pyparsing.ParseResults):

                #treatment of min/max as operand 
                if any(m in _operand.asList() for m in ["min","max"]):
                    if _operand[0] == "min": func = _min
                    elif _operand[0] == "max": func = _max
                        
                    args = []
                    for a in _operand[1]:
                        args.append(operand(a))
                    return func(*args)
                                            
                #treatment with arithmetical operations as operand
                if any(op in _operand.asList() for op in ["-","+","*","/","^"]):
                    if len(_operand) == 2:
                        return operation(operator=_operand[0], rhs=operand(_operand[1])) 
                    elif len(_operand) > 2:                        
                        return operation(lhs=operand(_operand[0]), operator=_operand[1], rhs=operand(_operand[2:]))                                            
            
            if isinstance(_operand, str):
                     
                if _operand == "True":
                    return True
                elif _operand == "False":
                    return False
                try:
                    float(_operand)
                except ValueError:
                    return dataset[_operand]
                else:
                    return float(_operand)
                    
        def loopselection(parsedsel):
            #loop inside the selection, to take into account all subterms, and evaluate the selection
            #from right to left.    
            
            suboperations = []
            bitwiseoperators = []

            for i,s in enumerate(parsedsel):
                if i % 2 == 0:
                    if "&" in s.asList() or "|" in s.asList():
                        suboperations.append(loopselection(s))
                    else:
                        lhs = operand(s.lhs)
                        rhs = operand(s.rhs)
                        suboperations.append(operation(lhs, s.operator, rhs))
                else:
                    bitwiseoperators.append(s)
                    
            while len(bitwiseoperators) > 0:
                index = bitwiseoperators.index(bitwiseoperators[-1])
                loopedselection = operation( suboperations[index], bitwiseoperators[-1], suboperations[index+1] )
                bitwiseoperators.pop(); suboperations.pop(); suboperations.pop()
                suboperations.append(loopedselection)

            return loopedselection
            
        if "&" in self.parsed.asList() or "|" in self.parsed.asList():
            evaluatedselection = loopselection(self.parsed)
        else:
            s = self.parsed
            lhs = operand(s.lhs)
            rhs = operand(s.rhs)
            evaluatedselection = operation(lhs, s.operator, rhs)
        
        return evaluatedselection

    
    @property    
    def numpyselection(self):
        """
        Return the selection readable for NumpyDataset
        """
        
        operators = {">": numpy.greater, "<": numpy.less, ">=": numpy.greater_equal, "<=": numpy.less_equal,
                     "==": numpy.equal, "!=": numpy.not_equal, "&": numpy.bitwise_and, "|": numpy.bitwise_and,
                     "+": numpy.add, "-": numpy.subtract, "/": numpy.divide, "*": numpy.multiply,
                     "^": numpy.power}
        
        def evaluateufunc(ufunc, *args):
            if len(args) == 2:
                return ufunc(*args)
            else:
                return ufunc.reduce(args)
        
        def _min(*args):
            ufunc = numpy.minimum
            return evaluateufunc(ufunc, *args)
            
        def _max(*args):
            ufunc = numpy.minimum
            return evaluateufunc(ufunc, *args)
            
        def selection(numpydataset):
            # selection as a function of the numpy dataset
            return self.evaluateselection(numpydataset, operators, _min, _max)
            
        return selection
        
    @property    
    def pandasselection(self):
        """
        Return the selection readable for possible PandasDataset
        """
        
        raise NotImplementedError
    
    @property    
    def rootselection(self):
        """
        Return the selection readable for RootDataset
        """
        
        selection = self._selection.replace("&","&&")
        selection = selection.replace("|","||")
        return selection
                                                
    def __repr__(self):
        return self._selection
        
    def __and__(self, other):
        """
        Return new selection = self and other
        """
        
        if not isinstance(other, Selection):
            return NotImplemented
            
        if "|" in self._selection:
            lhs = "(" + self._selection + ")"
        else:
            lhs = self._selection
            
        if "|" in other._selection:
            rhs = "(" + other._selection + ")"
        else:
            rhs = other._selection

        selection = lhs + " & " + rhs

        return Selection(selection)
        
    def __or__(self, other):
        """
        Return new selection = self or other
        """
        
        if not isinstance(other, Selection):
            return NotImplemented
            
        if "&" in self._selection:
            lhs = "(" + self._selection + ")"
        else:
            lhs = self._selection
            
        if "&" in other._selection:
            rhs = "(" + other._selection + ")"
        else:
            rhs = other._selection

        selection = lhs + " | " + rhs

        return Selection(selection)
        
        
        
        
        

                    
            
                        