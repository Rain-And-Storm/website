# Little research on battery types

I have two 48V electric motors to install,
and also happen to need to do something about heating and powering outlets throughout the boat.

Currently my one and only battery circuit is 12V.
Since I have plans getting 230VAC inverter, and powerful ones (over 5KW) usually require at least 48V,
it looks like I’ll have to get something like Victron [Multi RS Solar](https://www.victronenergy.com/inverters-chargers/multi-rs-solar).
That one will let me charge from the shore, acts as my new MPPT, and also power my 230VAC devices if needed.
A mechanical or solid-state switch of sorts will have to be installed to direct the charge towards:
port motor bank, starboard motor bank, central ship bank, or all at once.

Victron has more powerful inverters, but they weigh over 40kg (vs. Multi RS’ 11kg),
and just look like something superyachts or multihulls over 65’ usually have.
It’s important to watch the weight.

If I do go with 48V battery setup, a DC-DC converter from 48V to 12V will have to be hooked up to the main battery bank.
[Orion-Tr 48/12-30 (360W)](https://www.victronenergy.com/dc-dc-converters/orion-tr-dc-dc-converters-isolated) should do it.
Only about 400W maximum output, but should be enough for marine electronics and 12VDC outlets (laptops, phone chargers, etc).
Curious Cat is big, but she’s not a cruise ship.
Plus it’s only 2kg, much lighter than having a dedicated battery for my 12VDC needs.
And the efficiency of that converter seems to be around 87%, not too bad.

## Types of batteries

Since I’m going to have three separate 48V battery banks, I now need to figure out what kind of chemistry to target.
I won’t buy anything battery-wise until at least one of my electric motors is installed,
or until I get my inverter and that DC-DC converter.


| Battery         | Stats      | Count | Weight          | Total bank capacity | Total bank cost      |
|:----------------|:-----------|------:|:----------------|--------------------:|---------------------:|
| LiFePo4 Super-B | 12V@210Ah  |     4 | 23x4=92kg       |            10.08KWh | 3171 € x 4 = 12684 € |
| LTO Zenaji      | 48V@40Ah   |     5 | 36x5=180kg      |             9.65KWh | 2808 € x 5 = 14040 € |
| LTO Echandia    | ?          |     ? | ?               |                     | ?                    |
| SC Maxwell      | 48V@1Ah    |    10 | 13.8kgx10=138kg |             0.53KWh | ?                    |
| SC Skeleton     | 48V@1.28Ah |    10 | 16x10=160kg     |             0.64KWh | ?                    |

This is all there is right now on the market.  Even if Echandia gets back to me,
the energy density of lithium-titanate (LTO) batteries is about half of what LFP offers.
Maybe LTO is the best there is on land, but once again, gotta watch the weight.
Supercapacitors are still at about 1/20th of what batteries can offer today, but it’s a cool technology.

Super-B’s Nomia or upcoming 12V@320Ah is what I’m likely going to go with.
I really want to go with LTE at least or my main bank,
but the weight is just always twice as bad when compared to LFP, no matter how small or big the battery is.
Sad.
