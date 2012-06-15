#! /usr/bin/python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:         harrisonHarmony.py
# Purpose:      music21-compatible classes for performing and presenting an
#               analysis in the style of Daniel Harrison (1994)
# 
# Copyright (C) 2012 Christopher Antila
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------
'''
Classes and functions for performing and presenting a harmonic-functional
analysis in the style of Daniel Harrison (1994).

The program may be started by itself, or imported as a library.

As per the theory, major and minor keys with the same tonic pitch are treated
as identical.

The following classes are defined:
:class:`~HarmonicFunctionalNote` does blah blah blah
TODO: Finish this list.
'''

## Import required libraries
from music21 import pitch # confirmed requirement
from music21 import scale
from music21 import interval # confirmed requirement
from music21 import key # confirmed requirement
from music21 import chord
from music21 import converter
from music21 import analysis
from music21 import stream
from music21 import note # confirmed requirement
from os.path import exists as pathExists # confirmed requirement
from music21.converter import ConverterException # confirmed requirement
from music21.converter import ConverterFileException # confirmed requirement
# TODO: Quadruple-fun check that these are all that's required.

## TODO: Change all the classes to "new-type" (by making them inherit from object)
## class HarmonicFunctionalNote( object ):
## ........ for example

## Reference for documentation:

# define order to present names in documentation; use strings
#_DOC_ORDER = ['duration', 'quarterLength', 'editorial']
# documentation for all attributes (not properties or methods)
#_DOC_ATTR = {
#'editorial': 'a :class:`~music21.editorial.NoteEditorial` object that stores editorial information (comments, harmonic information, ficta) and certain display information (color, hidden-state).',
#'isChord': 'Boolean read-only value describing if this object is a Chord.',
#'lyrics': 'A list of :class:`~music21.note.Lyric` objects.',
#'tie': 'either None or a :class:`~music21.note.Tie` object.'
#}    



#-------------------------------------------------------------------------------
class NonsensicalInputError( Exception ):
   '''
   An error to throw when receiving nonsensical input that would otherwise
   cause undesirable behaviour but not likely crash the program.
   '''
   def __init__( self, val ):
      self.value = val
   def __str__( self ):
      return repr( self.value )
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
def chromaticScaleDegree( tonicKey, unknownPitch ):
   # NOTE: unit tests written
   '''
   Given a :class:`~music21.key.Key` and :class:`~music21.pitch.Pitch` or
   :class:`~music21.note.Note`, returns a :class:str that represents the
   scale degree of the Note/Pitch in the Key.
   
   :function:`chromaticScaleDegree` is tested for use with natural, sharp, flat,
   double-sharp, and double-flat scale degrees, and will return an empty str
   for all others.
   
   >>> from harrisonHarmony import *
   >>> from music21 import key, note, pitch
   >>> chromaticScaleDegree(key.Key('C'),note.Note('C'))
   '1'
   >>> chromaticScaleDegree(key.Key('F#'),pitch.Pitch('D'))
   '-6'
   >>> chromaticScaleDegree(key.Key('B-'),note.Note('E#5'))
   '##4'
   '''
   
   # TODO: See if this could be more elegant.
   
   # If there's an octave specified in unknownPitch, it causes problems, but
   # I'm not sure why. Even so, this will get rid of the octave number.
   unknownPitch = pitch.Pitch( unknownPitch.name )
   
   # get a Pitch from the tonic Key
   tonicPitch = tonicKey.pitchFromDegree( 1 )
   
   # first try to get interval between first two pitches
   medialInt = interval.notesToInterval( tonicPitch, unknownPitch )
   
   # would-be problems:
   #    dd-2 and ascending direction
   #    descending direction
   #    d-2 and 0 direction
   if ( ( 'dd-2' == medialInt.directedName ) and ( 1 == medialInt.direction ) or ( -1 == medialInt.direction ) or ( ( 0 == medialInt.direction ) and ( 'd-2' == medialInt.directedName ) ) ):
      medialInt = interval.notesToInterval( tonicPitch, interval.transposePitch( unknownPitch, interval.Interval( 'P8' ) ) )
   
   # now figure out the degree!
   mInt = medialInt.name # this is the name of the interval
   if ( 2 == len( mInt ) ):
      if ( 'M' == mInt[0] ):
         post = mInt[1]
      elif ( 'P' == mInt[0] ):
         post = mInt[1]
      elif ( 'm' == mInt[0] ):
         post = '-' + mInt[1]
      elif ( 'A' == mInt[0] ):
         post = '#' + mInt[1] ## only one possibility, whether P4/P5/P8 or other
      elif ( 'd' == mInt[0] ):
         if ( ( '4' == mInt[1] ) or ( '5' == mInt[1] ) ):
            post = '-' + mInt[1]
         elif ( '8' == mInt[1] ): # to avoid "-8"
            post = '-1'
         else:
            post = '--' + mInt[1]
      else:
         post = ""
   elif ( 3 == len( mInt ) ):
      if ( 'AA' == mInt[0:2] ):
         post = '##' + mInt[2]
      elif ( 'dd' == mInt[0:2] ):
         post = '--' + mInt[2]
      else:
         post = ""
      if ( '8' == post[2] ): # to avoid "--8"
         post = post[0:2] + '1'
   else:
      post = ""
   
   return post
# End function chromaticScaleDegree() ------------------------------------------



#-------------------------------------------------------------------------------
class HarmonicFunction( object ):
   # NOTE: unit tests written
   '''
   Holds four objects, representing the three harmonic functions and an
   "unknown' function for cases where we are unsure.
   
   - HarmonicFunction.Subdominant
   
   - HarmonicFunction.Tonic
   
   - HarmonicFunction.Dominant
   
   - HarmonicFunction.Unknown
   '''
   class Subdominant( object ):
      def __str__( self ):
         return 'Subdominant'
   class Dominant( object ):
      def __str__( self ):
         return 'Dominant'
   class Tonic( object ):
      def __str__( self ):
         return 'Tonic'
   class Unknown( object ):
      def __str__( self ):
         return 'Unknown function'
   
   #----------------------------------------------------------------------------
   @staticmethod
   def toLetter( function ):
      '''
      Outputs a one-character string when given a :class:`HarmonicFunction`
      object.
      
      >>> from harrisonHarmony import *
      >>> HarmonicFunction.toLetter( HarmonicFunction.Subdominant )
      'S'
      >>> HarmonicFunction.toLetter( HarmonicFunction.Unknown )
      'U'
      '''
      if HarmonicFunction.Subdominant == function:
         return 'S'
      elif HarmonicFunction.Dominant == function:
         return 'D'
      elif HarmonicFunction.Tonic == function:
         return 'T'
      elif HarmonicFunction.Unknown == function:
         return 'U'
      else:
         raise NonsensicalInputError( "Expected HarmonicFunction static member, but got " + str(function) + " instead." )
# Ends class: HarmonicFunction -------------------------------------------------



#-------------------------------------------------------------------------------
class FunctionalRole( object ):
   # NOTE: unit tests written
   '''
   Holds four objects representing the three functional roles and "unknown"
   for when we are unsure of the functional role.
   
   - FunctionalRole.Base
   
   - FunctionalRole.Agent
   
   - FunctionalRole.Associate
   
   - FunctionalRole.Unknown
   '''
   class Base( object ):
      def __str__( self ):
         return 'base'
   class Agent( object ):
      def __str__( self ):
         return 'agent'
   class Associate( object ):
      def __str__( self ):
         return 'associate'
   class Unknown( object ):
      def __str__( self ):
         return 'unknown role'
   
   #----------------------------------------------------------------------------
   @staticmethod
   def toLetter( role ):
      '''
      Outputs a two-character string when given a :class:`FunctionalRole`
      object.
      
      >>> from harrisonHarmony import *
      >>> FunctionalRole.toLetter( FunctionalRole.Agent )
      'ag'
      >>> FunctionalRole.toLetter( FunctionalRole.Base )
      'ba'
      >>> FunctionalRole.toLetter( FunctionalRole.Associate )
      'as'
      >>> FunctionalRole.toLetter( FunctionalRole.Unknown )
      'un'
      '''
      if FunctionalRole.Base == role:
         return "ba"
      elif FunctionalRole.Agent == role:
         return "ag"
      elif FunctionalRole.Associate == role:
         return "as"
      elif FunctionalRole.Unknown == role:
         return "un"
      else:
         raise NonsensicalInputError( "Expected FunctionalRole static member, but got " + str(role) + " instead." )
# End: class FunctionalRole ---------------------------------------------------



#-------------------------------------------------------------------------------
class RelativeVoicePosition( object ):
   # NOTE: unit tests written
   '''
   Holds four objects representing possibilities for the position of a voice
   relative to other voices.
   
   - RelativeVoicePosition.Lowest
   - RelativeVoicePosition.Middle
   - RelativeVoicePosition.Highest
   - RelativeVoicePosition.Solo
   '''
   class Lowest( object ):
      def __str__( self ):
         return 'lowest'
   class Middle( object ):
      def __str__( self ):
         return 'middle'
   class Highest( object ):
      def __str__( self ):
         return 'highest'
   class Solo( object ):
      def __str__( self ):
         return 'solo'
   
   #----------------------------------------------------------------------------
   @staticmethod
   def toLetter( position ):
      '''
      Outputs a string when given a :class:`RelativeVoicePosition` object.
      
      >>> from harrisonHarmony import *
      >>> RelativeVoicePosition.toLetter( RelativeVoicePosition.Lowest )
      'lowest'
      >>> RelativeVoicePosition.toLetter( RelativeVoicePosition.Middle )
      'middle'
      >>> RelativeVoicePosition.toLetter( RelativeVoicePosition.Highest )
      'highest'
      >>> RelativeVoicePosition.toLetter( RelativeVoicePosition.Solo )
      'solo'
      '''
      if position == RelativeVoicePosition.Lowest:
         return 'lowest'
      elif position == RelativeVoicePosition.Middle:
         return 'middle'
      elif position == RelativeVoicePosition.Highest:
         return 'highest'
      elif position == RelativeVoicePosition.Solo:
         return 'solo'
      else:
         raise NonsensicalInputError( "Expected RelativeVoicePosition static member, but got " + str(position) + " instead." )
# End: class RelativeVoicePosition ---------------------------------------------



#-------------------------------------------------------------------------------
class ConditionForFunction( object ):
   # NOTE: unit tests written
   '''
   Instantiable class that holds information about what is required for a
   possible harmonic function and functional role to be the correct choice for
   a HarmonicFunctionalNote.
   
   Also holds three contingencies:
   - ConditionforFunction.IsLowest : when a function is certain (as agents)
   
   - ConditionforFunction.IsLowestVoice : whether another note is in the
   lowest voice
   
   - ConditionforFunction.IsPresent : whether another specific scale degree
   or HarmonicFunctionalNote is present
   '''
   
   ## Static (non-)Variables
   class IsGuaranteed( object ):
      pass
   class IsLowestVoice( object ):
      pass
   class IsPresent( object ):
      pass
   
   ## Instance Variables
   # self.contingentOn --------- the Symbol saying what 
   # self.dependsOnThis --------- the HarmonicFunctionalNote influencing contingentOn
   def __init__( self, condition, harFuncNote ):
      '''
      Instantiate a condition.
      
      >>> from harrisonHarmony import *
      >>> from music21 import key
      >>> ConditionForFunction( ConditionForFunction.IsGuaranteed, '' )
      <harrisonHarmony.ConditionForFunction instance at 0x???????>
      >>> ConditionForFunction( ConditionForFunction.IsLowestVoice, HarmonicFunctionalNote( key.Key( 'C' ), HarmonicFunction.Tonic, FunctionalRole.Base, '1' ) )
      <harrisonHarmony.ConditionForFunction instance at 0x???????>
      >>> ConditionForFunction( ConditionForFunction.IsPresent, HarmonicFunctionalNote( key.Key( 'C' ), HarmonicFunction.Tonic, FunctionalRole.Agent, '3' ) )
      <harrisonHarmony.ConditionForFunction instance at 0x???????>
      '''
      self._contingentOn = condition
      self._dependsOnThis = harFuncNote
   
   def __repr__( self ):
        return "<harrisonHarmony.ConditionForFunction %s>" % self.__str__()

   def __str__( self ):
      if self.IsGuaranteed == self._contingentOn:
         return "guaranteed"
      elif self.IsLowestVoice == self._contingentOn:
         return "true if lowest voice is " + str(self._dependsOnThis)
      elif self.IsPresent == self._contingentOn:
         return "true in presence of " + str(self._dependsOnThis)
   
   def getContingency( self ):
      '''
      Returns the contingency of the condition.
      
      >>> from harrisonHarmony import *
      >>> a = ConditionForFunction( ConditionForFunction.IsGuaranteed, '' )
      >>> a.getContingency()
      <class 'harrisonHarmony.IsPresent'>
      '''
      return self._contingentOn
   
   def getDependency( self ):
      '''
      Returns the dependency of the condition.
      
      >>> from harrisonHarmony import *
      >>> from music21 import key
      >>> a = ConditionForFunction( ConditionForFunction.IsLowestVoice, HarmonicFunctionalNote( key.Key( 'C' ), HarmonicFunction.Tonic, FunctionalRole.Base, '1' ) )
      >>> a.getDependency()
      <HarmonicFunctionalNote instance at 0x???????>
      '''
      return self._dependsOnThis
   
   def equal( self, other ):
      '''
      Returns True if the two ConditionForFunction objects are equal,
      otherwise False. Tests both the contingency and dependency.
      
      >>> from harrisonHarmony import *
      >>> from music21 import key
      >>> a = ConditionForFunction( ConditionForFunction.IsLowestVoice, HarmonicFunctionalNote( key.Key( 'C' ), HarmonicFunction.Tonic, FunctionalRole.Base, '1' ) )
      >>> b = ConditionForFunction( ConditionForFunction.IsLowestVoice, HarmonicFunctionalNote( key.Key( 'C' ), HarmonicFunction.Tonic, FunctionalRole.Base, '1' ) )
      >>> a.equal( b )
      1
      >>> b = ConditionForFunction( ConditionForFunction.IsLowestVoice, HarmonicFunctionalNote( key.Key( 'C' ), HarmonicFunction.Tonic, FunctionalRole.Agent, '-3' ) )
      >>> a.equal( b )
      0
      '''
      if ( self._contingentOn == ConditionForFunction.IsGuaranteed ):
         if ( other._contingentOn == ConditionForFunction.IsGuaranteed ):
            return True
         else:
            return False
      elif ( isinstance( self._dependsOnThis, str ) and # if dependency is a str scale degree
      isinstance( other._dependsOnThis, str ) ):
         if ( self._dependsOnThis == other._dependsOnThis and
         self._contingentOn == other._contingentOn ):
            return True
         else:
            return False
      elif ( self._contingentOn == other._contingentOn and # if dependency is a HarmonicFunctionalNote
      self._dependsOnThis.equal( other._dependsOnThis ) ):
         return True
      else:
         return False
# End: class ConditionForFunction ----------------------------------------------



#-------------------------------------------------------------------------------
class HarmonicFunctionalNote( object ):
   '''
   Instantiable class to describe a note that has harmonic function. In the
   future, this class will extend :class:`music21.note.Note`
   '''
   
   ## Instance Variables
   # _key ---- it's a music21.key.Key
   # _function ---- it's a HarmonicFunction Symbol
   # _role ---- it's a FunctionalRole Symbol
   # _degree ---- it's a str, saying which scale degree
   # _stringRep ---- it's a str that is the string-format representation
   
   #----------------------------------------------------------------------------
   def __init__( self, theKey, theFunction, theRole, theDegree ):
      '''
      Given a :class:`music21.key.Key`, a :class:`harrisonHarmony.HarmonicFunction`,
      a :class:`harrisonHarmony.FunctionalRole`, and a scale degrees, produces
      the corresponding :class:`HarmonicFunctionalNote`.
      
      >>> from music21 import key
      >>> from harrisonHarmony import *
      >>> HarmonicFunctionalNote( key.Key( 'D-' ), HarmonicFunction.Subdominant, FunctionalRole.Associate, '1' )
      <HarmonicFunctionalNote ^1 as Subdominant associate in D->
      '''
      self._key = theKey
      self._function = theFunction
      self._role = theRole
      self._degree = theDegree
      
      # set string-format representation
      keyRep = self._key.tonic.name
      self._stringRep = '^' + self._degree + ' as ' + str(self._function()) \
                        + ' ' + str(self._role()) + ' in ' + keyRep
   
   #----------------------------------------------------------------------------
   def __repr__( self ):
        return "<HarmonicFunctionalNote %s>" % self.__str__()
   
   #----------------------------------------------------------------------------
   def __str__( self ):
      # str created in the __init__() function
      return self._stringRep
   
   #----------------------------------------------------------------------------
   def getKey( self ):
      '''
      Returns the :class:`music21.key.Key` of this instance.
      
      >>> from music21 import key
      >>> from harrisonHarmony import *
      >>> a = HarmonicFunctionalNote( key.Key( 'D-', HarmonicFunction.Subdominant, FunctionalRole.Associate, '1' )
      >>> a.getKey()
      <music21.key.Key of D- major>
      '''
      return self._key
   
   #----------------------------------------------------------------------------
   def getFunction( self ):
      '''
      Returns the HarmonicFunction of this instance.
      
      >>> from music21 import key
      >>> from harrisonHarmony import *
      >>> a = HarmonicFunctionalNote( key.Key( 'D-', HarmonicFunction.Subdominant, FunctionalRole.Associate, '1' )
      >>> a.getFunction()
      <class 'harrisonHarmony.Subdominant'>
      '''
      return self._function
   
   #----------------------------------------------------------------------------
   def getRole( self ):
      '''
      Returns the FunctionalRole of this instance.
      
      >>> from music21 import key
      >>> from harrisonHarmony import *
      >>> a = HarmonicFunctionalNote( key.Key( 'D-', HarmonicFunction.Subdominant, FunctionalRole.Associate, '1' )
      >>> a.getRole()
      <class 'harrisonHarmony.Associate'>
      '''
      return self._role
   
   #----------------------------------------------------------------------------
   def getDegree( self ):
      '''
      Returns the str representing the scale degree of this instance.
      
      >>> from music21 import key
      >>> from harrisonHarmony import *
      >>> a = HarmonicFunctionalNote( key.Key( 'D-', HarmonicFunction.Subdominant, FunctionalRole.Associate, '1' )
      >>> a.getDegree()
      '1'
      '''
      return self._degree
   
   #----------------------------------------------------------------------------
   def getLabel( self ):
      '''
      Returns a str that is a label representing the key, function, and
      functional role of this instance.
      
      >>> from music21 import key
      >>> from harrisonHarmony import *
      >>> a = HarmonicFunctionalNote( key.Key( 'D-' ), HarmonicFunction.Subdominant, FunctionalRole.Associate, '1' )
      >>> a.getLabel()
      'D-:Sas'
      >>> a = HarmonicFunctionalNote( key.Key( 'F' ), HarmonicFunction.Unknown, FunctionalRole.Unknown, '-4' )
      >>> a.getLabel()
      'F:Uun'
      >>> a = HarmonicFunctionalNote( key.Key( 'F#' ), HarmonicFunction.Tonic, FunctionalRole.Agent, '3' )
      >>> a.getLabel()
      'F#:Tag'
      >>> a = HarmonicFunctionalNote( key.Key( 'E' ), HarmonicFunction.Dominant, FunctionalRole.Base, '5' )
      >>> a.getLabel()
      'E:Dba'
      '''
      return self._key.tonic.name + ":" + HarmonicFunction.toLetter( self._function ) \
            + FunctionalRole.toLetter( self._role )
   # End: HarmonicFunctionalNote.getLabel() ------------------------------------
      
   #----------------------------------------------------------------------------
   def equal( self, other ):
      '''
      Returns True if the two HarmonicFunctionalNote objects are semantically
      equivalent, or False if they are not.
      
      >>> from music21 import key
      >>> from harrisonHarmony import *
      >>> a = HarmonicFunctionalNote( key.Key( 'D-' ), HarmonicFunction.Subdominant, FunctionalRole.Associate, '1' )
      >>> b = HarmonicFunctionalNote( key.Key( 'D-' ), HarmonicFunction.Dominant, FunctionalRole.Associate, '2' )
      >>> a.equal( b )
      False
      >>> b = HarmonicFunctionalNote( key.Key( 'D-' ), HarmonicFunction.Subominant, FunctionalRole.Associate, '1' )
      >>> a.equal( b )
      True
      >>> b = HarmonicFunctionalNote( key.Key( 'd-' ), HarmonicFunction.Subominant, FunctionalRole.Associate, '1' )
      >>> a.equal( b )
      True
      '''
      if self._key.tonic.name.upper() == other._key.tonic.name.upper() \
      and self._function == other._function \
      and self._role == other._role \
      and self._degree == other._degree:
         return True
      else:
         return False
# End: class HarmonicFunctionalNote



#-------------------------------------------------------------------------------
class HarmonicFunctionalChord:
   '''
   Instantiable class that represents a chord made of HarmonicFunctionalNote
   objects in a known key.
   '''
   
   ## Instance Variables
   # self._key ---- music21.key.Key; represents the key of the harmony
   # self._bFn ---- it's a HarmonicFunctionalNote
   # self._oFns ---- it's a List of HarmonicFunctionNote s
   # self._label ---- it's a str
   
   #----------------------------------------------------------------------------
   def __init__( self, bassFunction, otherFunctions = [], theKey = None ):
      '''
      Given a HarmonicFunctionalNote and a list of other HarmonicFunctionalNote
      objects, produces the corresponding HarmonicFunctionalChord.
      
      The first argument is taken as the lowest voice, and the second argument
      as a list, from lowest to highest, of the rest of the voices. The
      second argument is optional, for situations where only one voice is present.
      
      At least for now, the key is understood as the key of the lowest voice.
      You may also provide a :class:`music21.key.Key` as the third argument
      for situations where the prevailing key is not represented in the lowest
      voice.
      
      >>> from harrisonHarmony import *
      >>> T = HarmonicFunction.Tonic
      >>> ag = FunctionalRole.Agent
      >>> Tag = HarmonicFunctionalNote( key.Key( 'C' ), T, ag, '3' )
      >>> HarmonicFunctionalChord( Tag )
      0x???????>
      >>> ba = FunctionalRole.Base
      >>> as = FunctionalRole.Associate
      >>> Tba = HarmonicFunctionalNote( key.Key( 'C' ), T, ba, '1' )
      >>> Tas = HarmonicFunctionalNote( key.Key( 'C' ), T, as, '5' )
      >>> HarmonicFunctionalChord( Tba, [Tag,Tas,Tba] )
      0x???????>
      >>> # Subdominant tonicization?
      >>> HarmonicFunctionalChord( Tba, [Tag,Tas,Tba], key.Key( 'G' ) )
      0x???????>
      '''
      if None == theKey:
         # take the bass note's key
         self._key = bassFunction.getKey()
      else:
         self._key = theKey
      
      self._bFn = bassFunction
      self._oFns = otherFunctions
      self._label = self.__makeMyLabel()
      
      # verify the objects are the right type, then assign
      # theKey
      #if isinstance( theKey, key.Key ):
         #self.key = theKey
      #elif None == theKey:
         #pass # we'll assign after error-checking bassFunction
      #else:
         #raise InvalidInputError( "HarmonicFunctionalChord(): Optional third constructor argument must be a music21.key.Key; received " + str(type(theKey)) )
      # bassFunction
      #if isinstance( bassFunction, HarmonicFunctionalNote ):
         #self.bFn = bassFunction
      #else:
         #raise InvalidInputError( "HarmonicFunctionalChord(): First constructor argument must be a mumt621.HarmonicFunctionalNote; received " + str(type(bassFunction)) )
      # if theKey wasn't given, we'll assign it now from the bassFunction
      #if None == theKey:
         #self.key = bassFunction.getKey()
      ## otherFunctions
      #self.oFns = []
      #if isinstance( otherFunctions, list ):
         #for oFn in otherFunctions:
            #if isinstance( oFn, HarmonicFunctionalNote ):
               #self.oFns.append( oFn )
            #else:
               #raise InvalidInputError( "HarmonicFunctionalChord(): Second constructor argument must be a list of mumt621.HarmonicFunctionalNote; received a " + str(type(oFn)) )
      #else:
         #raise InvalidInputError( "HarmonicFunctionalChord(): Second constructor argument must be a list of mumt621.HarmonicFunctionalNote; received " + str(type(otherFunctions)) )
      # get the label for this note
      #self._label = self.__makeMyLabel()
      #
   
   #----------------------------------------------------------------------------
   def __repr__( self ):
        return "<HarmonicFunctionalChord %s>" % self.__str__()
   
   #----------------------------------------------------------------------------
   def __str__( self ):
      # str created in the __makeMyLabel() function
      return self._label
   
   ############################################################
   ## PRIVATE FUNCTION                                       ##
   ## makeMyLabel() --> None                                 ##
   ##                                                        ##
   ## Figures out the label for this HarmonicFunctionalChord ##
   ############################################################
   def __makeMyLabel( self ):
      # just put in the function of the bass note, if it's good
      post = HarmonicFunction.toLetter( self._bFn.getFunction() )
      if "U" == post:
         pass # maybe later, we'll erase it and do something...
      # see what the other functions are
      additionals = []
      for additionalFunction in self._oFns:
         potentialNewFunction = HarmonicFunction.toLetter( additionalFunction.getFunction() )
         if potentialNewFunction != post and potentialNewFunction not in additionals:
            additionals.append( potentialNewFunction )
      additionals = set(additionals) # to get rid of duplicates
      # add the other functions on 
      if len(additionals) > 0:
         if "S" in additionals:
            post += "^S"
         if "T" in additionals:
            if len(post) > 1:
               post += "T"
            else:
               post += "^T"
         if "D" in additionals:
            if len(post) > 1:
               post += "D"
            else:
               post += "^D"
      # append the scale degree of the lowest voice
      post += "(" + self._bFn.getDegree() + ")"
      # assign the label to this object
      return post
   
   #----------------------------------------------------------------------------
   def getKey( self ):
      '''
      Returns the :class:`music21.key.Key` of the lowest voice, or the key
      that was provided on initialization.
      
      >>> from harrisonHarmony import *
      >>> T = HarmonicFunction.Tonic
      >>> ba = FunctionalRole.Base
      >>> ag = FunctionalRole.Agent
      >>> as = FunctionalRole.Associate
      >>> Tag = HarmonicFunctionalNote( key.Key( 'C' ), T, ag, '3' )
      >>> Tba = HarmonicFunctionalNote( key.Key( 'C' ), T, ba, '1' )
      >>> Tas = HarmonicFunctionalNote( key.Key( 'C' ), T, as, '5' )
      >>> a = HarmonicFunctionalChord( Tba, [Tag,Tas,Tba] )
      >>> a.getKey()
      <music21.key.Key of C major>
      >>> a = HarmonicFunctionalChord( Tba, [Tag,Tas,Tba], key.Key( 'G' ) )
      >>> a.getKey()
      <music21.key.Key of G major>
      '''
      return self._key
   
   #----------------------------------------------------------------------------
   def getFunctionalNotes( self ):
      '''
      Returns a List of all HarmonicFunctionalNote objects in the chord.
      '''
      return [self._bFn] + self._oFns
   
   #----------------------------------------------------------------------------
   def getBassFunctionalNote( self ):
      '''
      Returns a List of the HarmonicFunctionalNote that is the lowest voice.
      '''
      return self._bFn
   
   #----------------------------------------------------------------------------
   def getOtherFunctionalNotes( self ):
      '''
      Returns a List of all HarmonicFunctionalNote objects in upper voices.
      '''
      return self._oFns
   
   #----------------------------------------------------------------------------
   def getLabel( self ):
      '''
      Returns a str with a label representing the function(s) of the chord, and
      the scale degree of the lowest voice.
      
      >>> from harrisonHarmony import *
      >>> T = HarmonicFunction.Tonic
      >>> ba = FunctionalRole.Base
      >>> ag = FunctionalRole.Agent
      >>> as = FunctionalRole.Associate
      >>> Tag = HarmonicFunctionalNote( key.Key( 'C' ), T, ag, '3' )
      >>> Tba = HarmonicFunctionalNote( key.Key( 'C' ), T, ba, '1' )
      >>> Tas = HarmonicFunctionalNote( key.Key( 'C' ), T, as, '5' )
      >>> a = HarmonicFunctionalChord( Tba, [Tag,Tas,Tba] )
      >>> a.getLabel()
      'T(1)'
      >>> S = HarmonicFunction.Tonic
      >>> Sag = HarmonicFunctionalNote( key.Key( 'C' ), S, ag, '-6' )
      >>> a = HarmonicFunctionalChord( Sag, [Tba,Tag,Tas] )
      >>> a.getLabel()
      'S^T(-6)'
      '''
      return self._label
   
   #----------------------------------------------------------------------------
   def getVerboseLabel( self ):
      '''
      Returns a label representing the HarmonicFunctionalNote.getLabel() of each
      chord member, from lowest to highest, joined by a comma.
      
      >>> from harrisonHarmony import *
      >>> T = HarmonicFunction.Tonic
      >>> ag = FunctionalRole.Agent
      >>> Tag = HarmonicFunctionalNote( key.Key( 'C' ), T, ag, '3' )
      >>> Tba = HarmonicFunctionalNote( key.Key( 'C' ), T, ba, '1' )
      >>> Tas = HarmonicFunctionalNote( key.Key( 'C' ), T, as, '5' )
      >>> a = HarmonicFunctionalChord( Tba, [Tag,Tas,Tba] )
      >>> a.getVerboseLabel()
      'C:Tba,C:Tag,C:Tas,C:Tba'
      '''
      # TODO: test this
      post = self._bFn.getLabel()
      for member in self._oFns:
         post += "," + member.getLabel()
      return post
   
   #----------------------------------------------------------------------------
   def equal( self, other ):
      '''
      Returns True if the two HarmonicFunctionalChord objects are
      semantically equivalent, or False if they are not.
      
      >>> from harrisonHarmony import *
      >>> T = HarmonicFunction.Tonic
      >>> ba = FunctionalRole.Base
      >>> ag = FunctionalRole.Agent
      >>> as = FunctionalRole.Associate
      >>> Tag = HarmonicFunctionalNote( key.Key( 'C' ), T, ag, '3' )
      >>> Tba = HarmonicFunctionalNote( key.Key( 'C' ), T, ba, '1' )
      >>> Tas = HarmonicFunctionalNote( key.Key( 'C' ), T, as, '5' )
      >>> a = HarmonicFunctionalChord( Tba, [Tag,Tas,Tba] )
      >>> b = HarmonicFunctionalChord( Tag, [Tag,Tas,Tba] )
      >>> a.equal( b )
      False
      >>> b = HarmonicFunctionalChord( Tba, [Tag,Tas,Tba] )
      >>> a.equal( b )
      True
      '''
      if not isinstance( other, HarmonicFunctionalChord ):
         return False
      if ( self._key.tonic.name.upper() == other._key.tonic.name.upper() and self._bFn.equal( other._bFn ) ):
         if len(self._oFns) != len(other._oFns):
            return False
         #
         for function in self._oFns:
            foundMatch = False
            for possibleEquivalent in other._oFns:
               if function.equal( possibleEquivalent ):
                  foundMatch = True
            if foundMatch is False:
               return False
         #
         for function in other._oFns:
            foundMatch = False
            for possibleEquivalent in self._oFns:
               if function.equal( possibleEquivalent ):
                  foundMatch = True
            if foundMatch is False:
               return False
         #
         return True
      else:
         return False
# end Class HarmonicFunctionalChord



#-------------------------------------------------------------------------------
def possibleFunctionsFromScaleDegree( theKey, scaleDegree, position ):
   '''
   When given a scale :class:`music21.key.Key` with a scale degree (from
   `chromaticScaleDegree()` ) and :class:`harrisonHarmony.RelativeVoicePosition`,
   outputs a list of possible :class:`harrisonharmony.HarmonicFunctionalNote`
   objects and their :class:`harrisonHarmony.ConditionForFunction` for being
   true.
   
   Note: If result is what pFFSD() returns, then each first index in result,
   being result[0] and result[1] and so on, represents an "or" possibility.
   If len(result[x][1]) > 1 then all ConditionForFunction objects must be
   satisified... this is an "and" possibility.
   
   Limitations: Currently only works for the diatonic, single-sharp, and
   single-flat scale degrees.
   
   >>> from harrisonHarmony import *
   >>> from music21 import key
   >>> Etonic = key.Key( 'E' ) # major or minor, same thing
   >>> a = possibleFunctionsFromScaleDegree( Etonic, '1', RelativeVoicePosition.Lowest )
   [[<HarmonicFunctionalNote E major Tonic Base '1'>, <ConditionForFunction IsGuaranteed>]]
   
   TODO: finish those tests
   And so on... I didn't finish writing those tests because I haven't serialized them yet.
   '''
   
   post = [] # holds what we'll return
   
   ## We have to start with possible applied Subdominant leading tones, or else the -3, -6, and -7 will
   ## appear as a possibility *after* the ConditionForFunction.IsGuaranteed for Agent, so it won't
   ## be considered.
   if ( 2 == len(scaleDegree) and '-' == scaleDegree[0] ):
      ## finds the applied key--probably a more efficient way to do this one!
      ## note that a Subdominant leading tone resolves by step downward to applied ^5
      appliedKey = key.Key( pitch.Pitch( theKey.getPitches()[int(scaleDegree[1])-1].name ).transpose( 'M-6' ).name )
      ## adds the relevant stuff
      post.append( [HarmonicFunctionalNote( appliedKey, HarmonicFunction.Subdominant, FunctionalRole.Agent, scaleDegree ), \
            ConditionForFunction( ConditionForFunction.IsPresent, HarmonicFunctionalNote( appliedKey, HarmonicFunction.Subdominant, FunctionalRole.Base, '4' ) )] )
      ## not sure, but I don't think there's a Subdominant-equivalent for the traditional applied vii
      # post.append( [HarmonicFunctionalNote( appliedKey, HarmonicFunction.Dominant, FunctionalRole.Agent ), ConditionForFunction( ConditionForFunction.IsPresent, '2' ), ConditionForFunction( ConditionForFunction.IsPresent, '4' )] )
   
   ## agent is always (and only ever) agent
   if ( '-3' == scaleDegree or '3' == scaleDegree ):
      post.append( [HarmonicFunctionalNote( theKey, HarmonicFunction.Tonic, FunctionalRole.Agent, scaleDegree ), ConditionForFunction( ConditionForFunction.IsGuaranteed, "" ) ] )
   elif ( '-6' == scaleDegree or '6' == scaleDegree ):
      post.append( [HarmonicFunctionalNote( theKey,HarmonicFunction.Subdominant,FunctionalRole.Agent, scaleDegree ), ConditionForFunction( ConditionForFunction.IsGuaranteed, "" ) ] )
   elif ( '-7' == scaleDegree or '7' == scaleDegree ):
      post.append( [HarmonicFunctionalNote( theKey,HarmonicFunction.Dominant,FunctionalRole.Agent, scaleDegree ), ConditionForFunction( ConditionForFunction.IsGuaranteed, "" ) ] )
   
   ## base is base if in lowest voice
   if ( RelativeVoicePosition.Lowest == position and '1' == scaleDegree ):
      post.append( [HarmonicFunctionalNote( theKey, HarmonicFunction.Tonic, FunctionalRole.Base, scaleDegree ), ConditionForFunction( ConditionForFunction.IsGuaranteed, "" )] )
   elif ( RelativeVoicePosition.Lowest == position and '4' == scaleDegree ):
      post.append( [HarmonicFunctionalNote( theKey, HarmonicFunction.Subdominant, FunctionalRole.Base, scaleDegree ), ConditionForFunction( ConditionForFunction.IsGuaranteed, "" )] )
   elif ( RelativeVoicePosition.Lowest == position and '5' == scaleDegree ):
      post.append( [HarmonicFunctionalNote( theKey, HarmonicFunction.Dominant, FunctionalRole.Base, scaleDegree ), ConditionForFunction( ConditionForFunction.IsGuaranteed, "" )] )
   
   ## here we get things that accumulate multiple functions
   if ( RelativeVoicePosition.Lowest != position ):
      if ( '1' == scaleDegree ):
         post.append( [HarmonicFunctionalNote( theKey, HarmonicFunction.Tonic, FunctionalRole.Base, scaleDegree ), ConditionForFunction( ConditionForFunction.IsPresent, HarmonicFunctionalNote(theKey, HarmonicFunction.Tonic, FunctionalRole.Agent, "3" ) )] )
         post.append( [HarmonicFunctionalNote( theKey, HarmonicFunction.Tonic, FunctionalRole.Base, scaleDegree ), ConditionForFunction( ConditionForFunction.IsPresent, HarmonicFunctionalNote(theKey, HarmonicFunction.Tonic, FunctionalRole.Agent, "-3" ) )] )
         post.append( [HarmonicFunctionalNote( theKey, HarmonicFunction.Subdominant, FunctionalRole.Associate, scaleDegree ), ConditionForFunction( ConditionForFunction.IsPresent, HarmonicFunctionalNote(theKey, HarmonicFunction.Subdominant, FunctionalRole.Agent, "6" ) )] )
         post.append( [HarmonicFunctionalNote( theKey, HarmonicFunction.Subdominant, FunctionalRole.Associate, scaleDegree ), ConditionForFunction( ConditionForFunction.IsPresent, HarmonicFunctionalNote(theKey, HarmonicFunction.Subdominant, FunctionalRole.Agent, "-6" ) )] )
         post.append( [HarmonicFunctionalNote( theKey, HarmonicFunction.Subdominant, FunctionalRole.Associate, scaleDegree ), ConditionForFunction( ConditionForFunction.IsLowestVoice, HarmonicFunctionalNote(theKey, HarmonicFunction.Subdominant, FunctionalRole.Base, '4' ) )] )
      elif ( '4' == scaleDegree ):
         post.append( [HarmonicFunctionalNote( theKey, HarmonicFunction.Subdominant, FunctionalRole.Base, scaleDegree ), ConditionForFunction( ConditionForFunction.IsPresent, HarmonicFunctionalNote(theKey, HarmonicFunction.Subdominant, FunctionalRole.Agent, "6" ) )] )
         post.append( [HarmonicFunctionalNote( theKey, HarmonicFunction.Subdominant, FunctionalRole.Base, scaleDegree ), ConditionForFunction( ConditionForFunction.IsPresent, HarmonicFunctionalNote(theKey, HarmonicFunction.Subdominant, FunctionalRole.Agent, "-6" ) )] )
      elif ( '5' == scaleDegree ):
         post.append( [HarmonicFunctionalNote( theKey, HarmonicFunction.Dominant, FunctionalRole.Base, scaleDegree ), ConditionForFunction( ConditionForFunction.IsPresent, HarmonicFunctionalNote(theKey, HarmonicFunction.Dominant, FunctionalRole.Agent, "7" ) )] )
         post.append( [HarmonicFunctionalNote( theKey, HarmonicFunction.Dominant, FunctionalRole.Base, scaleDegree ), ConditionForFunction( ConditionForFunction.IsPresent, HarmonicFunctionalNote(theKey, HarmonicFunction.Dominant, FunctionalRole.Agent, "-7" ) )] )
         post.append( [HarmonicFunctionalNote( theKey, HarmonicFunction.Tonic, FunctionalRole.Associate, scaleDegree ), ConditionForFunction( ConditionForFunction.IsPresent, HarmonicFunctionalNote(theKey, HarmonicFunction.Tonic, FunctionalRole.Agent, "3" ) )] )
         post.append( [HarmonicFunctionalNote( theKey, HarmonicFunction.Tonic, FunctionalRole.Associate, scaleDegree ), ConditionForFunction( ConditionForFunction.IsPresent, HarmonicFunctionalNote(theKey, HarmonicFunction.Tonic, FunctionalRole.Agent, "-3" ) )] )
         post.append( [HarmonicFunctionalNote( theKey, HarmonicFunction.Tonic, FunctionalRole.Associate, scaleDegree ), ConditionForFunction( ConditionForFunction.IsLowestVoice, HarmonicFunctionalNote(theKey, HarmonicFunction.Tonic, FunctionalRole.Base, '1' ) )] )
   
   if ( '2' == scaleDegree ):
      post.append( [HarmonicFunctionalNote( theKey, HarmonicFunction.Dominant, FunctionalRole.Associate, scaleDegree ), ConditionForFunction( ConditionForFunction.IsPresent, HarmonicFunctionalNote(theKey, HarmonicFunction.Dominant, FunctionalRole.Agent, "7" ) )] )
      post.append( [HarmonicFunctionalNote( theKey, HarmonicFunction.Dominant, FunctionalRole.Associate, scaleDegree ), ConditionForFunction( ConditionForFunction.IsPresent, HarmonicFunctionalNote(theKey, HarmonicFunction.Dominant, FunctionalRole.Agent, "-7" ) )] )
      if ( RelativeVoicePosition.Lowest != position ):
         post.append( [HarmonicFunctionalNote( theKey, HarmonicFunction.Dominant, FunctionalRole.Associate, scaleDegree ), ConditionForFunction( ConditionForFunction.IsLowestVoice, HarmonicFunctionalNote(theKey, HarmonicFunction.Dominant, FunctionalRole.Base, '5' ) )] )
   ## here are probable applied Dominant leading tones
   elif ( 2 == len(scaleDegree) and '#' == scaleDegree[0] ):
      ## finds the applied key--probably a more efficient way to do this one!
      appliedKey = key.Key( pitch.Pitch( theKey.getPitches()[int(scaleDegree[1])-1].name ).transpose( 'M2' ).name )
      ## adds the relevant stuff
      post.append( [HarmonicFunctionalNote( appliedKey, HarmonicFunction.Dominant, FunctionalRole.Agent, '7' ), ConditionForFunction( ConditionForFunction.IsPresent, HarmonicFunctionalNote(appliedKey, HarmonicFunction.Dominant, FunctionalRole.Base, '5' ) )] )
      post.append( [HarmonicFunctionalNote( appliedKey, HarmonicFunction.Dominant, FunctionalRole.Agent, '7' ), ConditionForFunction( ConditionForFunction.IsPresent, HarmonicFunctionalNote(appliedKey, HarmonicFunction.Dominant, FunctionalRole.Associate, '2' ) ), \
                     ConditionForFunction( ConditionForFunction.IsPresent, HarmonicFunctionalNote(appliedKey, HarmonicFunction.Unknown, FunctionalRole.Unknown, '4') )] )
   
   return post
# End function possibleFunctionsFromScaleDegree() ------------------------------



#-------------------------------------------------------------------------------
def reconcilePossibleFunctions( functions ):
   '''
   Takes a list of the outputs from 
   :class:`harrisonHarmony.possibleFunctionsFromScaleDegree()` and determines
   which functions are most likely to be true. Assumes the voices are given in
   ascending order, so the first element of the argument is always the lowest
   voice, the last element is always the highest voice, and all other elements
   are middle voices.
   
   Output takes the form of a :class:`HarmonicFunctionalChord`.
   
   >>> from harrisonHarmony import *
   >>> from music21 import key
   >>> FStonic = key.Key( 'F#' ) # major or minor, same thing
   >>> a = possibleFunctionsFromScaleDegree( FStonic, '1', RelativeVoicePosition.Lowest )
   >>> b = possibleFunctionsFromScaleDegree( FStonic, '5', RelativeVoicePosition.Middle )
   >>> c = possibleFunctionsFromScaleDegree( FStonic, '1', RelativeVoicePosition.Middle )
   >>> d = possibleFunctionsFromScaleDegree( FStonic, '3', RelativeVoicePosition.Highest )
   >>> reconcilePossibleFunctions( [a, b, c, d] )
   HarmonicFunctionalChord( [base, associate, base, agent] )
   '''
   
   ## TODO: contemplate dynamically determining which is the lowest/highest voice
   ## TODO: Have a more elegant way to get "unknown" functions.
   ## TODO: What happens when one note has multiple simultaneous functions?
   ## TODO: Doesn't play nicely with applied chords.
   ## TODO: more efficient implementations probably exist

   post = [] # holds what we'll return
   # make a list of the same length as the number of voices we have
   for item in functions:
      post.append( "" )
   
   if ( len(functions) != len(post) ):
      print( "functions: " + str(len(functions)) + " and post " + str(len(post)) )
   
   # This will hold the number of times we've been through the loop,
   # and if we haven't come up with an answer by safeGuard == 1000 then we're
   # probably not going to, so we'll just quit.
   safeGuard = 0
   # Infinite Loop! Supposed to end when all of "post" has something useful.
   while ( 5 == 5 ):
      safeGuard += 1
      # if lowest voice is undecided, decide the lowest voice
      if ( "" == post[0] ):
         # look for a guaranteed function
         for possibility in functions[0]:
            if ( ConditionForFunction.IsGuaranteed == possibility[1].getContingency() ):
               post[0] = possibility[0]
         # if we still don't have an answer...
         if ( "" == post[0] ):
            # go through the list of possibilities again
            for possibility in functions[0]:
               # If a function is contingent on something else being present, look
               # for "something else."
               if ( ConditionForFunction.IsPresent == possibility[1].getContingency() ):
                  # this is what we have to find
                  dependency = possibility[1].getDependency()
                  # we search the list of things we already know for sure
                  for alreadyConfirmedNote in post:
                     if "" != alreadyConfirmedNote:
                        if alreadyConfirmedNote.equal( dependency ):
                           post[0] = possibility[0]
      # Go through upper voices.
      # Unfortunately we have to remember index numbers, so the voices are
      # placed into "post" in the right order.
      for index in range(1,len(functions)):
         # Do we still need to solve this index?
         # Look for functions that depend on the bass note.
         if ( "" == post[index] ):
            # if we have a confirmed bass note
            if ( "" != post[0] ):
               # look through each of the conditions
               for possibility in functions[index]:
                  # if a condition depends on the bass voice
                  if ( ConditionForFunction.IsLowestVoice == possibility[1].getContingency() ):
                     # if the bass voice is that function
                     if ( possibility[1].getDependency().equal( post[0]  )):
                        # assign it
                        post[index] = possibility[0]
         # Do we still need to solve this index?
         # Look for functions that depend on a non-bass note.
         if ( "" == post[index] ): # same algorithm as for bass notes
            for possibility in functions[index]:
               if ( ConditionForFunction.IsPresent == possibility[1].getContingency() ):
                  dependency = possibility[1].getDependency()
                  for alreadyConfirmedNote in post:
                     if "" != alreadyConfirmedNote:
                        if alreadyConfirmedNote.equal( dependency ):
                           post[index] = possibility[0]
         # NB: The IsGuaranteed must go last, because of complicated reasons where it may not be guaranteed.
         # Do we still need to solve this index?
         # Look for a guaranteed function,
         if ( "" == post[index] ):
            for possibility in functions[index]:
               if ( ConditionForFunction.IsGuaranteed == possibility[1].getContingency() ):
                  post[index] = possibility[0]
      # loop-finish check: do all the elements of "post" have something useful?
      unassignedNotes = len(post)
      for thing in post:
         if thing != "":
            unassignedNotes -= 1
      if 0 == unassignedNotes:
         return HarmonicFunctionalChord( post[0], post[1:] )
      elif ( safeGuard > 5 ):
         # TODO: Make this more elegant...
         # I should be able to assign an "unknown" function/action as something other than a last resort
         for i in range(len(post)):
            if post[i] == "":
               post[i] = HarmonicFunctionalNote( functions[i][0][0].getKey(), HarmonicFunction.Unknown, FunctionalRole.Unknown, functions[i][0][0].getDegree() )
         return HarmonicFunctionalChord( post[0], post[1:] )
   # end Infinite Loop
# End function reconcilePossibleFunctions() ------------------------------------



#-------------------------------------------------------------------------------
def labelThisChord( whatKey, harmony, verbosity = 'concise' ):
   '''
   Given a :class:`music21.key.Key` and :class:`music21.chord.Chord`, finds the
   corresponding str label. There is an optional third argument to specify
   whether you want a "verbose" or "concise" label; default is "concise."
   
   >>> from music21 import key, chord
   >>> from harrisonHarmony import *
   >>> Dftonic = key.Key( 'D-' )
   >>> aChord = chord.Chord( ['D-', 'F', 'A-', 'D-'] )
   >>> labelThisChord( Dftonic, aChord )
   'T(1)'
   >>> labelThisChord( Dftonic, aChord, 'verbose' )
   'D-:Tba,D-:Tag,D-:Tas,D-:Tba'
   >>> aChord = chord.Chord( ['F', 'G-', 'D-', 'B-'] )
   >>> labelThisChord( Dftonic, aChord )
   'T^S(3)'
   >>> labelThisChord( Dftonic, aChord, 'verbose' )
   'D-:Tag,D-:Sba,D-:Tba,D-:Sag'
   '''
   
   ## sort the Chord from lowest to highest, using MIDI note number
   harmony = chord.Chord( sorted( harmony, key=lambda a: a.midi ) )
   
   ## this will hold a list of str that are the scale degrees present in the chord
   listOfScaleDegrees = []
   
   ## find the scale degrees of each chord member
   for chordMember in harmony:
      listOfScaleDegrees.append( chromaticScaleDegree( whatKey, chordMember ) )
   
   ## this holds the HarmonicFunctionalNote corresponding to each scale degree
   ## start by putting the bass voice on
   listOfHarmonicFunctionalNotes = [ possibleFunctionsFromScaleDegree( whatKey, listOfScaleDegrees[0], RelativeVoicePosition.Lowest ) ]
   
   ## this puts the scale degrees into HarmonicFunctionalNotes, taking account of which is the bass voice
   ## I should change this to use the map() function
   for ecks in range( 1, len(listOfScaleDegrees) - 1 ):
      listOfHarmonicFunctionalNotes.append( possibleFunctionsFromScaleDegree( whatKey, listOfScaleDegrees[ecks], RelativeVoicePosition.Middle ) )
   
   ## finally, put add the highest voice
   listOfHarmonicFunctionalNotes.append( possibleFunctionsFromScaleDegree( whatKey, listOfScaleDegrees[len(listOfScaleDegrees)-1], RelativeVoicePosition.Highest ) )
   
   ## Reconcile the list of HarmonicFunctionalNote into a HarmonicFunctionalChord,
   ## then return the label.
   if 'concise' == verbosity:
      return reconcilePossibleFunctions( listOfHarmonicFunctionalNotes ).getLabel()
   elif 'verbose' == verbosity:
      return reconcilePossibleFunctions( listOfHarmonicFunctionalNotes ).getVerboseLabel()
   else:
      raise NonsensicalInputError( "labelThisChord(): third argument must be 'verbose' or 'concise' but I got '" + verbosity + "'" )
# End function labelThisChord() ------------------------------------------------



#-------------------------------------------------------------------------------
def analyzeThis( pathname, theSettings ):
   '''
   Given the path to a music21-supported score, imports the score, performs a
   harmonic-functional analysis, annotates the score, and displays it with show().
   
   The second argument is a HarrisonHarmonySettings object.
   '''
   
   # TODO: parallelization: we could do .chordify() and .getSolution() (for key-finding)
   # simultaneously, and (for as long as we're only doing 'vertical' analysis) we could
   # also analyze all the chords simultaneously.
   
   theScore = theChords = None
   # See what input we have...
   if isinstance( pathname, str ):
      ## get the score
      print( "Importing score to music21." )
      try:
         theScore = converter.parse( pathname )
      except ConverterException:
         raise
      except ConverterFileException:
         raise
      ## "chordify" the score
      print( "Chordifying the score." )
      theChords = theScore.chordify()
   elif isinstance( pathname, stream.Score ):
      theScore = pathname
      ## "chordify" the score
      print( "Chordifying the score." )
      theChords = theScore.chordify()
   elif isinstance( pathname, stream.Part ):
      theChords = pathname
   else:
      raise NonsensicalInputError( "analyzeThis(): input must be str, Score, or Part; received " + str(type(pathname)) )
   
   ## Remove ties because, if we're using the "lyric" property,
   ## MusicXML-->LilyPond won't allow two annotations for chords with tied notes.
   ## It doesn't hurt to do this, even if it's already been done.
   print( "Removing ties from the score." )
   for eachMeasure in theChords:
      if isinstance( eachMeasure, stream.Measure ):
         for event in eachMeasure:
            if isinstance( event, chord.Chord ):
               for chordMember in event:
                  event.tie = None
      elif isinstance( eachMeasure, chord.Chord ):
         for chordMember in eachMeasure:
            chordMember.tie = None
   
   ## find the key
   anal = analysis.discrete.SimpleWeights()
   whatKey = anal.getSolution( theChords )
   
   print( "Parsing and labelling chords." )
   # find the index of the bass part
   foundBassPart = False
   tryThisIndex = len(theScore) - 1
   indexOfBassPart = -1
   while False == foundBassPart:
      if -1 == tryThisIndex:
         foundBassPart = True
      elif isinstance( theScore[tryThisIndex], stream.Part ):
         foundBassPart = True
         indexOfBassPart = tryThisIndex
      else:
         tryThisIndex -= 1
   
   # Parse and label the chords.
   for measure in theChords:
      if isinstance( measure, chord.Chord ):
         # find the label
         theLabel = labelThisChord( whatKey, measure, theSettings.parsePropertyGet( 'chordLabelVerbosity' ) )
         # if needed, put label on the actual score
         if False == theSettings.parsePropertyGet( 'annotateChordifiedScore' ):
            # NOTE: this is the same algorithm as just below, except here:
            #    measureOffset = theChords.offset
            #    offsetOfChord = measure.offset
            measureOffset = theChords.offset
            offsetOfChord = measure.offset
            try:
               # Sometimes, we get more than one thing with the same offset,
               # like if there is an Instrument at the beginning of the Part.
               # Usually this will just stop after 0.
               i = 0
               annotated = False
               while not annotated:
                  # thisOne will be set to the the i-th element at the offset
                  # of our target measure in the real score
                  thisOne = theScore[indexOfBassPart].getElementsByOffset( measureOffset )[i]
                  # If the i-th element is a Measure, we can find the
                  # Chord in it, and anootate it.
                  if isinstance( thisOne, stream.Measure ):
                     # find the chord at the proper offset
                     thisOne.getElementsByOffset( offsetOfChord )[0].lyric = theLabel
                     annotated = True
                  elif i > 10:
                     annotated = True
                  else:
                     i += 1
            except stream.StreamException as e:
               print( "analyzeThis(): Couldn't annotate measure with offset " + str(measureOffset) + ", chord offset " + str(offsetOfChord) )
               print( "   " + str(e) )
         else: # otherwise label goes on the chordified score
            measure.lyric = theLabel
      elif isinstance( measure, stream.Measure ):
         for harmony in measure:
            if isinstance( harmony, chord.Chord ):
               # find the label
               theLabel = labelThisChord( whatKey, harmony, theSettings.parsePropertyGet( 'chordLabelVerbosity' ) )
               # if needed, put label on the actual score
               if False == theSettings.parsePropertyGet( 'annotateChordifiedScore' ):
                  # NOTE: this is the same algorithm as just below, except here:
                  #    measureOffset = measure.offset
                  #    offsetOfChord = harmony.offset
                  measureOffset = measure.offset
                  offsetOfChord = harmony.offset
                  try:
                     # Sometimes, we get more than one thing with the same offset,
                     # like if there is an Instrument at the beginning of the Part.
                     # Usually this will just stop after 0.
                     i = 0
                     annotated = False
                     while not annotated:
                        # thisOne will be set to the the i-th element at the offset
                        # of our target measure in the real score
                        thisOne = theScore[indexOfBassPart].getElementsByOffset( measureOffset )[i]
                        # If the i-th element is a Measure, we can find the
                        # Chord in it, and anootate it.
                        if isinstance( thisOne, stream.Measure ):
                           # find the chord at the proper offset
                           thisOne.getElementsByOffset( offsetOfChord )[0].lyric = theLabel
                           annotated = True
                        elif i > 10:
                           annotated = True
                        else:
                           i += 1
                  except stream.StreamException as e:
                     print( "analyzeThis(): Couldn't annotate measure with offset " + str(measureOffset) + ", chord offset " + str(offsetOfChord) )
                     print( "   " + str(e) )
               else: # otherwise label goes on the chordified score
                  harmony.lyric = theLabel
   #
   
   print( "Processing score for display." )
   # output the score!
   if False == theSettings.parsePropertyGet( 'annotateChordifiedScore' ):
      theScore.show()
   else:
      theChords.show()
# End function analyzeThis() ---------------------------------------------------



# Class: HarrisonHarmonySettings ----------------------------------------------
class HarrisonHarmonySettings:
   # An internal class that holds settings for stuff.
   # 
   # _chordLabelVerbosity = 'concise' or 'verbose' that will be given to
   #        labelThisChord()
   # 
   # NOTE: When you add a property, remember to test its default setting in
   # the unit test file.
   def __init__( self ):
      self._chordLabelVerbosity = 'concise'
      self._annotateChordifiedScore = False
   
   def parsePropertySet( self, propertyStr ):
      # Parses 'propertyStr' and sets the specified property to the specified
      # value. Might later raise an exception if the property doesn't exist or
      # if the value is invalid.
      # 
      # Examples:
      # a.parsePropertySet( 'chordLabelVerbosity concise' )
      # a.parsePropertySet( 'set chordLabelVerbosity concise' )
      
      # if the str starts with "set " then remove that
      if len(propertyStr) < 4:
         pass # panic
      elif 'set ' == propertyStr[:4]:
         propertyStr = propertyStr[4:]
      
      # check to make sure there's a property and a value
      spaceIndex = propertyStr.find(' ')
      if -1 == spaceIndex:
         pass #panic
      
      # now match the property
      if 'chordLabelVerbosity' == propertyStr[:spaceIndex]:
         if 'verbose' == propertyStr[spaceIndex+1:] or 'concise' == propertyStr[spaceIndex+1:]:
            self._chordLabelVerbosity = propertyStr[spaceIndex+1:]
         else: # invalid setting
            raise NonsensicalInputError( "Invalid value for 'chordLabelVerbosity': " + propertyStr[spaceIndex+1:] )
      elif 'annotateChordifiedScore' == propertyStr[:spaceIndex]:
         if 'True' == propertyStr[spaceIndex+1:] or 'true' == propertyStr[spaceIndex+1:]:
            self._annotateChordifiedScore = True
         elif 'False' == propertyStr[spaceIndex+1:] or 'false' == propertyStr[spaceIndex+1:]:
            self._annotateChordifiedScore = False
         else: # invalid setting
            raise NonsensicalInputError( "Invalid value for 'chordLabelVerbosity': " + propertyStr[spaceIndex+1:] )
      # unrecognized property
      else:
         raise NonsensicalInputError( "Unrecognized property: " + propertyStr )
   
   def parsePropertyGet( self, propertyStr ):
      # Parses 'propertyStr' and returns the value of the specified property.
      # Might later raise an exception if the property doesn't exist.
      # 
      # Examples:
      # a.parsePropertyGet( 'chordLabelVerbosity' )
      # a.parsePropertyGet( 'get chordLabelVerbosity' )
      
      # if the str starts with "get " then remove that
      if len(propertyStr) < 4:
         pass # panic
      elif 'get ' == propertyStr[:4]:
         propertyStr = propertyStr[4:]
      
      # now match the property
      if 'chordLabelVerbosity' == propertyStr:
         return self._chordLabelVerbosity
      elif 'annotateChordifiedScore' == propertyStr:
         return self._annotateChordifiedScore
      # unrecognized property
      else:
         raise NonsensicalInputError( "Unrecognized property: " + propertyStr )
# End Class: HarrisonHarmonySettings ------------------------------------------



# "main" function --------------------------------------------------------------
# TODO: write the GPL-specified blurb here, and implemenet the commands, as specified at the end of the licence
if __name__ == '__main__':
   print( "harrisonHarmony" )
   print( "===============" )
   print( "For a list of commands, type \"help\"," )
   print( "or input the filename of a score to analyze." )
   
   mySettings = HarrisonHarmonySettings()
   exitProgram = False
   
   # See which command they wanted
   while False == exitProgram:
      userSays = raw_input( "hH @: " )
      # help
      if 'help' == userSays:
         print( "\nList of Commands:" )
         print( "-----------------" )
         print( "- 'exit' or 'quit' to exit or quit the program" )
         print( "- 'set' to set an option (see 'set help' for more information)" )
         print( "- 'get' to get the setting of an option (see 'get help')" )
         print( "" )
      elif 'exit' == userSays or 'quit' == userSays:
         print( "" )
         exitProgram = True
      # multi-word commands
      elif 0 < userSays.find(' '):
         if 'set' == userSays[:userSays.find(' ')]:
            if 'set help' == userSays:
               pass # TODO: print set help
            else:
               try:
                  mySettings.parsePropertySet( userSays )
               except NonsensicalInputError as e:
                  print( "Error: " + str(e) )
         elif 'get' == userSays[:userSays.find(' ')]:
            if 'get help' == userSays:
               pass # TODO: print get help
            else:
               try:
                  val = mySettings.parsePropertyGet( userSays )
                  print( val )
               except NonsensiclaInputError as e:
                  print( "Error: " + str(e) )
      else:
         if pathExists( userSays ):
            print( "Loading " + userSays + " for analysis." )
            try:
               analyzeThis( userSays, mySettings )
            except ConverterException as e:
               print( "--> musc21 Error: " + str(e) )
            except ConverterFileException as e:
               print( "--> musc21 Error: " + str(e) )
            except NonsensicalInputError as e:
               print( "--> Error from analyzeThis(): " + str(e) )
         else:
            print( "File doesn't seem to exist (" + userSays + ")" )
# End "main" function ----------------------------------------------------------































