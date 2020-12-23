So far:

o Converted from Python 2, to Python 3. 

o Simplifying coordinate calculations - kudos for the idea!

o Added random event Quips – should make the game a tad more ‘NPC’?

o Heavily re-factored for growth, testing, re-use, and maintenance using modern Python.


Original authors did an excellent job here - made the modernization a WHOLE LOT easier!

-- Nagy

Original:


================
 Star Trek 1971
================
------------
 for Python
------------

About
=====

I recently discovered the classic old BASIC game `Star Trek`_ from 1971, through a post seen on Reddit_.

The post contained a version of the game rewritten in C-Sharp which I thought was quite good.
I wondered if anyone had ported it to Python.

After a little bit of research, I didn't find a definitive version for Python.

This is by no means a definitive version itself; I just took the C# version and converted it to Python.

.. _Star Trek: http://en.wikipedia.org/wiki/Star_Trek_%28text_game%29
.. _Reddit: http://www.codeproject.com/Articles/28228/Star-Trek-Text-Game

Improvements
============

There's heaps that can be done with this program. A lot of implementations used global variables.
I tried to fix this by encapsulating them in a global object, but this can definitely be improved further.

Here is a list of possible improvements:

- Encapsulate everything in classes
- Include help/instructions
- Add extra features;
   + new ships, celestial objects, etc
   + new weapon types
   + crew functions
- Easier navigation (using cartesian system maybe)
- Make some parts more 'Pythonic'
- ...Plenty more!
