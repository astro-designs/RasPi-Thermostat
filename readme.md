This project is the Raspi-Thermostat, the following notes will hopefully provide enough background information for someone to re-create this.

These are very roughly cobbled-together notes that need improving. But there may be a few useful clues in here worth sharing before I get around to cleaning it up.

The project was created to provide a Central-Heating Thermostat that could be more accurately calibrated and configured than a typical electro-mechanical thermostat. Electro-mechanical thermostats typically use a bi-metalic strip to control a switch that turns the heating on or off depending on the air temperature. While these can work reasonably well and have been in use for donkey's years, they often suffer from large and poorly controlled hysteresis between the temperature threshold that turns the heading on and the temperature threshold that turns the heating off. The thermostat that was previously installed in this system was particularly bad, having about 5 degrees of hysteresis between the on and off temperatures. This led to a poorly controlled room temperature and a system that frequently left the heating on for too long or it didn't come on at all. This project aimed to fix this. It also aimed to introduce a little fun in the process.

Sure, we could go and buy a better thermostat, afterall, these are plenty of readily available and fairly cheap thermostats out there. We could also go buy a 'Hive' thermostat for even better control but at £200+ that's a little painful (caveate - but less painful than 240V across your body). Or we could buy a Raspberry Pi, a temperature sensor and a few other low-cost parts and create an entirely custom solution that does the jobe just as well as a Hive Thermostat but is infinitely more configureable.

*** Warning ***
This project requires the user to have an appreciation of the dangers of handling high-voltage mains electricity. This project is not for the feint hearted. If you were to ask a reputable qualified electrician about doing something like this then their response would be "DON'T DO IT - Buy safe, and get an approved electrician / installer to fit it for you"
Firstly it's not safe for the inexperienced, it could do serious harm or even kill someone if exposed & live wiring came into contact with them.
Secondly no qualified electrician would probably want to have anything to do with it - other than to remove it and replace it with an off-the-shelf central-heating thermostat that meets the standards applicable for the country it's installed in, so you'd be on your own if it went wrong.
Thirdly, using something like this could invalidate your home insurance. If it caused a fire then you could be left with a very large bill or far far worse.
If you want my advice - Stay safe - DON'T DO IT! :o)

But if you wish to know more, please read on...

Central heating wiring varies from system to system and i'm not going to go into details about adapting this to other systems. This is designed to work with what is usually described as an 'S-Plan' Central Heating System. If your system has one 'room thermostat', a 2-port valve, a separate central-heating pump that's not integral to the boiler then you could have a compatible system. But you need to figure that bit out. As above, if in doubt, don't do it...

Parts required
1) Raspberry Pi Zero W & SD card
    You could use a plain Pi Zero (no WiFi) but setting it up and developing the software would be more difficult.
    Cost: £9.30
    https://thepihut.com/products/raspberry-pi-zero-w
    https://shop.pimoroni.com/products/raspberry-pi-zero-w?variant=39458414297171
    
    SD Card... any 8GB or larger class 10 micro-SD card.
    Cost: £5.00
    
2) Temperature sensor
    We used a 1-wire temperature sensor but other types, other sensors or other interfaces could be used here but this option gave us a sensor that would stick out through a hole in the case to sample the air temperature.
    Cost: £8.70 https://thepihut.com/products/waterproof-ds18b20-digital-temperature-sensor-extras
    
3) Screen.
    We used a Waveshare 1.44" screen with integrated joystick and three buttons.
    https://www.waveshare.com/wiki/1.44inch_LCD_HAT
    https://www.amazon.co.uk/Waveshare-1-44inch-LCD-HAT-Communicating/dp/B077YK8161
    Cost: £16
    
4) Mains relay board
    We chose a separate board so the high voltage mains could be switched well away from the Raspberry Pi.
    https://www.amazon.co.uk/gp/product/B01BWX6B9M/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1
    Cost: £15

5) Power supply
    This needs to power the Raspberry Pi, taking power from the Central Heating system.
    For this we used an off-the-shelf 2A USB leaded power supply that had a US style mains plug. We got it cheap - one of those things that you get thinking you'll use it one day - well we finally found a use for it. Even though it has a US plug, the board inside is still designed to run off a 110V or 220V / 240V supply. So that came apart, the board was safely extracted and built into the thermostat project.
    We could have used an off-the-shelf separate USB leaded power supply which has the advantages that we don't need to expose the high voltage but we wanted to build this into a box that contained the relay and was connected to the central heating mains.
    
    https://shop.pimoroni.com/products/raspberry-pi-universal-power-supply
    https://thepihut.com/collections/raspberry-pi-power-supplies/products/raspberry-pi-zero-uk-power-supply
    
    Cost: £7 - £9 (typ)
    
6) 4.7kR 1/4W or 1/8W wired resistor
    If you're lucky, this will come with the 1-wire temperature sensor
    
7) Servo extension cables (2)
    https://thepihut.com/collections/adafruit-cables/products/servo-extension-cable-30cm-12-long
    Cost: £1.70 each (two required)
    
8) Sundry items including equipment wire, 2mm clear heat-shrink sleaving, soldering iron, connectors etc. hot-melt glue / gun.
9) Optional - 500mA 20mm fuse
10) A bot to put it in - or two...
    We used two boxes here. The first was a 45mm deep single pattress box with a blank cover.
    https://www.toolstation.com/axiom-pattress-box/p24531
    
    The second was a smaller 25mm pattress box with a not-so-plane cover
    https://www.toolstation.com/axiom-pattress-box/p68852
    
    The cover was a modified Ethernet socket panel where the existing cut-out was almost perfectly matched to the 1.44" screen. The cutout was enlarged to suit the screen and a 4mm hole was added to allow the joystick to stick out at the bottom of the panel.
    The panel I used came out of a box of eletrical bits that i'd been saving for that thing that application you never know about until you've usually thrown the bits away. In this case I was lucky, I had just one of these and it was a near perfect fit. But if I had a basic blank faceplate then i'd have probably used that and cut a square hole...
    https://www.networkscentre.com/i/q/SM-MX-BFP-S-02-02/siemon-max-single-gang-british-faceplate-2-port-white
    https://www.toolstation.com/axiom-blank-plate/p35507?_br_psugg_q=single+blank+plate?searchstr=single%20blank
        
    
    A 6mm hole was drilled into the bottom 'side' of the pattress box to allow the temperature sensor to poke out and sample the air temperature.

There are plenty of details out there on how to connect a 1-wire temperature sensor to a Raspberry Pi. The easiest way is to connect it across the 3.3V supply, connecting the signal wire to GPIO(4) and have a 4.7k pull-up from GPIO(4) to 3.3V.

Enable the 1-wire interface through raspi-config...

Controlling a relay...
Again there are plenty of examples out there on how to do this. However, what we want here is a safe solution. No relays hanging off wires please. The solution we used here was an off-the-shelf mains relay board designed to allow something like a Raspberry Pi, Arduino or similar to control a mains relay. It has screw terminals for the mains, screw terminals for the connection to the Pi and what appears to be a safe degree of isloation between the low-voltage interface and the high-voltage interface.

The relay board used here as a "Mains Switch Relay 2" by SF Innovations, available from your average rain-forest / river brand supplier for around £15.

https://www.amazon.co.uk/gp/product/B01BWX6B9M/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1

It's rated for 5A - at least it has a 5A fuse. But we're only expecting to switch a 6W load. A typical S-Plan central heating system will use a 2-port valve or possibly a 3-port valve which usually consume around 6W. 6W on a 220V circuit means we're switching just less than 30mA. So a 5A fuse is far higher that we really need here. In fact central heating systems usually have a 3A or 5A fuse to supply the whole system! So for a little extra safety, you could swap the fuse for (say) a 500mA fuse.

There are other versions of this relay board that include a small case too, these are good to help keep those nasty mains voltages away from your lovely Raspberry Pi or even those inquisitive fingers.

The screen...
The screen was considered a mini marvel when we first had a play with it. Just 1.44" across, 128 x 128 pixels, an 8 position joystick with push switch and three other push-switches all on a Pi Zero 'Hat'. The example software provided by Waveshare made the whole project so much easier. Originally the plan was to find some way to write to the screen. Having never done this before we weren't too sure what to expect but the one thing that got our pulses racing was an example from Waveshere that got the Raspberry Pi desktop running on that tiny 1.44" screen, supporting refresh rates of around 30Hz. There's even examples that allow you to use the joystick to control the mouse! This meant that we could develop the software on a HDMI monitor, configure the software to run full-screen and then switch to the smaller screen where it would run a full-screen application across the 128 x 128 pixel 1.44" screen.

https://www.waveshare.com/wiki/1.44inch_LCD_HAT

https://www.amazon.co.uk/Waveshare-1-44inch-LCD-HAT-Communicating/dp/B077YK8161

Next it was a few lessons in using the Python3 GuiZero library to write stuff to the screen. This was made easy by the tutorials available for GuiZero and also that we could switch to developing the code on a normal HDMI monitor and then switch to the 1.44" screen once the code was running.

To get the Pi desktop running on the 1.44" screen, we followed these instructions. We didn't go for the option to turn the joystick into a mouse as we use the joystick to control the software.
https://www.waveshare.com/wiki/1.44inch_LCD_HAT (Guides for Pi)


Wiring it all together

We used a 3-wire servo extension cable to connect the 1-wire temperature sensor to the Pi. Cutting the cable in two, the plug end was connected to the Pi and the temperature sensor was fitted with a mating plug connector so that it could easily be connected / disconnected as required during development. The red lead at the Pi end connects to pin 1 on the Pi (+3.3V). The black lead to pin 9 (GND) and the white lead to pin 7 / GPIO(4). A 4.7kR resistor needs to be soldered between GPIO(4) and 3.3V to privide a pull-up for the 1-wire interface.

https://thepihut.com/collections/adafruit-cables/products/servo-extension-cable-30cm-12-long

We also used a 3-wire servo extension to get power to the Raspberry Pi from the power supply board (see more info below) and use the spare white wire here to connect the relay control signal from the Pi GPIO to the relay board.
Again, a servo extender was cut in two, using the shrouded plug end to connect to the Pi and the unshrouded socket-end to connect to the power supply & relay board.
Connect the red wire to pin 2 on the Pi (+5V), the black wire to pin 6 (GND) and the white wire to pin 12 / GPIO(18)

Fixing the temperature sensor...
The temperature sensor sticks out of a hole in the bottom 'side' of the pattress box that supports the display panel. The temperature sensor is approximately 6mm in diameter so a 6mm hole works well here. Inside the temperature sensor is glued to the innards of the pattress box using a healthy dollop of hot-melt glue.

The temperature sensor lead needs to be cut down in size so that there's not too much cable floating around the inside of the box. In this case it was cut down to leave around 70mm of wire sticking out of the back of the temperature sensor.

Power supply...

Depending on how you want to do this, leave the Pi power supply as it is - nicely enclosed and safe, or start breaking it apart to get the circuit board out if you want to enclose it in the same box as the relay board and run it off the Central Heating supply. We broke ours apart (carefully)

Once apart, the Live & Neutral wires were connected to the Mains In terminals of the relay board. We used 7/0.2 equipment wire for this which is more than up to the job here. Remove existing wires from the power supply board and fit the new wires. Connect the other end to the relay board making sure that the live and neutral are conencted the right way around. It'll actually work either way around but it's extremely bad practice not to follow any existing labelling that tells any user which is the L / live terminal and which is the N / neutral terminal. For our solution we had about 8-10cm of 7/0.2 wire between the mains in terminal of the relay board and the mains terminals of the Pi power supply board.

It's worth adding a length of clear heat-shrink sleaving around the mains wiring from the relay board to the Pi power supply board. This is just to add an extra layer of insulation from the mains voltages. It's also worth adding a small dollop of hot-melt glue around the mains connections to the Pi Power supply. Soldered wires can be brittle, especially if the wires were knicked when the insulation was stripped off so having a little hot-melt clue around the insulation so that it tacks it to the baord and providea a little strain-relief is a good way to further help ensure that those nasty mains voltages don't go anywhere that the shouldn't.

Wire the low-voltage side of the Pi power supply to the low-voltage terminals of the relay board. This connects the +5V & GND power connections only. We're using the mains relay board as a juntion point to connect the wiring from the power supply to the Pi and the screw terminals on the relay board make it easy to use it as a easy-access junction point.

Wire the low-voltage side of the relay board to the Raspberry Pi. Use the spare end of one of the servo extension wires that was cut in two - it should plug in to the shrouded plug that's soldered to the Pi and the open end should be tinned and connected to the low voltage screw terminals on the relay board. The white wire should go to the 'IN' terminal which is the control signal for the relay. The red and black so to the +5V and GND / 0V screw terminals respectively.

Finally, connecting the nasty mains bit...

The Central heating Thermostat could be wired in one of several ways. What we need here to make life easy is a Switched live out of the heating controller - this is a live (mains) signal that becomes live when the heating timer says it's time to turn th heating on. This connects to one end of the thermostat 'switch'. The other end of the switch - the out side, goes to the 2-port valve or 3-port valve. So usually what happens is that the as the temperature falls, the bi-metalic strip in a basic electro-mechanical thermostat will close the switch and cause the heating controller live output to be conencted to the appropriate wire on the 2-port valve. This will open the valve and when open it triggers another switch to turn on the boiler & pump.

The first problem is that a basic heating thermostat doesn't need the 'Neutral' wire and without that we don't have a mains power supply to power the Raspberry Pi Power supply. If the Neutral wire is missing then you need to do some re-wiring so that the Neutral can be routed from the permanent Neutral terminal within the central heating controller - or more usually, within the heating control wiring box. Look-up the S-Plan wiring diagram for more information here. And again, if in doubt, DON'T DO IT.

Assuming there's a Neutral wire in the thermostat, then we can proceed to connect things up.

The Live in to the thermostat goes to the Live terminal of the mains-in screw terminal on the relay board.
The Neutral in the thermostat goes to the Neutral terminal of the mains-in screw terminal on the relay board.
The Earth (hopefully you have an earth wire!!) goes to the earth terminal in the inside of the 45mm patress box.
The Live out to the 2-port or 3-port valve needs to connect to the Live terminal of the mains-out screw terminal on the relay board.
The Neutral terminal of the Mains-out screw terminal should go to the Neutral terminal of the Pi Power Supply.
The Live terminal of the Mains-In (that's IN :o) ) screw terminal should also go to the Live terminal of the Pi Power supply.

This brings up the next problem... This wiring assumes that there is no permanent live into the Thermostat. That can be quite normal. The problem is that without a Permanent live, the Raspberry Pi will only be powered-up when the heating timer say's it's time to turn the heating on. This is fine and it'll work but it's not so great if you want to continually monitor the room temperature - even when the heating is off.
There are two solutions here. 1) Run a permanent live from the heating controller wiring box to the thermostat - in addition to the existing wiring. This can then be used to power the Pi permanently. You'll need an extra screw terminal for this that'll allow you to connect the permanent live to the Pi Power supply.
2) Turn the heating on permanently and let the Pi control the timing of the heating. This is exactly what we did here. This is absolutely fine but it means that your Raspberry Pi is now the heating timer and needs to be configured to bring turn the heating on and off in accordance with the original timer.
Note that the software included here currently has fixed on/off times but provision is included to set these in the settings file and since the settings file is re-written by the software when something changes, the software just needs to be modified to allow the user to change the on/off times. Work in progress...


That's mostly it. As I said above, very rough notes nut hopefully a few clues in there.

I'll get some pictures in here at some point too.