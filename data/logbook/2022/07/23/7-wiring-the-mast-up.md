# Wiring the mast up

My mast is pretty boring right now — nothing lights up, only the bees seem to be enjoying it.

By just looking at it, it seems to have the following electronics on it:

  - spreader lights
  - wind vane
  - running lights
  - antenna

Here’re the wires that go from it into my cabin along with the compression post, and then into the engine compartment:

 - 1 green
 - 1 yellow
 - 1 white(red stripe)
 - 1 white(black stripe)
 - 1 black coaxial
 - 1 black multi-prong

Tho coaxial is obviously for the antenna, the black multi-wire is definitely the Raytheon wind instrument (back in the 90s they didn’t have wireless wind vanes yet), and green/yellow and that other pair of white wires with stripes on them seem to be both for lights.  One is for navigation lights, other is for two lamps on my lower spreader.  Good that I can figure out which one is which by just plugging them in, even polarity doesn’t matter — no way they’re LED.  Interesting how all those wires go into the engine compartment, and then end up in my starboard hull where the instruments and switches are, even though they run behind the compression post inside the cabin prior to that.  Adventurous little wires.  Now I’m gonna do my best tracing them to my circuit breaker panel.

The white(red stripe)/white(black stripe) pair seems to be for foredeck (spreader) lights.  The green/yellow pair seems to be for running lights (navigation).  Both of those pairs get the voltage just fine, the bulbs must be dead (lightning strike?).

Found switch for engine room lights - those were wrongly labeled as "ANCHOR WASHDOWN".  There’s no washdown pump, hence must’ve been something else.  Both navigation lights’ and engine room lights’ wires have yellow color and exact same gauge, both go from the engine room.  Gotta love when everything’s intuitive and makes sense.

Here’s what I now know about wires coming out of the engine room:

 - yellow — (12V+) engine room lights, hooked up to "ANCHOR WASHDOWN", operational
 - green(white stripe) — (12V+) engine room blowers, goes to "ENGINE ROOM BLOWERS", operational
 - white(black stripe) — (GND) shared between engine room blowers and engine room lights
 - green — (GND) running lights
 - yellow — (12V+) running lights, goes to "RUNNING LIGHTS", non-operational
 - white(red stripe) — (12V+) spreader lights, goes to "FOREDECK LIGHTS", non-operational
 <!-- - white(black stripe) - (GND) spreader lights, goes to "ANCHOR LIGHT" for some reason... obviously non-operational -->
 - white(black stripe) - (GND) spreader lights

So, it seems to be that somebody mistakenly wired spreader lights to two separate switches, rather than one to +12V and the other to GND.  I’m gonna try to unfuck this terrible mistake.  If I’m mistaken — it’s been nice knowing y’all.

Nope, nothing.  Dead bulbs?  Both bulbs dead?  Could be, they’re really high up and hard to get to, and the boat’s over 20 years old, hence quite possible.  The resistance is 35KOhm one way, 40MOhm the other... might be LEDs — color me impressed.  Will rewire now and give it another try.

Nothing again.  Time to put this shit to bed, it’s almost 23:00.

On a side note, the current state of wiring on that panel could be best described as dismal.
