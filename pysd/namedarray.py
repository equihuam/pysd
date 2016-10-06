class namedarray(object):
    def __init__(self,object):
        self.object=object
        
    def shorthander(self,operation,other_object):
        if len(self.object['shape'])>=len(other_object['shape']):
            result=self.object['array']
            other_numeral=other_object['array']
            dct=other_object['shape'].copy()
            refdct=self.object['shape'].copy()
            copyofref=self.object['shape'].copy()
        else:
            result=other_object['array']
            other_numeral=self.object['array']
            dct=self.object['shape'].copy()
            refdct=other_object['shape'].copy()
            copyofref=other_object['shape'].copy()
            
        difference=abs(len(refdct)-len(dct))
        
        for key,val in dct.iteritems():
            result=np.swapaxes(result,copyofref[key],val+difference)
            copyofref[copyofref.keys()[copyofref.values().index(val+difference)]]=copyofref[key]
            copyofref[key]=val+difference
            
        #Perform Operation Here Before Returning to Normal Shape
        result_vars={'a':result,'b':other_numeral}
        result=eval('a %s b'%operation,result_vars)
        ########################################################
        
        for val in sorted(refdct.itervalues()):
            key=refdct.keys()[refdct.values().index(val)]
            result=np.swapaxes(result,copyofref[key],val)
            copyofref[copyofref.keys()[copyofref.values().index(val)]]=copyofref[key]
            copyofref[key]=val
        return namedarray({'array':result,'shape':refdct})
    
    def __add__(self,other_object):
        return self.shorthander('+',other_object)
    def __sub__(self,other_object):
        return self.shorthander('-',other_object)
    def __mul__(self,other_object):
        return self.shorthander('*',other_object)
    def __div__(self,other_object):
        return self.shorthander('/',other_object)
    
    def __repr__(self):
        return repr(self.object['array'])
    def __getitem__(self,rhs):
        return self.object[rhs]  
    def __setitem__(self,rhs,value):
        if rhs=='array' and len(self.object['shape'])>=len(value['shape']):
            self.object[rhs]*=0
            self.object[rhs]=self.shorthander('+',value)['array']
        elif len(self.object['shape'])<len(value['shape']):
            raise NamedArrayException('Cannot set value of array with subscripts %s to value with subscripts %s'
                                      %(self.object['shape'],value['shape']))
        else:
            raise NamedArrayException('Cannot change array subscripts %s'%self.object['shape'])
class NamedArrayException(Exception):
    pass