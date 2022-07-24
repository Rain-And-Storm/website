# Solar panels

Done mounting four [170W 24V Sunpower flexible solar panels](https://www.sunpoweredyachts.com/product-page/sunpower-e-flex-170watt-panel) onto my bimini.  Used [these zip ties](https://www.amazon.com/gp/product/B09S5T2846/).  They claim to be UV-resistant.  Let’s see how long they last.  Initially I used much smaller zip ties; those got broken by strong winds during one of the mini-storms two months ago — almost lost one of my $500 panels!

It was either too hard to make the aluminum skeleton of the bimini symmetrical, or my boat’s cockpit is asymmetrical... in any way, when I will have built a new carbon/epoxy hard top, it’ll be as OCD as they come.  That roof should also help me lower the boom back to where it originally was before the current roof was installed.  I’m gonna miss those round beams that I use for doing pull-ups, but it’s a small trade-off.

Things learned:
 - Flexible solar panels easily get dents from tiny things that fall off trees and get dropped by stupid birds
 - A lot of nasty stuff gets underneath flexible panels — they should ideally be glued onto the surface
 - Flexible solar panels can get permanently bent by skeleton of the bimini
 - Despite additional weight, it’s always worth going with rigid solar panels

I now have to figure out how to connect those panels to two [Victron BlueSolar MPPT 100/30 charge controllers](https://www.victronenergy.com/solar-charge-controllers/mppt-100-30) that I got from [Sun Powered Yachts](https://www.sunpoweredyachts.com) about three months ago.  I’m planning to detach from the dock within two weeks, so need to be able to recharge my batteries while at anchor.

My plans related to battery setup have slightly changed, now it’s quite possible that I’ll switch my main battery bank from 12V to 48V.  That would let me use more powerful inverter for my computers, kitchen equipment, washing machine, 3D printer, welder, etc.  12V would then come out of that inverter or some DC-DC converter.  If and when I switch to 48V, these 100/30 charging controllers won’t be of much use anymore — but that’s okay, they were just $200 each and I should be able to sell them in no time.  Two battery banks for my electric motors will have to be 48V each, no matter what.  The final setup will most likely be done in a way where I’ll be able to switch zones of my PV setup to either charge/power my motors, direct everything towards my main battery bank, or charge and power everything at the same time.  Ideally there should be a box full of MOSFETs and blinking lights that would let me reroute those things using some kind of fancy UI on a colorful touch panel, and not just some creepy mechanical tumbler.
Maybe I’ll keep it at 12V, and do high-voltage output out of the same batteries that power my motors... we’ll see.

Alright, so my current plan is to wire those 4 panels in series of two — that would make it about 60V per array (340W each, 0.68KW in total).  Then I’ll drop wires from those Victron charge controllers to my battery bank.  Their manual recommends using 6 AWG for connecting controller to battery.  I have 10 AWG wires that go from PV array to controllers, but I need them, and they’re way too thin to have enough ampacity, only good for up to 15 Amps.  I might go with something like 4 AWG or thicker if 48V chargers require that — so that I won’t need to mess with wires again when it’s time for me to fiddle with 48V battery banks.  Either way, now have to find good wires with lots of thin strands to complete my photovoltaic battery charging setup.

The kit came with 30A surge protectors, they have to be included in the circuit.  There’s also Cerbo GX with LCD touchscreen, and a battery temperature sensor – no BMS, but who needs one for cheap AWG batteries, right?  Right?

I’ll connect Cerbo GX later, no need to go crazy until the basic setup is working.  No idea if I need to ground these charge controllers or not, will figure that out in the process.
