'''
mutant.py

Copyright 2006 Andres Riancho

This file is part of w3af, w3af.sourceforge.net .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

'''

from core.controllers.w3afException import w3afException
import copy

class mutant:
    '''
    This class is a wrapper for fuzzable requests that have been modified.
    '''
    def __init__( self, freq ):
        self._freq = freq
        self._fuzzableType = None
        self._var = ''
        self._originalValue = ''
        self._originalResponseBody = None
    
    #
    # this methods are from the mutant
    #
    def getFuzzableReq( self ): return self._freq
    def setFuzzableReq( self, freq ): self._freq = freq

    def setVar( self, var): 
        '''
        Set the name of the variable that this mutant modifies.
        '''
        self._var = var
        
    def getVar( self ): return self._var

    def setOriginalValue( self , v ):
        self._originalValue = v
        
    def getOriginalValue( self ):
        return self._originalValue
    
    def setModValue( self, val ):
        '''
        Set the value of the variable that this mutant modifies.
        '''
        try:
            self._freq._dc[ self.getVar() ] = val
        except:
            raise w3afException('The mutant object was\'nt correctly initialized.')
        
    def getModValue( self ): 
        try:
            return self._freq._dc[ self.getVar() ]
        except:
            raise w3afException('The mutant object was\'nt correctly initialized.')
    
    def getMutantType( self ):
        raise w3afException('You should implement the getMutantType method when inhereting from mutant.')
    
    def printModValue( self ):
        return 'The sent '+ self.getMutantType() +' is: "' + self.getData() + '" .'
    
    def __repr__( self ):
        return '<'+ self.getMutantType() +' mutant | '+ self.getMethod() +' | '+ self.getURI() +' >'
    
    def dynamicURL( self ):
        '''
        @return: True if the URL is going to change from one mutant to another (when both mutants were created
        in the same call to the createMutants call.) This was added mostly because of mutantFileName.py
        '''
        return False
    
    def copy( self ):
        newMut = copy.deepcopy( self )
        return newMut
    
    def getOriginalResponseBody( self ):
        '''
        The fuzzable request is a representation of a request; the original response body is the
        body of the response that is generated when w3af requests the fuzzable request for
        the first time.
        '''
        if self._originalResponseBody == None:
            raise w3afException('[mutant error] You should set the original response body before getting its value!')
        else:
            return self._originalResponseBody
    
    def setOriginalResponseBody( self, orBody ):
        self._originalResponseBody = orBody
        
    #
    # All the other methods are forwarded to the fuzzable request
    #
    def __getattr__( self, name ):
        return getattr( self._freq, name )
        
    def foundAt(self):
        '''
        @return: A string representing WHAT was fuzzed. This string is used like this:
                - v.setDesc( 'SQL injection in a '+ v['db'] +' was found at: ' + mutant.foundAt() )
        '''
        res = ''
        res += '"' + self.getURL() + '", using HTTP method '
        res += self.getMethod() + '. The sent data was: "'
        
        # Depending on the data container, print different things:
        dc_length = 0
        for i in self._freq._dc:
            dc_length += len(i) + len(self._freq._dc[i])
        if dc_length > 65:
            res += '...' + self.getVar()  + '=' + self.getModValue() + '...'
            res += '"'
        else:
            res += str(self.getDc())
            res += '".'
            if len(self.getDc()) > 1:
                res +=' The modified parameter was "' + self.getVar() +'".'
        
        return res
