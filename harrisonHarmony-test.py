#! /usr/bin/python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:         harrisonHarmony.py
# Purpose:      music21-compatible classes for performing and presenting an
#               analysis in the style of Daniel Harrison (1994)
#
# Authors:      Christopher Antila
#
# Copyright:    (c) 2012 The music21 Project
# License:      GPL v 3.0
#-------------------------------------------------------------------------------

import unittest
from harrisonHarmony import *

## Import required libraries (this list is from the module)
from music21 import pitch # confirmed requirement
from music21 import scale
from music21 import interval # confirmed requirement
from music21 import key # confirmed requirement
from music21 import chord
from music21 import converter
from music21 import analysis
from music21 import stream
from music21 import note # confirmed requirement
# TODO: Quadruple-fun check that these are all that's required.

#-------------------------------------------------------------------------------
class TestChromaticScaleDegree( unittest.TestCase ):
   def chkExp( self, theDegree, theKey, theNote ):
         self.assertEqual( chromaticScaleDegree( key.Key( theKey ), pitch.Pitch( theNote ) ), theDegree )
   
   def test_C_tonic( self ):
      self.chkExp( '7', 'C', 'B' )
      self.chkExp( '6', 'C', 'A' )
      self.chkExp( '5', 'C', 'G' )
      self.chkExp( '4', 'C', 'F' )
      self.chkExp( '3', 'C', 'E' )
      self.chkExp( '2', 'C', 'D' )
      self.chkExp( '1', 'C', 'C' )
      # flat scale degrees
      self.chkExp( '-7', 'C', 'B-' )
      self.chkExp( '-6', 'C', 'A-' )
      self.chkExp( '-5', 'C', 'G-' )
      self.chkExp( '-4', 'C', 'F-' )
      self.chkExp( '-3', 'C', 'E-' )
      self.chkExp( '-2', 'C', 'D-' )
      self.chkExp( '-1', 'C', 'C-' )
      # sharp scale degrees
      self.chkExp( '#7', 'C', 'B#' )
      self.chkExp( '#6', 'C', 'A#' )
      self.chkExp( '#5', 'C', 'G#' )
      self.chkExp( '#4', 'C', 'F#' )
      self.chkExp( '#3', 'C', 'E#' )
      self.chkExp( '#2', 'C', 'D#' )
      self.chkExp( '#1', 'C', 'C#' )
      # double-flat scale degrees
      self.chkExp( '--7', 'C', 'B--' )
      self.chkExp( '--6', 'C', 'A--' )
      self.chkExp( '--5', 'C', 'G--' )
      self.chkExp( '--4', 'C', 'F--' )
      self.chkExp( '--3', 'C', 'E--' )
      self.chkExp( '--2', 'C', 'D--' )
      self.chkExp( '--1', 'C', 'C--' )
      # double-sharp scale degrees
      self.chkExp( '##7', 'C', 'B##' )
      self.chkExp( '##6', 'C', 'A##' )
      self.chkExp( '##5', 'C', 'G##' )
      self.chkExp( '##4', 'C', 'F##' )
      self.chkExp( '##3', 'C', 'E##' )
      self.chkExp( '##2', 'C', 'D##' )
      self.chkExp( '##1', 'C', 'C##' )
      
   def test_D_tonic( self ):
      tonic = 'D'
      self.chkExp( '7', tonic, 'C#' )
      self.chkExp( '6', tonic, 'B' )
      self.chkExp( '5', tonic, 'A' )
      self.chkExp( '4', tonic, 'G' )
      self.chkExp( '3', tonic, 'F#' )
      self.chkExp( '2', tonic, 'E' )
      self.chkExp( '1', tonic, 'D' )
      # flat scale degrees
      self.chkExp( '-7', tonic, 'C' )
      self.chkExp( '-6', tonic, 'B-' )
      self.chkExp( '-5', tonic, 'A-' )
      self.chkExp( '-4', tonic, 'G-' )
      self.chkExp( '-3', tonic, 'F' )
      self.chkExp( '-2', tonic, 'E-' )
      self.chkExp( '-1', tonic, 'D-' )
      # sharp scale degrees
      self.chkExp( '#7', tonic, 'C##' )
      self.chkExp( '#6', tonic, 'B#' )
      self.chkExp( '#5', tonic, 'A#' )
      self.chkExp( '#4', tonic, 'G#' )
      self.chkExp( '#3', tonic, 'F##' )
      self.chkExp( '#2', tonic, 'E#' )
      self.chkExp( '#1', tonic, 'D#' )
      # double-flat scale degrees
      self.chkExp( '--7', tonic, 'C-' )
      self.chkExp( '--6', tonic, 'B--' )
      self.chkExp( '--5', tonic, 'A--' )
      self.chkExp( '--4', tonic, 'G--' )
      self.chkExp( '--3', tonic, 'F-' )
      self.chkExp( '--2', tonic, 'E--' )
      self.chkExp( '--1', tonic, 'D--' )
      # double-sharp scale degrees
      self.chkExp( '##7', tonic, 'C###' )
      self.chkExp( '##6', tonic, 'B##' )
      self.chkExp( '##5', tonic, 'A##' )
      self.chkExp( '##4', tonic, 'G##' )
      self.chkExp( '##3', tonic, 'F###' )
      self.chkExp( '##2', tonic, 'E##' )
      self.chkExp( '##1', tonic, 'D##' )
      
   def test_E_tonic( self ):
      tonic = 'E-'
      self.chkExp( '7', tonic, 'D' )
      self.chkExp( '6', tonic, 'C' )
      self.chkExp( '5', tonic, 'B-' )
      self.chkExp( '4', tonic, 'A-' )
      self.chkExp( '3', tonic, 'G' )
      self.chkExp( '2', tonic, 'F' )
      self.chkExp( '1', tonic, 'E-' )
      # flat scale degrees
      self.chkExp( '-7', tonic, 'D-' )
      self.chkExp( '-6', tonic, 'C-' )
      self.chkExp( '-5', tonic, 'B--' )
      self.chkExp( '-4', tonic, 'A--' )
      self.chkExp( '-3', tonic, 'G-' )
      self.chkExp( '-2', tonic, 'F-' )
      self.chkExp( '-1', tonic, 'E--' )
      # sharp scale degrees
      self.chkExp( '#7', tonic, 'D#' )
      self.chkExp( '#6', tonic, 'C#' )
      self.chkExp( '#5', tonic, 'B' )
      self.chkExp( '#4', tonic, 'A' )
      self.chkExp( '#3', tonic, 'G#' )
      self.chkExp( '#2', tonic, 'F#' )
      self.chkExp( '#1', tonic, 'E' )
      # double-flat scale degrees
      self.chkExp( '--7', tonic, 'D--' )
      self.chkExp( '--6', tonic, 'C--' )
      self.chkExp( '--5', tonic, 'B---' )
      self.chkExp( '--4', tonic, 'A---' )
      self.chkExp( '--3', tonic, 'G--' )
      self.chkExp( '--2', tonic, 'F--' )
      self.chkExp( '--1', tonic, 'E---' )
      # double-sharp scale degrees
      self.chkExp( '##7', tonic, 'D##' )
      self.chkExp( '##6', tonic, 'C##' )
      self.chkExp( '##5', tonic, 'B#' )
      self.chkExp( '##4', tonic, 'A#' )
      self.chkExp( '##3', tonic, 'G##' )
      self.chkExp( '##2', tonic, 'F##' )
      self.chkExp( '##1', tonic, 'E#' )
      
   def test_Csharp_tonic( self ):
      self.chkExp( '7', 'C#', 'B#' )
      self.chkExp( '6', 'C#', 'A#' )
      self.chkExp( '5', 'C#', 'G#' )
      self.chkExp( '4', 'C#', 'F#' )
      self.chkExp( '3', 'C#', 'E#' )
      self.chkExp( '2', 'C#', 'D#' )
      self.chkExp( '1', 'C#', 'C#' )
      # flat scale degrees
      self.chkExp( '-7', 'C#', 'B' )
      self.chkExp( '-6', 'C#', 'A' )
      self.chkExp( '-5', 'C#', 'G' )
      self.chkExp( '-4', 'C#', 'F' )
      self.chkExp( '-3', 'C#', 'E' )
      self.chkExp( '-2', 'C#', 'D' )
      self.chkExp( '-1', 'C#', 'C' )
      # sharp scale degrees
      self.chkExp( '#7', 'C#', 'B##' )
      self.chkExp( '#6', 'C#', 'A##' )
      self.chkExp( '#5', 'C#', 'G##' )
      self.chkExp( '#4', 'C#', 'F##' )
      self.chkExp( '#3', 'C#', 'E##' )
      self.chkExp( '#2', 'C#', 'D##' )
      self.chkExp( '#1', 'C#', 'C##' )
      # double-flat scale degrees
      self.chkExp( '--7', 'C#', 'B-' )
      self.chkExp( '--6', 'C#', 'A-' )
      self.chkExp( '--5', 'C#', 'G-' )
      self.chkExp( '--4', 'C#', 'F-' )
      self.chkExp( '--3', 'C#', 'E-' )
      self.chkExp( '--2', 'C#', 'D-' )
      self.chkExp( '--1', 'C#', 'C-' )
      # double-sharp scale degrees
      self.chkExp( '##7', 'C#', 'B###' )
      self.chkExp( '##6', 'C#', 'A###' )
      self.chkExp( '##5', 'C#', 'G###' )
      self.chkExp( '##4', 'C#', 'F###' )
      self.chkExp( '##3', 'C#', 'E###' )
      self.chkExp( '##2', 'C#', 'D###' )
      self.chkExp( '##1', 'C#', 'C###' )
      
   def test_Cflat_tonic( self ):
      tonic = 'C-'
      self.chkExp( '7', tonic, 'B-' )
      self.chkExp( '6', tonic, 'A-' )
      self.chkExp( '5', tonic, 'G-' )
      self.chkExp( '4', tonic, 'F-' )
      self.chkExp( '3', tonic, 'E-' )
      self.chkExp( '2', tonic, 'D-' )
      self.chkExp( '1', tonic, 'C-' )
      # flat scale degrees
      self.chkExp( '-7', tonic, 'B--' )
      self.chkExp( '-6', tonic, 'A--' )
      self.chkExp( '-5', tonic, 'G--' )
      self.chkExp( '-4', tonic, 'F--' )
      self.chkExp( '-3', tonic, 'E--' )
      self.chkExp( '-2', tonic, 'D--' )
      self.chkExp( '-1', tonic, 'C--' )
      # sharp scale degrees
      self.chkExp( '#7', tonic, 'B' )
      self.chkExp( '#6', tonic, 'A' )
      self.chkExp( '#5', tonic, 'G' )
      self.chkExp( '#4', tonic, 'F' )
      self.chkExp( '#3', tonic, 'E' )
      self.chkExp( '#2', tonic, 'D' )
      self.chkExp( '#1', tonic, 'C' )
      # double-flat scale degrees
      self.chkExp( '--7', tonic, 'B---' )
      self.chkExp( '--6', tonic, 'A---' )
      self.chkExp( '--5', tonic, 'G---' )
      self.chkExp( '--4', tonic, 'F---' )
      self.chkExp( '--3', tonic, 'E---' )
      self.chkExp( '--2', tonic, 'D---' )
      self.chkExp( '--1', tonic, 'C---' )
      # double-sharp scale degrees
      self.chkExp( '##7', tonic, 'B#' )
      self.chkExp( '##6', tonic, 'A#' )
      self.chkExp( '##5', tonic, 'G#' )
      self.chkExp( '##4', tonic, 'F#' )
      self.chkExp( '##3', tonic, 'E#' )
      self.chkExp( '##2', tonic, 'D#' )
      self.chkExp( '##1', tonic, 'C#' )
   
   def test_variety_of_input( self ):
      theKey = "C"
      theDegree = '1'
      ## Pitch ##
      # Pitch and no register
      self.assertEqual( chromaticScaleDegree( key.Key( theKey ), pitch.Pitch( 'C' ) ), theDegree )
      # Pitch and same register
      self.assertEqual( chromaticScaleDegree( key.Key( theKey ), pitch.Pitch( 'C4' ) ), theDegree )
      # Pitch and second self.higher
      self.assertEqual( chromaticScaleDegree( key.Key( theKey ), pitch.Pitch( 'C5' ) ), theDegree )
      # Pitch and second self.lower
      self.assertEqual( chromaticScaleDegree( key.Key( theKey ), pitch.Pitch( 'C3' ) ), theDegree )
      # Pitch and second much self.higher
      self.assertEqual( chromaticScaleDegree( key.Key( theKey ), pitch.Pitch( 'C20' ) ), theDegree )
      # Pitch and second much self.lower
      self.assertEqual( chromaticScaleDegree( key.Key( theKey ), pitch.Pitch( 'C0' ) ), theDegree )
      ## Note ##
      # Note and no register
      self.assertEqual( chromaticScaleDegree( key.Key( theKey ), note.Note( 'C' ) ), theDegree )
      # Note and same register
      self.assertEqual( chromaticScaleDegree( key.Key( theKey ), note.Note( 'C4' ) ), theDegree )
      # Note and second self.higher
      self.assertEqual( chromaticScaleDegree( key.Key( theKey ), note.Note( 'C5' ) ), theDegree )
      # Note and second self.lower
      self.assertEqual( chromaticScaleDegree( key.Key( theKey ), note.Note( 'C3' ) ), theDegree )
      # Note and second much self.higher
      self.assertEqual( chromaticScaleDegree( key.Key( theKey ), note.Note( 'C20' ) ), theDegree )
      # Note and second much self.lower
      self.assertEqual( chromaticScaleDegree( key.Key( theKey ), note.Note( 'C0' ) ), theDegree )
      
      #### Minor Mode ####
      theKey = "c"
      ## Pitch ##
      # Pitch and no register
      self.assertEqual( chromaticScaleDegree( key.Key( theKey ), pitch.Pitch( 'C' ) ), theDegree )
      # Pitch and same register
      self.assertEqual( chromaticScaleDegree( key.Key( theKey ), pitch.Pitch( 'C4' ) ), theDegree )
      # Pitch and second self.higher
      self.assertEqual( chromaticScaleDegree( key.Key( theKey ), pitch.Pitch( 'C5' ) ), theDegree )
      # Pitch and second self.lower
      self.assertEqual( chromaticScaleDegree( key.Key( theKey ), pitch.Pitch( 'C3' ) ), theDegree )
      # Pitch and second much self.higher
      self.assertEqual( chromaticScaleDegree( key.Key( theKey ), pitch.Pitch( 'C20' ) ), theDegree )
      # Pitch and second much self.lower
      self.assertEqual( chromaticScaleDegree( key.Key( theKey ), pitch.Pitch( 'C0' ) ), theDegree )
      ## Note ##
      # Note and no register
      self.assertEqual( chromaticScaleDegree( key.Key( theKey ), note.Note( 'C' ) ), theDegree )
      # Note and same register
      self.assertEqual( chromaticScaleDegree( key.Key( theKey ), note.Note( 'C4' ) ), theDegree )
      # Note and second self.higher
      self.assertEqual( chromaticScaleDegree( key.Key( theKey ), note.Note( 'C5' ) ), theDegree )
      # Note and second self.lower
      self.assertEqual( chromaticScaleDegree( key.Key( theKey ), note.Note( 'C3' ) ), theDegree )
      # Note and second much self.higher
      self.assertEqual( chromaticScaleDegree( key.Key( theKey ), note.Note( 'C20' ) ), theDegree )
      # Note and second much self.lower
      self.assertEqual( chromaticScaleDegree( key.Key( theKey ), note.Note( 'C0' ) ), theDegree )
      
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
class TestHarmonicFunction( unittest.TestCase ):
   def test_toLetter( self ):
      self.assertEqual( HarmonicFunction.toLetter( HarmonicFunction.Subdominant ), 'S' )
      self.assertEqual( HarmonicFunction.toLetter( HarmonicFunction.Tonic ), 'T' )
      self.assertEqual( HarmonicFunction.toLetter( HarmonicFunction.Dominant ), 'D' )
      self.assertEqual( HarmonicFunction.toLetter( HarmonicFunction.Unknown ), 'U' )
      self.assertRaises( NonsensicalInputError, HarmonicFunction.toLetter, 'argh' )
   
   def test_str( self ):
      self.assertEqual( str(HarmonicFunction.Subdominant()), 'Subdominant' )
      self.assertEqual( str(HarmonicFunction.Tonic()), 'Tonic' )
      self.assertEqual( str(HarmonicFunction.Dominant()), 'Dominant' )
      self.assertEqual( str(HarmonicFunction.Unknown()), 'Unknown function' )
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
class TestFunctionalRole( unittest.TestCase ):
   def test_toLetter( self ):
      self.assertEqual( FunctionalRole.toLetter( FunctionalRole.Base ), 'ba' )
      self.assertEqual( FunctionalRole.toLetter( FunctionalRole.Agent ), 'ag' )
      self.assertEqual( FunctionalRole.toLetter( FunctionalRole.Associate ), 'as' )
      self.assertEqual( FunctionalRole.toLetter( FunctionalRole.Unknown ), 'un' )
      self.assertRaises( NonsensicalInputError, FunctionalRole.toLetter, key.Key('D-') )
   
   def test_str( self ):
      self.assertEqual( str(FunctionalRole.Base()), 'base' )
      self.assertEqual( str(FunctionalRole.Agent()), 'agent' )
      self.assertEqual( str(FunctionalRole.Associate()), 'associate' )
      self.assertEqual( str(FunctionalRole.Unknown()), 'unknown role' )
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
class TestRelativeVoicePosition( unittest.TestCase ):
   def test_toLetter( self ):
      self.assertEqual( RelativeVoicePosition.toLetter( RelativeVoicePosition.Highest ), 'highest' )
      self.assertEqual( RelativeVoicePosition.toLetter( RelativeVoicePosition.Middle ), 'middle' )
      self.assertEqual( RelativeVoicePosition.toLetter( RelativeVoicePosition.Lowest ), 'lowest' )
      self.assertEqual( RelativeVoicePosition.toLetter( RelativeVoicePosition.Solo ), 'solo' )
      self.assertRaises( NonsensicalInputError, RelativeVoicePosition.toLetter, 42 )
   
   def test_str( self ):
      self.assertEqual( str(RelativeVoicePosition.Highest()), 'highest' )
      self.assertEqual( str(RelativeVoicePosition.Middle()), 'middle' )
      self.assertEqual( str(RelativeVoicePosition.Lowest()), 'lowest' )
      self.assertEqual( str(RelativeVoicePosition.Solo()), 'solo' )
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
class TestConditionForFunction( unittest.TestCase ):
   def test_str( self ):
      self.assertEqual( str(ConditionForFunction( ConditionForFunction.IsGuaranteed, '' )), 'guaranteed' )
      self.assertEqual( str(ConditionForFunction( ConditionForFunction.IsLowestVoice, 'A' )), 'true if lowest voice is A' )
      self.assertEqual( str(ConditionForFunction( ConditionForFunction.IsPresent, 'B' )), 'true in presence of B' )
   
   def test_equal_contingencies( self ):
      a = ConditionForFunction( ConditionForFunction.IsGuaranteed, 'A' )
      b = ConditionForFunction( ConditionForFunction.IsLowestVoice, 'B' )
      c = ConditionForFunction( ConditionForFunction.IsPresent, 'C' )
      self.assertTrue( a.equal( a ) )
      self.assertTrue( b.equal( b ) )
      self.assertTrue( c.equal( c ) )
      self.assertEqual( a.equal( b ), False )
      self.assertEqual( b.equal( a ), False )
      self.assertEqual( a.equal( c ), False )
      self.assertEqual( c.equal( a ), False )
      self.assertEqual( b.equal( c ), False )
      self.assertEqual( c.equal( b ), False )
   
   def test_equal_dependencies_with_str( self ):
      # These are different but should be considered equal because there's no
      # situation where the function is guaranteed and the dependency is ever checked.
      a = ConditionForFunction( ConditionForFunction.IsGuaranteed, 'A' )
      b = ConditionForFunction( ConditionForFunction.IsGuaranteed, 'B' )
      self.assertTrue( a.equal( b ), False )
      self.assertTrue( b.equal( a ), False )
      # But these should not be considered equal.
      a = ConditionForFunction( ConditionForFunction.IsLowestVoice, 'A' )
      b = ConditionForFunction( ConditionForFunction.IsLowestVoice, 'B' )
      self.assertEqual( a.equal( b ), False )
      self.assertEqual( b.equal( a ), False )
   
   def test_equal_dependencies_with_HarFuncNote( self ):
      # And we have to test that it works with HarmonicFunctionalNote objects, too.
      a = ConditionForFunction( ConditionForFunction.IsLowestVoice, HarmonicFunctionalNote( key.Key('C'), HarmonicFunction.Tonic, FunctionalRole.Base, '1' ) )
      b = ConditionForFunction( ConditionForFunction.IsLowestVoice, HarmonicFunctionalNote( key.Key('C'), HarmonicFunction.Tonic, FunctionalRole.Base, '1' ) )
      self.assertTrue( a.equal( b ) )
      self.assertTrue( b.equal( a ) )
      a = ConditionForFunction( ConditionForFunction.IsLowestVoice, HarmonicFunctionalNote( key.Key('C'), HarmonicFunction.Tonic, FunctionalRole.Base, '1' ) )
      b = ConditionForFunction( ConditionForFunction.IsLowestVoice, HarmonicFunctionalNote( key.Key('C'), HarmonicFunction.Tonic, FunctionalRole.Agent, '3' ) )
      self.assertEqual( a.equal( b ), False )
      self.assertEqual( b.equal( a ), False )
      a = ConditionForFunction( ConditionForFunction.IsLowestVoice, HarmonicFunctionalNote( key.Key('C'), HarmonicFunction.Tonic, FunctionalRole.Base, '1' ) )
      b = ConditionForFunction( ConditionForFunction.IsPresent, HarmonicFunctionalNote( key.Key('C'), HarmonicFunction.Tonic, FunctionalRole.Agent, '-3' ) )
      self.assertEqual( a.equal( b ), False )
      self.assertEqual( b.equal( a ), False )
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
class TestHarmonicFunctionalNote( unittest.TestCase ):
   def test_str( self ):
      self.assertEqual( str(HarmonicFunctionalNote( key.Key('c'), HarmonicFunction.Tonic, FunctionalRole.Agent, '3' )), '^3 as Tonic agent in C' )
      self.assertEqual( str(HarmonicFunctionalNote( key.Key('c'), HarmonicFunction.Tonic, FunctionalRole.Agent, '-3' )), '^-3 as Tonic agent in C' )
      self.assertEqual( str(HarmonicFunctionalNote( key.Key('C'), HarmonicFunction.Tonic, FunctionalRole.Agent, '3' )), '^3 as Tonic agent in C' )
      self.assertEqual( str(HarmonicFunctionalNote( key.Key('c'), HarmonicFunction.Subdominant, FunctionalRole.Associate, '1' )), '^1 as Subdominant associate in C' )
      self.assertEqual( str(HarmonicFunctionalNote( key.Key('c#'), HarmonicFunction.Tonic, FunctionalRole.Agent, '3' )), '^3 as Tonic agent in C#' )
      self.assertEqual( str(HarmonicFunctionalNote( key.Key('c#'), HarmonicFunction.Tonic, FunctionalRole.Agent, '-3' )), '^-3 as Tonic agent in C#' )
      self.assertEqual( str(HarmonicFunctionalNote( key.Key('C#'), HarmonicFunction.Tonic, FunctionalRole.Agent, '3' )), '^3 as Tonic agent in C#' )
      self.assertEqual( str(HarmonicFunctionalNote( key.Key('C#'), HarmonicFunction.Tonic, FunctionalRole.Agent, '-3' )), '^-3 as Tonic agent in C#' )
   
   def test_getLabel( self ):
      a = HarmonicFunctionalNote( key.Key( 'D-' ), HarmonicFunction.Subdominant, FunctionalRole.Associate, '1' )
      self.assertEqual( a.getLabel(), 'D-:Sas' )
      a = HarmonicFunctionalNote( key.Key( 'F' ), HarmonicFunction.Unknown, FunctionalRole.Unknown, '-4' )
      self.assertEqual( a.getLabel(), 'F:Uun' )
      a = HarmonicFunctionalNote( key.Key( 'F#' ), HarmonicFunction.Tonic, FunctionalRole.Agent, '3' )
      self.assertEqual( a.getLabel(), 'F#:Tag' )
      a = HarmonicFunctionalNote( key.Key( 'E' ), HarmonicFunction.Dominant, FunctionalRole.Base, '5' )
      self.assertEqual( a.getLabel(), 'E:Dba' )
   
   def test_equal( self ):
      # HFNs are the same
      a = HarmonicFunctionalNote( key.Key( 'F#' ), HarmonicFunction.Dominant, FunctionalRole.Agent, '7' )
      b = HarmonicFunctionalNote( key.Key( 'F#' ), HarmonicFunction.Dominant, FunctionalRole.Agent, '7' )
      self.assertTrue( a.equal( b ) )
      self.assertTrue( b.equal( a ) )
      # scale degree is different
      b = HarmonicFunctionalNote( key.Key( 'F#' ), HarmonicFunction.Dominant, FunctionalRole.Agent, '-7' )
      self.assertEqual( a.equal( b ), False )
      self.assertEqual( b.equal( a ), False )
      # role is different
      b = HarmonicFunctionalNote( key.Key( 'F#' ), HarmonicFunction.Dominant, FunctionalRole.Base, '-7' )
      self.assertEqual( a.equal( b ), False )
      self.assertEqual( b.equal( a ), False )
      # function is different
      b = HarmonicFunctionalNote( key.Key( 'F#' ), HarmonicFunction.Tonic, FunctionalRole.Agent, '-7' )
      self.assertEqual( a.equal( b ), False )
      self.assertEqual( b.equal( a ), False )
      # if the key is a different mode, they should still be equal
      b = HarmonicFunctionalNote( key.Key( 'f#' ), HarmonicFunction.Dominant, FunctionalRole.Agent, '7' )
      self.assertTrue( a.equal( b ) )
      self.assertTrue( b.equal( a ) )
#-------------------------------------------------------------------------------   



#-------------------------------------------------------------------------------   
class TestHarmonicFunctionalChord( unittest.TestCase ):
   def setUp( self ):
      self.T = HarmonicFunction.Tonic
      self.S = HarmonicFunction.Subdominant
      self.D = HarmonicFunction.Dominant
      self.U = HarmonicFunction.Unknown
      self.bas = FunctionalRole.Base
      self.age = FunctionalRole.Agent
      self.ass = FunctionalRole.Associate
      self.unk = FunctionalRole.Unknown
   
   def test_init( self ):
      #def __init__( self, bassFunction, otherFunctions = [], theKey = None ):
      #with no argument for otherFunctions
      CM = key.Key( 'C' )
      a = HarmonicFunctionalNote( CM, HarmonicFunction.Tonic, FunctionalRole.Base, '1' )
      b = HarmonicFunctionalNote( CM, HarmonicFunction.Tonic, FunctionalRole.Agent, '3' )
      c = HarmonicFunctionalNote( CM, HarmonicFunction.Tonic, FunctionalRole.Associate, '5' )
      tester = HarmonicFunctionalChord( a, [b, c, a], CM )
      self.assertEqual( tester.getKey(), CM )
      self.assertEqual( tester.getBassFunctionalNote(), a )
      self.assertEqual( tester.getOtherFunctionalNotes(), [b, c, a] )
      self.assertEqual( tester.getFunctionalNotes(), [a, b, c, a] )
      tester = HarmonicFunctionalChord( a, [b,c,a] )
      self.assertEqual( tester.getKey(), CM )
      self.assertEqual( tester.getBassFunctionalNote(), a )
      self.assertEqual( tester.getOtherFunctionalNotes(), [b, c, a] )
      self.assertEqual( tester.getFunctionalNotes(), [a, b, c, a] )
      tester = HarmonicFunctionalChord( a )
      self.assertEqual( tester.getKey(), CM )
      self.assertEqual( tester.getBassFunctionalNote(), a )
      self.assertEqual( tester.getOtherFunctionalNotes(), [] )
      self.assertEqual( tester.getFunctionalNotes(), [a] )
      tester = HarmonicFunctionalChord( a, theKey = CM )
      self.assertEqual( tester.getKey(), CM )
      self.assertEqual( tester.getBassFunctionalNote(), a )
      self.assertEqual( tester.getOtherFunctionalNotes(), [] )
      self.assertEqual( tester.getFunctionalNotes(), [a] )
   
   # __repr__
   # __str__
   # def getLabel( self ):
   def test_str( self ):
      CM = key.Key( 'C' )
      HFN = lambda a, b, c, d: HarmonicFunctionalNote( a, b, c, d )
      HFC = lambda a, b, c = None : HarmonicFunctionalChord( a, b, c )
      # the doc-tests
      a = HarmonicFunctionalNote( key.Key( 'C' ), HarmonicFunction.Tonic, FunctionalRole.Agent, '3' )
      b = HarmonicFunctionalNote( key.Key( 'C' ), HarmonicFunction.Tonic, FunctionalRole.Base, '1' )
      c = HarmonicFunctionalNote( key.Key( 'C' ), HarmonicFunction.Tonic, FunctionalRole.Associate, '5' )
      self.assertEqual( str(HarmonicFunctionalChord( b, [a, c, b] )), 'T(1)' )
      d = HarmonicFunctionalNote( key.Key( 'C' ), HarmonicFunction.Subdominant, FunctionalRole.Agent, '-6' )
      self.assertEqual( str(HarmonicFunctionalChord( d, [b, a, c] )), 'S^T(-6)' )
      a = b = c = d = None
      # end doc-tests
      # only Tonic
      self.assertEqual( "T(1)", str(HFC(HFN(CM,self.T,self.bas,'1'),[HFN(CM,self.T,self.age,'3'),HFN(CM,self.T,self.ass,'5')] ) ) )
      self.assertEqual( "T(1)", str(HFC(HFN(CM,self.T,self.bas,'1'),[HFN(CM,self.T,self.age,'4'),HFN(CM,self.T,self.bas,'1'),HFN(CM,self.T,self.ass,'5')] ) ) )
      self.assertEqual( "T(1)", str(HFC(HFN(CM,self.T,self.bas,'1'),[HFN(CM,self.T,self.age,'3')] ) ) )
      self.assertEqual( "T(1)", str(HFC(HFN(CM,self.T,self.bas,'1'),[HFN(CM,self.T,self.bas,'1')] ) ) )
      self.assertEqual( "T(1)", str(HFC(HFN(CM,self.T,self.bas,'1'),[] ) ) )
      self.assertEqual( "T(3)", str(HFC(HFN(CM,self.T,self.age,'3'),[HFN(CM,self.T,self.age,'3'),HFN(CM,self.T,self.ass,'5')] ) ) )
      self.assertEqual( "T(3)", str(HFC(HFN(CM,self.T,self.age,'3'),[HFN(CM,self.T,self.bas,'1'),HFN(CM,self.T,self.ass,'5')] ) ) )
      self.assertEqual( "T(3)", str(HFC(HFN(CM,self.T,self.age,'3'),[HFN(CM,self.T,self.bas,'1'),HFN(CM,self.T,self.age,'3')] ) ) )
      self.assertEqual( "T(3)", str(HFC(HFN(CM,self.T,self.age,'3'),[HFN(CM,self.T,self.age,'3'),HFN(CM,self.T,self.ass,'5'),HFN(CM,self.T,self.bas,'1')] ) ) )
      self.assertEqual( "T(3)", str(HFC(HFN(CM,self.T,self.age,'3'),[HFN(CM,self.T,self.bas,'1'),HFN(CM,self.T,self.bas,'1'),HFN(CM,self.T,self.ass,'5')] ) ) )
      # Dominant base with Tonic on top
      self.assertEqual( "D^T(5)", str(HFC(HFN(CM,self.D,self.bas,'5'),[HFN(CM,self.T,self.age,'3'),HFN(CM,self.T,self.bas,'1'),HFN(CM,self.T,self.ass,'5')] ) ) )
      self.assertEqual( "D^T(5)", str(HFC(HFN(CM,self.D,self.bas,'5'),[HFN(CM,self.T,self.age,'3'),HFN(CM,self.T,self.ass,'5')] ) ) )
      self.assertEqual( "D^T(5)", str(HFC(HFN(CM,self.D,self.bas,'5'),[HFN(CM,self.T,self.age,'3'),HFN(CM,self.T,self.bas,'1')] ) ) )
      self.assertEqual( "D^T(5)", str(HFC(HFN(CM,self.D,self.bas,'5'),[HFN(CM,self.T,self.age,'3')] ) ) )
      # only Subdominant
      self.assertEqual( "S(4)", str(HFC(HFN(CM,self.S,self.bas,'4'),[HFN(CM,self.S,self.age,'6'),HFN(CM,self.S,self.ass,'1')] ) ) )
      self.assertEqual( "S(4)", str(HFC(HFN(CM,self.S,self.bas,'4'),[HFN(CM,self.S,self.age,'6'),HFN(CM,self.S,self.bas,'4'),HFN(CM,self.S,self.ass,'1')] ) ) )
      self.assertEqual( "S(4)", str(HFC(HFN(CM,self.S,self.bas,'4'),[HFN(CM,self.S,self.age,'6')] ) ) )
      self.assertEqual( "S(4)", str(HFC(HFN(CM,self.S,self.bas,'4'),[HFN(CM,self.S,self.bas,'4')] ) ) )
      self.assertEqual( "S(4)", str(HFC(HFN(CM,self.S,self.bas,'4'),[] ) ) )
      self.assertEqual( "S(6)", str(HFC(HFN(CM,self.S,self.age,'6'),[HFN(CM,self.S,self.age,'6'),HFN(CM,self.S,self.ass,'1')] ) ) )
      self.assertEqual( "S(6)", str(HFC(HFN(CM,self.S,self.age,'6'),[HFN(CM,self.S,self.bas,'4'),HFN(CM,self.S,self.ass,'1')] ) ) )
      self.assertEqual( "S(6)", str(HFC(HFN(CM,self.S,self.age,'6'),[HFN(CM,self.S,self.bas,'4'),HFN(CM,self.S,self.age,'6')] ) ) )
      self.assertEqual( "S(6)", str(HFC(HFN(CM,self.S,self.age,'6'),[HFN(CM,self.S,self.age,'6'),HFN(CM,self.S,self.ass,'1'),HFN(CM,self.S,self.bas,'4')] ) ) )
      self.assertEqual( "S(6)", str(HFC(HFN(CM,self.S,self.age,'6'),[HFN(CM,self.S,self.bas,'4'),HFN(CM,self.S,self.bas,'4'),HFN(CM,self.S,self.ass,'1')] ) ) )
      # Tonic base with Subdominant on top
      self.assertEqual( "T^S(1)", str(HFC(HFN(CM,self.T,self.bas,'1'),[HFN(CM,self.S,self.age,'6'),HFN(CM,self.S,self.bas,'4'),HFN(CM,self.S,self.ass,'1')] ) ) )
      self.assertEqual( "T^S(1)", str(HFC(HFN(CM,self.T,self.bas,'1'),[HFN(CM,self.S,self.age,'6'),HFN(CM,self.S,self.ass,'1')] ) ) )
      self.assertEqual( "T^S(1)", str(HFC(HFN(CM,self.T,self.bas,'1'),[HFN(CM,self.S,self.age,'6'),HFN(CM,self.S,self.bas,'4')] ) ) )
      self.assertEqual( "T^S(1)", str(HFC(HFN(CM,self.T,self.bas,'1'),[HFN(CM,self.S,self.age,'6')] ) ) )
      # only Dominant
      self.assertEqual( "D(5)", str(HFC(HFN(CM,self.D,self.bas,'5'),[HFN(CM,self.D,self.age,'7'),HFN(CM,self.D,self.ass,'2')] ) ) )
      self.assertEqual( "D(5)", str(HFC(HFN(CM,self.D,self.bas,'5'),[HFN(CM,self.D,self.age,'7'),HFN(CM,self.D,self.bas,'5'),HFN(CM,self.D,self.ass,'2')] ) ) )
      self.assertEqual( "D(5)", str(HFC(HFN(CM,self.D,self.bas,'5'),[HFN(CM,self.D,self.age,'7')] ) ) )
      self.assertEqual( "D(5)", str(HFC(HFN(CM,self.D,self.bas,'5'),[HFN(CM,self.D,self.bas,'5')] ) ) )
      self.assertEqual( "D(5)", str(HFC(HFN(CM,self.D,self.bas,'5'),[] ) ) )
      self.assertEqual( "D(7)", str(HFC(HFN(CM,self.D,self.age,'7'),[HFN(CM,self.D,self.age,'7'),HFN(CM,self.D,self.ass,'2')] ) ) )
      self.assertEqual( "D(7)", str(HFC(HFN(CM,self.D,self.age,'7'),[HFN(CM,self.D,self.bas,'5'),HFN(CM,self.D,self.ass,'2')] ) ) )
      self.assertEqual( "D(7)", str(HFC(HFN(CM,self.D,self.age,'7'),[HFN(CM,self.D,self.bas,'5'),HFN(CM,self.D,self.age,'7')] ) ) )
      self.assertEqual( "D(7)", str(HFC(HFN(CM,self.D,self.age,'7'),[HFN(CM,self.D,self.age,'7'),HFN(CM,self.D,self.ass,'2'),HFN(CM,self.D,self.bas,'5')] ) ) )
      self.assertEqual( "D(7)", str(HFC(HFN(CM,self.D,self.age,'7'),[HFN(CM,self.D,self.bas,'5'),HFN(CM,self.D,self.bas,'5'),HFN(CM,self.D,self.ass,'2')] ) ) )
      self.assertEqual( "D(2)", str(HFC(HFN(CM,self.D,self.ass,'2'),[HFN(CM,self.D,self.age,'7'),HFN(CM,self.D,self.bas,'5'),HFN(CM,self.D,self.ass,'2')] ) ) )
      self.assertEqual( "D(2)", str(HFC(HFN(CM,self.D,self.ass,'2'),[HFN(CM,self.D,self.age,'7'),HFN(CM,self.D,self.ass,'2')] ) ) )
      self.assertEqual( "D(2)", str(HFC(HFN(CM,self.D,self.ass,'2'),[HFN(CM,self.D,self.age,'7'),HFN(CM,self.D,self.bas,'%')] ) ) )
      self.assertEqual( "D(2)", str(HFC(HFN(CM,self.D,self.ass,'2'),[HFN(CM,self.D,self.age,'7')] ) ) )
      # Tonic base with Dominant
      self.assertEqual( "T^D(1)", str(HFC(HFN(CM,self.T,self.bas,'1'),[HFN(CM,self.D,self.age,'7'),HFN(CM,self.D,self.bas,'5'),HFN(CM,self.D,self.ass,'2')] ) ) )
      self.assertEqual( "T^D(1)", str(HFC(HFN(CM,self.T,self.bas,'1'),[HFN(CM,self.D,self.age,'7'),HFN(CM,self.D,self.ass,'2')] ) ) )
      self.assertEqual( "T^D(1)", str(HFC(HFN(CM,self.T,self.bas,'1'),[HFN(CM,self.D,self.age,'7'),HFN(CM,self.D,self.bas,'5')] ) ) )
      self.assertEqual( "T^D(1)", str(HFC(HFN(CM,self.T,self.bas,'1'),[HFN(CM,self.D,self.age,'7')] ) ) )
      self.assertEqual( "T^D(1)", str(HFC(HFN(CM,self.T,self.bas,'1'),[HFN(CM,self.D,self.age,'7'),HFN(CM,self.D,self.bas,'5'),HFN(CM,self.D,self.ass,'2'),HFN(CM,self.T,self.age,'3'),HFN(CM,self.T,self.bas,'1')] ) ) )
      self.assertEqual( "T^D(1)", str(HFC(HFN(CM,self.T,self.bas,'1'),[HFN(CM,self.D,self.age,'7'),HFN(CM,self.D,self.ass,'2'),HFN(CM,self.T,self.age,'-3')] ) ) )
      self.assertEqual( "T^D(1)", str(HFC(HFN(CM,self.T,self.bas,'1'),[HFN(CM,self.D,self.age,'7'),HFN(CM,self.T,self.ass,'5')] ) ) )
      self.assertEqual( "T^D(1)", str(HFC(HFN(CM,self.T,self.bas,'1'),[HFN(CM,self.D,self.age,'7'),HFN(CM,self.T,self.age,'-3')] ) ) )
      # Tonic base with Dominant and Subdominant
      self.assertEqual( "T^SD(1)", str(HFC(HFN(CM,self.T,self.bas,'1'),[HFN(CM,self.D,self.age,'7'),HFN(CM,self.S,self.age,'-6')] ) ) )
      self.assertEqual( "T^SD(1)", str(HFC(HFN(CM,self.T,self.bas,'1'),[HFN(CM,self.S,self.age,'-6'),HFN(CM,self.D,self.age,'7')] ) ) )
      self.assertEqual( "T^SD(1)", str(HFC(HFN(CM,self.T,self.bas,'1'),[HFN(CM,self.S,self.age,'-6'),HFN(CM,self.D,self.age,'7'),HFN(CM,self.D,self.bas,'5'),HFN(CM,self.S,self.bas,'4')] ) ) )
      self.assertEqual( "T^SD(1)", str(HFC(HFN(CM,self.T,self.bas,'1'),[HFN(CM,self.S,self.age,'-6'),HFN(CM,self.D,self.age,'7'),HFN(CM,self.D,self.bas,'5'),HFN(CM,self.S,self.bas,'4'),HFN(CM,self.T,self.age,'-3')] ) ) )
      # Tonic agent with Dominant
      self.assertEqual( "T^D(3)", str(HFC(HFN(CM,self.T,self.age,'3'),[HFN(CM,self.D,self.age,'7'),HFN(CM,self.D,self.bas,'5'),HFN(CM,self.D,self.ass,'2')] ) ) )
      self.assertEqual( "T^D(3)", str(HFC(HFN(CM,self.T,self.age,'3'),[HFN(CM,self.D,self.age,'7'),HFN(CM,self.D,self.ass,'2')] ) ) )
      self.assertEqual( "T^D(3)", str(HFC(HFN(CM,self.T,self.age,'3'),[HFN(CM,self.D,self.age,'7'),HFN(CM,self.D,self.bas,'5')] ) ) )
      self.assertEqual( "T^D(-3)", str(HFC(HFN(CM,self.T,self.age,'-3'),[HFN(CM,self.D,self.age,'7')] ) ) )
      self.assertEqual( "T^D(3)", str(HFC(HFN(CM,self.T,self.age,'3'),[HFN(CM,self.D,self.age,'7'),HFN(CM,self.D,self.bas,'5'),HFN(CM,self.D,self.ass,'2'),HFN(CM,self.T,self.age,'3'),HFN(CM,self.T,self.bas,'1')] ) ) )
      self.assertEqual( "T^D(3)", str(HFC(HFN(CM,self.T,self.age,'3'),[HFN(CM,self.D,self.age,'7'),HFN(CM,self.D,self.ass,'2'),HFN(CM,self.T,self.age,'3')] ) ) )
      self.assertEqual( "T^D(-3)", str(HFC(HFN(CM,self.T,self.age,'-3'),[HFN(CM,self.D,self.age,'7'),HFN(CM,self.T,self.ass,'5')] ) ) )
      self.assertEqual( "T^D(3)", str(HFC(HFN(CM,self.T,self.age,'3'),[HFN(CM,self.D,self.age,'7'),HFN(CM,self.T,self.age,'-3')] ) ) )
      # Tonic agent with Subdominant
      self.assertEqual( "T^S(-3)", str(HFC(HFN(CM,self.T,self.age,'-3'),[HFN(CM,self.S,self.age,'6'),HFN(CM,self.S,self.bas,'4'),HFN(CM,self.S,self.ass,'1')] ) ) )
      self.assertEqual( "T^S(-3)", str(HFC(HFN(CM,self.T,self.age,'-3'),[HFN(CM,self.S,self.age,'6'),HFN(CM,self.S,self.ass,'1')] ) ) )
      self.assertEqual( "T^S(-3)", str(HFC(HFN(CM,self.T,self.age,'-3'),[HFN(CM,self.S,self.age,'6'),HFN(CM,self.S,self.bas,'4')] ) ) )
      self.assertEqual( "T^S(-3)", str(HFC(HFN(CM,self.T,self.age,'-3'),[HFN(CM,self.S,self.age,'6')] ) ) )
      self.assertEqual( "T^S(3)", str(HFC(HFN(CM,self.T,self.age,'3'),[HFN(CM,self.S,self.age,'6'),HFN(CM,self.S,self.bas,'4'),HFN(CM,self.S,self.ass,'1'),HFN(CM,self.T,self.age,'3'),HFN(CM,self.T,self.bas,'1')] ) ) )
      self.assertEqual( "T^S(3)", str(HFC(HFN(CM,self.T,self.age,'3'),[HFN(CM,self.S,self.age,'6'),HFN(CM,self.S,self.ass,'1'),HFN(CM,self.T,self.age,'-3')] ) ) )
      self.assertEqual( "T^S(3)", str(HFC(HFN(CM,self.T,self.age,'3'),[HFN(CM,self.S,self.age,'6'),HFN(CM,self.T,self.ass,'5')] ) ) )
      self.assertEqual( "T^S(3)", str(HFC(HFN(CM,self.T,self.age,'3'),[HFN(CM,self.S,self.age,'6'),HFN(CM,self.T,self.age,'-3')] ) ) )
      # Tonic agent with Dominant and Subdominant
      self.assertEqual( "T^SD(3)", str(HFC(HFN(CM,self.T,self.age,'3'),[HFN(CM,self.D,self.age,'7'),HFN(CM,self.S,self.age,'-6')] ) ) )
      self.assertEqual( "T^SD(3)", str(HFC(HFN(CM,self.T,self.age,'3'),[HFN(CM,self.S,self.age,'-6'),HFN(CM,self.D,self.age,'7')] ) ) )
      self.assertEqual( "T^SD(-3)", str(HFC(HFN(CM,self.T,self.age,'-3'),[HFN(CM,self.S,self.age,'-6'),HFN(CM,self.D,self.age,'7'),HFN(CM,self.D,self.bas,'5'),HFN(CM,self.S,self.bas,'4')] ) ) )
      self.assertEqual( "T^SD(-3)", str(HFC(HFN(CM,self.T,self.age,'-3'),[HFN(CM,self.S,self.age,'-6'),HFN(CM,self.D,self.age,'7'),HFN(CM,self.D,self.bas,'5'),HFN(CM,self.S,self.bas,'4'),HFN(CM,self.T,self.age,'-3')] ) ) )
      # Dominant base with Subdominant
      # Dominant base with Subdominant and Tonic
      # Dominant agent with Subdominant
      # Dominant agent with Tonic
      # Dominant agent with Subdominant and Tonic
      # Dominant associate with Tonic
      # Dominant associate with Subdominant
      # Dominant associate with Tonic and Subdominant
      # Subdominant base with Tonic
      # Subdominant base with Dominant
      # Subdominant base with Tonic and Dominant
      # Subdominant agent with Tonic
      # Subdominant agent with Dominant
      # Subdominant agent with Tonic and Dominant
      # Something known with Unknown on top
      self.assertEqual( "T(3)", str(HFC(HFN(CM,self.T,self.age,'3'),[HFN(CM,self.U,self.unk,'4'),HFN(CM,self.T,self.bas,'1')] ) ) )
      # Unknown with something known on top
      self.assertEqual( "U^S(#1)", str(HFC(HFN(CM,self.U,self.unk,'#1'),[HFN(CM,self.S,self.age,'-6'),HFN(CM,self.S,self.ass,'1')] ) ) )
   
   def test_equal( self ):
      a = HarmonicFunctionalNote( key.Key('C'), self.T, self.bas, '1' )
      b = HarmonicFunctionalNote( key.Key('C'), self.T, self.age, '3' )
      c = HarmonicFunctionalNote( key.Key('C'), self.T, self.ass, '5' )
      d = HarmonicFunctionalNote( key.Key('C'), self.D, self.bas, '5' )
      e = HarmonicFunctionalNote( key.Key('c'), self.T, self.age, '3' ) # c minor -- should be equivalent to b
      # these should be equal
      tester1 = HarmonicFunctionalChord( a, [a,b,c] )
      tester2 = HarmonicFunctionalChord( a, [a,b,c] )
      self.assertTrue( tester1.equal( tester2 ) )
      self.assertTrue( tester2.equal( tester1 ) )
      tester2 = HarmonicFunctionalChord( a, [a,c,b] )
      self.assertTrue( tester1.equal( tester2 ) )
      self.assertTrue( tester2.equal( tester1 ) )
      tester2 = HarmonicFunctionalChord( a, [b,a,c] )
      self.assertTrue( tester1.equal( tester2 ) )
      self.assertTrue( tester2.equal( tester1 ) )
      tester2 = HarmonicFunctionalChord( a, [b,c,a] )
      self.assertTrue( tester1.equal( tester2 ) )
      self.assertTrue( tester2.equal( tester1 ) )
      tester2 = HarmonicFunctionalChord( a, [c,a,b] )
      self.assertTrue( tester1.equal( tester2 ) )
      self.assertTrue( tester2.equal( tester1 ) )
      tester2 = HarmonicFunctionalChord( a, [c,b,a] )
      self.assertTrue( tester1.equal( tester2 ) )
      self.assertTrue( tester2.equal( tester1 ) )
      tester2 = HarmonicFunctionalChord( a, [a,c,e] )
      self.assertTrue( tester1.equal( tester2 ) )
      self.assertTrue( tester2.equal( tester1 ) )
      # these should not be equal
      tester2 = HarmonicFunctionalChord( a, [b,a,a] ) # c is missing
      self.assertEqual( tester1.equal( tester2 ), False )
      self.assertEqual( tester2.equal( tester1 ), False )
      tester2 = HarmonicFunctionalChord( a, [b,a] ) # c is missing
      self.assertEqual( tester1.equal( tester2 ), False )
      self.assertEqual( tester2.equal( tester1 ), False )
      tester2 = HarmonicFunctionalChord( a, [c,b,a], key.Key("D") ) # wrong key
      self.assertEqual( tester1.equal( tester2 ), False )
      self.assertEqual( tester2.equal( tester1 ), False )
      tester2 = HarmonicFunctionalChord( b, [c,b,a] ) # a is not bass
      self.assertEqual( tester1.equal( tester2 ), False )
      self.assertEqual( tester2.equal( tester1 ), False )
      tester2 = HarmonicFunctionalChord( a, [d,b,a] ) # c is replaced with d
      self.assertEqual( tester1.equal( tester2 ), False )
      self.assertEqual( tester2.equal( tester1 ), False )
      tester2 = HarmonicFunctionalChord( a, [d,b,a,c] ) # d is added
      self.assertEqual( tester1.equal( tester2 ), False )
      self.assertEqual( tester2.equal( tester1 ), False )

   def test_getVerboseLabel( self ):
      Tag = HarmonicFunctionalNote( key.Key( 'C' ), self.T, self.age, '3' )
      Tba = HarmonicFunctionalNote( key.Key( 'C' ), self.T, self.bas, '1' )
      Tas = HarmonicFunctionalNote( key.Key( 'C' ), self.T, self.ass, '5' )
      a = HarmonicFunctionalChord( Tba, [Tag,Tas,Tba] )
      self.assertEqual( a.getVerboseLabel(), 'C:Tba,C:Tag,C:Tas,C:Tba' )
      a = HarmonicFunctionalChord( Tba, [] )
      self.assertEqual( a.getVerboseLabel(), 'C:Tba' )
      a = HarmonicFunctionalChord( Tba )
      self.assertEqual( a.getVerboseLabel(), 'C:Tba' )
   
   def test_getFunctionalNotes( self ):
      Tag = HarmonicFunctionalNote( key.Key( 'C' ), self.T, self.age, '3' )
      Tba = HarmonicFunctionalNote( key.Key( 'C' ), self.T, self.bas, '1' )
      Tas = HarmonicFunctionalNote( key.Key( 'C' ), self.T, self.ass, '5' )
      a = HarmonicFunctionalChord( Tba, [Tag,Tas,Tba] )
      self.assertEqual( a.getFunctionalNotes(), [Tba,Tag,Tas,Tba] )
      a = HarmonicFunctionalChord( Tba, [] )
      self.assertEqual( a.getFunctionalNotes(), [Tba] )
      a = HarmonicFunctionalChord( Tba )
      self.assertEqual( a.getFunctionalNotes(), [Tba] )
   
   def test_getBassFunctionalNote( self ):
      Tag = HarmonicFunctionalNote( key.Key( 'C' ), self.T, self.age, '3' )
      Tba = HarmonicFunctionalNote( key.Key( 'C' ), self.T, self.bas, '1' )
      Tas = HarmonicFunctionalNote( key.Key( 'C' ), self.T, self.ass, '5' )
      a = HarmonicFunctionalChord( Tba, [Tag,Tas,Tba] )
      self.assertEqual( a.getBassFunctionalNote(), Tba )
      a = HarmonicFunctionalChord( Tba, [] )
      self.assertEqual( a.getBassFunctionalNote(), Tba )
      a = HarmonicFunctionalChord( Tba )
      self.assertEqual( a.getBassFunctionalNote(), Tba )
   
   def test_getOtherFunctionalNotes( self ):
      Tag = HarmonicFunctionalNote( key.Key( 'C' ), self.T, self.age, '3' )
      Tba = HarmonicFunctionalNote( key.Key( 'C' ), self.T, self.bas, '1' )
      Tas = HarmonicFunctionalNote( key.Key( 'C' ), self.T, self.ass, '5' )
      a = HarmonicFunctionalChord( Tba, [Tag,Tas,Tba] )
      self.assertEqual( a.getOtherFunctionalNotes(), [Tag,Tas,Tba] )
      a = HarmonicFunctionalChord( Tba, [] )
      self.assertEqual( a.getOtherFunctionalNotes(), [] )
      a = HarmonicFunctionalChord( Tba )
      self.assertEqual( a.getOtherFunctionalNotes(), [] )
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
class TestPossibleFunctionsFromScaleDegree( unittest.TestCase ):
   # possibleFunctionsFromScaleDegree( theKey, scaleDegree, position ):
   @staticmethod
   def equalsMaker( aaa, zzz ):
      # Given two model outputs from possibleFunctionsFromScaleDegre() outputs
      # True or False depending on whether the contents of the outputs is
      # the same. This function is required because, by default, assertEqual()
      # only uses the == to test equality, and the things outputted by pFFSD()
      # don't really like that.
      if len(aaa) != len(zzz):
         return False
      else:
         for i in xrange(len(aaa)):
            if aaa[i][0].equal( zzz[i][0] ) and aaa[i][1].equal( zzz[i][1] ):
               for i in xrange(len(zzz)):
                  if zzz[i][0].equal( aaa[i][0] ) and zzz[i][1].equal( aaa[i][1] ):
                     return True
            else:
               return False
   
   def setUp( self ):
      ## Some definitions for testing
      self.S = HarmonicFunction.Subdominant
      self.T = HarmonicFunction.Tonic
      self.D = HarmonicFunction.Dominant
      self.U = HarmonicFunction.Unknown
      self.bas = FunctionalRole.Base
      self.age = FunctionalRole.Agent
      self.ass = FunctionalRole.Associate
      self.unk = FunctionalRole.Unknown
      self.low = RelativeVoicePosition.Lowest
      self.mid = RelativeVoicePosition.Middle
      self.hig = RelativeVoicePosition.Highest
      self.guaranteed = ConditionForFunction.IsGuaranteed
      self.isLowest = ConditionForFunction.IsLowestVoice
      self.isPresent = ConditionForFunction.IsPresent
   
   def test_equalsMaker( self ):
      CM = key.Key( 'C' )
      self.assertTrue( self.equalsMaker( [[HarmonicFunctionalNote(CM,self.T,self.age,'3'),ConditionForFunction(self.guaranteed,0)]], [[HarmonicFunctionalNote(CM,self.T,self.age,'3'),ConditionForFunction(self.guaranteed,0)]] ) )
      self.assertFalse( self.equalsMaker( [[HarmonicFunctionalNote(CM,self.T,self.bas,'1'),ConditionForFunction(self.guaranteed,0)]], [[HarmonicFunctionalNote(CM,self.T,self.age,'3'),ConditionForFunction(self.guaranteed,0)]] ) )
   
   def test_agent_major( self ):
      CM = key.Key( 'C' )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'3',self.low ), [[HarmonicFunctionalNote(CM,self.T,self.age,'3'),ConditionForFunction(self.guaranteed,0)]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'6',self.low ), [[HarmonicFunctionalNote(CM,self.S,self.age,'6'),ConditionForFunction(self.guaranteed,0)]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'7',self.low ), [[HarmonicFunctionalNote(CM,self.D,self.age,'7'),ConditionForFunction(self.guaranteed,0)]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'3',self.mid ), [[HarmonicFunctionalNote(CM,self.T,self.age,'3'),ConditionForFunction(self.guaranteed,0)]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'6',self.mid ), [[HarmonicFunctionalNote(CM,self.S,self.age,'6'),ConditionForFunction(self.guaranteed,0)]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'7',self.mid ), [[HarmonicFunctionalNote(CM,self.D,self.age,'7'),ConditionForFunction(self.guaranteed,0)]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'3',self.hig ), [[HarmonicFunctionalNote(CM,self.T,self.age,'3'),ConditionForFunction(self.guaranteed,0)]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'6',self.hig ), [[HarmonicFunctionalNote(CM,self.S,self.age,'6'),ConditionForFunction(self.guaranteed,0)]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'7',self.hig ), [[HarmonicFunctionalNote(CM,self.D,self.age,'7'),ConditionForFunction(self.guaranteed,0)]] ) )
   
   def test_agent_minor( self ):
      CM = key.Key( 'C' )
      # the flatted 3, 6, 7 degrees might also serve as applied Subdominant agent.
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'-3',self.low ), \
                        [[HarmonicFunctionalNote(key.Key("G"),self.S,self.age,'-3'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(key.Key('G'),self.S,self.bas,'4'))], \
                           [HarmonicFunctionalNote(CM,self.T,self.age,'-3'),ConditionForFunction(self.guaranteed,0)]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'-6',self.low ), \
                        [[HarmonicFunctionalNote(key.Key("C"),self.S,self.age,'-6'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(key.Key('C'),self.S,self.bas,'4'))], \
                           [HarmonicFunctionalNote(CM,self.S,self.age,'-6'),ConditionForFunction(self.guaranteed,0)]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'-7',self.low ), \
                        [[HarmonicFunctionalNote(key.Key("D"),self.S,self.age,'-7'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(key.Key('D'),self.S,self.bas,'4'))], \
                           [HarmonicFunctionalNote(CM,self.D,self.age,'-7'),ConditionForFunction(self.guaranteed,0)]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'-3',self.mid ), \
                        [[HarmonicFunctionalNote(key.Key("G"),self.S,self.age,'-3'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(key.Key('G'),self.S,self.bas,'4'))], \
                           [HarmonicFunctionalNote(CM,self.T,self.age,'-3'),ConditionForFunction(self.guaranteed,0)]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'-6',self.mid ), \
                        [[HarmonicFunctionalNote(key.Key("C"),self.S,self.age,'-6'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(key.Key('C'),self.S,self.bas,'4'))], \
                           [HarmonicFunctionalNote(CM,self.S,self.age,'-6'),ConditionForFunction(self.guaranteed,0)]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'-7',self.mid ), \
                        [[HarmonicFunctionalNote(key.Key("D"),self.S,self.age,'-7'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(key.Key('D'),self.S,self.bas,'4'))], \
                           [HarmonicFunctionalNote(CM,self.D,self.age,'-7'),ConditionForFunction(self.guaranteed,0)]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'-3',self.hig ), \
                        [[HarmonicFunctionalNote(key.Key("G"),self.S,self.age,'-3'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(key.Key('G'),self.S,self.bas,'4'))], \
                           [HarmonicFunctionalNote(CM,self.T,self.age,'-3'),ConditionForFunction(self.guaranteed,0)]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'-6',self.hig ), \
                        [[HarmonicFunctionalNote(key.Key("C"),self.S,self.age,'-6'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(key.Key('C'),self.S,self.bas,'4'))], \
                           [HarmonicFunctionalNote(CM,self.S,self.age,'-6'),ConditionForFunction(self.guaranteed,0)]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'-7',self.hig ), \
                        [[HarmonicFunctionalNote(key.Key("D"),self.S,self.age,'-7'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(key.Key('D'),self.S,self.bas,'4'))], \
                           [HarmonicFunctionalNote(CM,self.D,self.age,'-7'),ConditionForFunction(self.guaranteed,0)]] ) )
   
   def test_base_lowest( self ):
      CM = key.Key( 'C' )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'1',self.low ), \
            [[HarmonicFunctionalNote(CM,self.T,self.bas,'1'),ConditionForFunction(self.guaranteed,0)]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'4',self.low ), \
            [[HarmonicFunctionalNote(CM,self.S,self.bas,'4'),ConditionForFunction(self.guaranteed,0)]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'5',self.low ), \
            [[HarmonicFunctionalNote(CM,self.D,self.bas,'5'),ConditionForFunction(self.guaranteed,0)]] ) )
   
   def test_base_middle_highest( self ):
      CM = key.Key( 'C' )
      ## ^4 is kind of stuck
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'4',self.mid ), \
            [[HarmonicFunctionalNote(CM,self.S,self.bas,'4'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(CM,self.S,self.age,'6'))], \
            [HarmonicFunctionalNote(CM,self.S,self.bas,'4'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(CM,self.S,self.age,'-6'))]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'4',self.hig ), \
            [[HarmonicFunctionalNote(CM,self.S,self.bas,'4'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(CM,self.S,self.age,'6'))], \
            [HarmonicFunctionalNote(CM,self.S,self.bas,'4'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(CM,self.S,self.age,'-6'))]] ) )
      ## ^1 and ^5 may also serve as associates
      ## if T-agent is present, then ^1 is a T-base; if S-agent is present or S-base is self.lowest voice, then ^1 is S-associate
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'1',self.mid ), \
            [[HarmonicFunctionalNote(CM,self.T,self.bas,'1'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(CM,self.T,self.age,'3'))], \
            [HarmonicFunctionalNote(CM,self.T,self.bas,'1'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(CM,self.T,self.age,'-3'))], \
            [HarmonicFunctionalNote(CM,self.S,self.ass,'1'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(CM,self.S,self.age,'6'))], \
            [HarmonicFunctionalNote(CM,self.S,self.ass,'1'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(CM,self.S,self.age,'-6'))], \
            [HarmonicFunctionalNote(CM,self.S,self.ass,'1'),ConditionForFunction(self.isLowest,HarmonicFunctionalNote(CM,self.S,self.bas,'4'))]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'1',self.hig ), \
            [[HarmonicFunctionalNote(CM,self.T,self.bas,'1'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(CM,self.T,self.age,'3'))], \
            [HarmonicFunctionalNote(CM,self.T,self.bas,'1'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(CM,self.T,self.age,'-3'))], \
            [HarmonicFunctionalNote(CM,self.S,self.ass,'1'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(CM,self.S,self.age,'6'))], \
            [HarmonicFunctionalNote(CM,self.S,self.ass,'1'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(CM,self.S,self.age,'-6'))], \
            [HarmonicFunctionalNote(CM,self.S,self.ass,'1'),ConditionForFunction(self.isLowest,HarmonicFunctionalNote(CM,self.S,self.bas,'4'))]] ) )
      ## if D-agent is present, then ^5 is a D-base; if T-agent is present or T-base is self.lowest voice, then ^5 is T-associate
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'5',self.mid ), \
            [[HarmonicFunctionalNote(CM,self.D,self.bas,'5'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(CM,self.D,self.age,'7'))], \
            [HarmonicFunctionalNote(CM,self.D,self.bas,'5'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(CM,self.D,self.age,'-7'))], \
            [HarmonicFunctionalNote(CM,self.T,self.ass,'1'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(CM,self.T,self.age,'3'))], \
            [HarmonicFunctionalNote(CM,self.T,self.ass,'1'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(CM,self.T,self.age,'-3'))], \
            [HarmonicFunctionalNote(CM,self.T,self.ass,'1'),ConditionForFunction(self.isLowest,HarmonicFunctionalNote(CM,self.T,self.bas,'1'))]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'5',self.hig ), \
            [[HarmonicFunctionalNote(CM,self.D,self.bas,'5'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(CM,self.D,self.age,'7'))], \
            [HarmonicFunctionalNote(CM,self.D,self.bas,'5'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(CM,self.D,self.age,'-7'))], \
            [HarmonicFunctionalNote(CM,self.T,self.ass,'1'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(CM,self.T,self.age,'3'))], \
            [HarmonicFunctionalNote(CM,self.T,self.ass,'1'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(CM,self.T,self.age,'-3'))], \
            [HarmonicFunctionalNote(CM,self.T,self.ass,'1'),ConditionForFunction(self.isLowest,HarmonicFunctionalNote(CM,self.T,self.bas,'1'))]] ) )
   
   def test_diatonic_degree_2( self ):
      CM = key.Key( 'C' )
      ### with ^2 in the self.lowest voice, the only thing that'll enable D-associate function is the D-agent
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'2',self.low ), \
            [[HarmonicFunctionalNote(CM,self.D,self.ass,'2'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(CM,self.D,self.age,'7'))], \
            [HarmonicFunctionalNote(CM,self.D,self.ass,'2'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(CM,self.D,self.age,'-7'))]] ) )
      ### with ^2 in a self.middle or upper voice, either the D-agent being present or the D-base in the self.lowest voice will enable D-associate function
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'2',self.mid ), \
            [[HarmonicFunctionalNote(CM,self.D,self.ass,'2'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(CM,self.D,self.age,'7'))], \
            [HarmonicFunctionalNote(CM,self.D,self.ass,'2'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(CM,self.D,self.age,'-7'))], \
            [HarmonicFunctionalNote(CM,self.D,self.ass,'2'),ConditionForFunction(self.isLowest,HarmonicFunctionalNote(CM,self.D,self.bas,'5'))]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'2',self.hig ), \
            [[HarmonicFunctionalNote(CM,self.D,self.ass,'2'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(CM,self.D,self.age,'7'))], \
            [HarmonicFunctionalNote(CM,self.D,self.ass,'2'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(CM,self.D,self.age,'-7'))], \
            [HarmonicFunctionalNote(CM,self.D,self.ass,'2'),ConditionForFunction(self.isLowest,HarmonicFunctionalNote(CM,self.D,self.bas,'5'))]] ) )
   
   def test_single_flat_degrees( self ):
      CM = key.Key( 'C' )
      ### if it's a single-flat degree, it's a Subdominant applied chord if:
      ###   -the degree a third lower is present in the self.lowest voice or this degree is a third (V of something), or
      ###   -the degrees a minor third above and a minor third above that are present (vii of something)
      ### also, it's an applied Agent, so it's pretty powerful... but we need some reason to believe it's not just a regular NHT
      ### *** NB: Degrees flat 3, 6, and 7 are tested above, in test_agent_minor()
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'-1',self.low ), \
            [[HarmonicFunctionalNote(key.Key("E-"),self.S,self.age,'-1'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(key.Key('E-'),self.S,self.bas,'4'))]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'-1',self.mid ), \
            [[HarmonicFunctionalNote(key.Key("E-"),self.S,self.age,'-1'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(key.Key('E-'),self.S,self.bas,'4'))]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'-1',self.hig ), \
            [[HarmonicFunctionalNote(key.Key("E-"),self.S,self.age,'-1'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(key.Key('E-'),self.S,self.bas,'4'))]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'-2',self.low ), \
            [[HarmonicFunctionalNote(key.Key("F"),self.S,self.age,'-2'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(key.Key('F'),self.S,self.bas,'4'))]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'-2',self.mid ), \
            [[HarmonicFunctionalNote(key.Key("F"),self.S,self.age,'-2'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(key.Key('F'),self.S,self.bas,'4'))]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'-2',self.hig ), \
            [[HarmonicFunctionalNote(key.Key("F"),self.S,self.age,'-2'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(key.Key('F'),self.S,self.bas,'4'))]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'-4',self.low ), \
            [[HarmonicFunctionalNote(key.Key("A-"),self.S,self.age,'-4'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(key.Key('A-'),self.S,self.bas,'4'))]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'-4',self.mid ), \
            [[HarmonicFunctionalNote(key.Key("A-"),self.S,self.age,'-4'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(key.Key('A-'),self.S,self.bas,'4'))]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'-4',self.hig ), \
            [[HarmonicFunctionalNote(key.Key("A-"),self.S,self.age,'-4'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(key.Key('A-'),self.S,self.bas,'4'))]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'-5',self.low ), \
            [[HarmonicFunctionalNote(key.Key("B-"),self.S,self.age,'-5'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(key.Key('B-'),self.S,self.bas,'4'))]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'-5',self.mid ), \
            [[HarmonicFunctionalNote(key.Key("B-"),self.S,self.age,'-5'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(key.Key('B-'),self.S,self.bas,'4'))]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'-5',self.hig ), \
            [[HarmonicFunctionalNote(key.Key("B-"),self.S,self.age,'-5'),ConditionForFunction(self.isPresent,HarmonicFunctionalNote(key.Key('B-'),self.S,self.bas,'4'))]] ) )
   
   def test_single_sharp_degrees( self ):
      CM = key.Key( 'C' )
      ### if it's a single-sharp degree, it's a Dominant applied chord if:
      ###   -the degree a third beself.low is present in the self.lowest voice or this degree is a third (V of something)
      ###   -the degrees a minor third above and a minor third above that are present (vii of something)
      ### also, it's an applied Agent, so it's pretty powerful... but we need some reason to believe it's not just a regular NHT
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'#1',self.low ), \
                              [[HarmonicFunctionalNote(key.Key("D"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'5')],
                              [HarmonicFunctionalNote(key.Key("D"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'2'),ConditionForFunction(self.isPresent,'4')]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'#1',self.mid ), \
                              [[HarmonicFunctionalNote(key.Key("D"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'5')],
                              [HarmonicFunctionalNote(key.Key("D"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'2'),ConditionForFunction(self.isPresent,'4')]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'#1',self.hig ), \
                              [[HarmonicFunctionalNote(key.Key("D"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'5')],
                              [HarmonicFunctionalNote(key.Key("D"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'2'),ConditionForFunction(self.isPresent,'4')]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'#2',self.low ), \
                              [[HarmonicFunctionalNote(key.Key("E"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'5')],
                              [HarmonicFunctionalNote(key.Key("E"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'2'),ConditionForFunction(self.isPresent,'4')]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'#2',self.mid ), \
                              [[HarmonicFunctionalNote(key.Key("E"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'5')],
                              [HarmonicFunctionalNote(key.Key("E"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'2'),ConditionForFunction(self.isPresent,'4')]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'#2',self.hig ), \
                              [[HarmonicFunctionalNote(key.Key("E"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'5')],
                              [HarmonicFunctionalNote(key.Key("E"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'2'),ConditionForFunction(self.isPresent,'4')]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'#3',self.low ), \
                              [[HarmonicFunctionalNote(key.Key("F#"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'5')],
                              [HarmonicFunctionalNote(key.Key("F#"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'2'),ConditionForFunction(self.isPresent,'4')]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'#3',self.mid ), \
                              [[HarmonicFunctionalNote(key.Key("F#"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'5')],
                              [HarmonicFunctionalNote(key.Key("F#"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'2'),ConditionForFunction(self.isPresent,'4')]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'#3',self.hig ), \
                              [[HarmonicFunctionalNote(key.Key("F#"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'5')],
                              [HarmonicFunctionalNote(key.Key("F#"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'2'),ConditionForFunction(self.isPresent,'4')]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'#4',self.low ), \
                              [[HarmonicFunctionalNote(key.Key("G"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'5')],
                              [HarmonicFunctionalNote(key.Key("G"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'2'),ConditionForFunction(self.isPresent,'4')]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'#4',self.mid ), \
                              [[HarmonicFunctionalNote(key.Key("G"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'5')],
                              [HarmonicFunctionalNote(key.Key("G"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'2'),ConditionForFunction(self.isPresent,'4')]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'#4',self.hig ), \
                              [[HarmonicFunctionalNote(key.Key("G"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'5')],
                              [HarmonicFunctionalNote(key.Key("G"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'2'),ConditionForFunction(self.isPresent,'4')]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'#5',self.low ), \
                              [[HarmonicFunctionalNote(key.Key("A"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'5')],
                              [HarmonicFunctionalNote(key.Key("A"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'2'),ConditionForFunction(self.isPresent,'4')]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'#5',self.mid ), \
                              [[HarmonicFunctionalNote(key.Key("A"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'5')],
                              [HarmonicFunctionalNote(key.Key("A"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'2'),ConditionForFunction(self.isPresent,'4')]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'#5',self.hig ), \
                              [[HarmonicFunctionalNote(key.Key("A"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'5')],
                              [HarmonicFunctionalNote(key.Key("A"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'2'),ConditionForFunction(self.isPresent,'4')]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'#6',self.low ), \
                              [[HarmonicFunctionalNote(key.Key("B"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'5')],
                              [HarmonicFunctionalNote(key.Key("B"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'2'),ConditionForFunction(self.isPresent,'4')]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'#6',self.mid ), \
                              [[HarmonicFunctionalNote(key.Key("B"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'5')],
                              [HarmonicFunctionalNote(key.Key("B"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'2'),ConditionForFunction(self.isPresent,'4')]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'#6',self.hig ), \
                              [[HarmonicFunctionalNote(key.Key("B"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'5')],
                              [HarmonicFunctionalNote(key.Key("B"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'2'),ConditionForFunction(self.isPresent,'4')]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'#7',self.low ), \
                              [[HarmonicFunctionalNote(key.Key("C#"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'5')],
                              [HarmonicFunctionalNote(key.Key("C#"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'2'),ConditionForFunction(self.isPresent,'4')]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'#7',self.mid ), \
                              [[HarmonicFunctionalNote(key.Key("C#"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'5')],
                              [HarmonicFunctionalNote(key.Key("C#"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'2'),ConditionForFunction(self.isPresent,'4')]] ) )
      self.assertTrue( self.equalsMaker( possibleFunctionsFromScaleDegree( CM,'#7',self.hig ), \
                              [[HarmonicFunctionalNote(key.Key("C#"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'5')],
                              [HarmonicFunctionalNote(key.Key("C#"),self.D,self.age,'7'),ConditionForFunction(self.isPresent,'2'),ConditionForFunction(self.isPresent,'4')]] ) )
#-------------------------------------------------------------------------------




#-------------------------------------------------------------------------------
# "Main" Function
#-------------------------------------------------------------------------------
if __name__ == '__main__':
   print( "###############################################################################" )
   print( "## harrisonHarmony Test Suite                                                ##" )
   print( "###############################################################################" )
   print( "" )
   # define test suites
   chromaticScaleDegreeSuite = unittest.TestLoader().loadTestsFromTestCase( TestChromaticScaleDegree )
   harmonicFunctionSuite = unittest.TestLoader().loadTestsFromTestCase( TestHarmonicFunction )
   functionalRoleSuite = unittest.TestLoader().loadTestsFromTestCase( TestFunctionalRole )
   relativeVoicePositionSuite = unittest.TestLoader().loadTestsFromTestCase( TestRelativeVoicePosition )
   conditionForFunctionSuite = unittest.TestLoader().loadTestsFromTestCase( TestConditionForFunction )
   harmonicFunctionalNoteSuite = unittest.TestLoader().loadTestsFromTestCase( TestHarmonicFunctionalNote )
   harmonicFunctionalChordSuite = unittest.TestLoader().loadTestsFromTestCase( TestHarmonicFunctionalChord )
   possibleFunctionsFromScaleDegreeSuite = unittest.TestLoader().loadTestsFromTestCase( TestPossibleFunctionsFromScaleDegree )
   
   # run test suites
   unittest.TextTestRunner( verbosity = 2 ).run( chromaticScaleDegreeSuite )
   unittest.TextTestRunner( verbosity = 2 ).run( harmonicFunctionSuite )
   unittest.TextTestRunner( verbosity = 2 ).run( functionalRoleSuite )
   unittest.TextTestRunner( verbosity = 2 ).run( relativeVoicePositionSuite )
   unittest.TextTestRunner( verbosity = 2 ).run( conditionForFunctionSuite )
   unittest.TextTestRunner( verbosity = 2 ).run( harmonicFunctionalNoteSuite )
   unittest.TextTestRunner( verbosity = 2 ).run( harmonicFunctionalChordSuite )
   unittest.TextTestRunner( verbosity = 2 ).run( possibleFunctionsFromScaleDegreeSuite )
   
   #unittest.main()