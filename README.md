Operating system for Minecraft programs
====

The big idea
----

I'm creating some technology that will allow the collaborative development
of awesome multi story active buildings inside Minecraft - buildings that
do things when you walk into the various rooms, such as a mini-game, a treasure
hunt, or any behaviour you could possibly imagine when you are in each room
of the building.

This technology will run on the Raspberry Pi, PC and Mac. 
You'll be able to download everything onto your computer and run it yourself. 

Some of the room designs and code will be contributed by you, and some will be 
contributed by people you have probably never met before!


What will it look like?
----

I'm going to build a huge multi storey building, with space for lots of rooms 
in it. Each room will be the same size. In the middle of the building will 
be the Minecraft lift from Adventure 10 of "Adventures in Minecraft". 
But that's as far as I'm going to go! I'm then going to open up the rest of 
the program design to a whole worldwide community of creative volunteers, to 
fill in the gaps for me!


How will it work?
----

You'll be able to prototype a room design inside a special "portacabin". Here 
you can build blocks normally by placing them to build your room. An option on 
a menu will allow you to save and restore this room to/from a disk file.

You'll be given a programming API identical to mcpi, to run scripts inside that 
room. Your script will start running from the moment the player walks into the 
room, and stop running when they exit the room.

Your scripts will be sandboxed, so that it is impossible for your script to 
affect the world outside of your room, so your room will be protected from 
damage by others!


What will you be able to do with it next?
----

Once you have prototyped your room and room script in the portacabin, you'll 
be able to upload it to a web service, where it will be loaded via a floor-planning 
system into the huge tower block. Each room will be submitted by different people. 
It will be a community developed building that you can walk around and explore all 
the rooms by going up and down in the lift.


What's the point?
----

The purpose of this idea is to develop something big where each part is written by 
someone else in the community, and for your scripts to set a challenge inside your room. Visitors will enter the room, and try and complete your challenge. It could be to 
find some treasure, to collect some blocks, to solve some puzzle, or to find a way to 
exit the room in a time limit. Gain inspiration by looking at the programs and 
challenges set by others, and learn new skills along the way.

* INSPIRING - see something really big built inside minecraft, 
bigger and more complex than you could imagine building on your own. Be inspired
that big projects are developed as a lot of smaller projects all put together,
and hopefully use this inspiration to design your own huge creations that you
might not have imagined before!

* FUN - how awesome will it be to walk around this multi storey multi roomed
building inside minecraft, whizzing up and down in the lift and walking into
rooms inside your minecraft world that others have designed?

* CREATIVE - not only can you create room designs by building with blocks,
but you can write program code that runs inside your room, creating challenges,
min-games and other activities for people to explore when they come into your
room!

* COLLABORATIVE - each room in the building will be designed by others, but
you could imagine a class of children in a school all designing the rooms
on one particular floor of this huge multi storey building. Work with your
classmates to design and build a really nice mix of different rooms and
challenges that represent the creative collective of your school or your
computer club!


Where does it lead?
----

Someone once told me that certain ideas are developed by experiencing them first.
Explaining an idea and setting a specific challenge, sometimes limits where
that idea could eventually go. So I'm intentionally setting the structure of
this project initially to have no longer term purpose other than to be
inspiring, fun, creative, and collaborative.

I'm hoping that some well known building designers and engineering firms will
see some of the great ideas that come from the early stages of this project, 
and later help us to set some construction and programming challenges with a 
specific goal or purpose, such as a competition with prizes. 
Perhaps we might find some town planners who come to the project and ask school 
children to design a new building or a new shopping centre and to prototype the 
whole thing inside minecraft. Who knows! Let's try it and see where it leads to!


Watch this space!
----
Why not sign up for github and "watch" this repo to get updates as they happen!


What happens next?
----

I'm currently testing the portacabin script and will release this soon.
This will provide a way for you to start prototyping and testing your room
designs in a safe "sandbox". This will include the following features:


DELIVERY 1: room design

This program will be a further development based on the Adventures in Minecraft
(Adventure 6) program "duplicator.py" (the duplicator room).

1. A main program that you run to make everything work
2. menu system to choose features of the portacabin
3. a way for you to build the portacabin
4. a way for you to destroy the portacabin
5. a way to light the portacabin while you are building it (see turnerprizeroom.py)
6. a defined file format for defining the block layout of a room
7. some help with deciding where your entry door to the room goes!
8. save your room to a file
9. restore your room from a file


Future releases
----

I think the following features will then be developed and made available
to you in future deliveries:

DELIVERY 2: script running

1. a geofence feature that monitors entry and exit to/from the room
2. your python program is started when you enter the room
3. your python program is stopped when you exit the room


DELIVERY 3: room sandboxing

1. an electric fence that "buzzes" if you try to build outside of your room
2. an electric fence that "buzzes" if your program tries to build outside of your room
3. an electric fence that "buzzes" if your program tries to observe outside of your room
4. 3 strikes and you are out - 3 buzzes and your program stops
5. stopping of an errant "buzzing" script.


DELIVERY 4: user memories

1. A python module that allows you to store and retrieve configuration settings
2. A python module that allows you to save and restore "state" about your room


DELIVERY 5: packaging

1. A menu feature that allows you to build a distributable package (zip) file
that contains your room design, configuration settings, any stored state, and
the program that runs when the player is in the room
2. A menu feature to load a room from a room package (zip) file.


TEASERS
====

* The portacabin, a hollow shell (Adventures in Minecraft ch3, house building)
* lighting the portacabin or rooms ("The Turner Prize Room" script I wrote)
* geofencing room entry and exit (Adventures in Minecraft ch2, the rent game)
* room save and load format (Adventures in Minecraft ch6, Duplicator room, 
  with added field for extraData)
* Building something much taller than the Minecraft world (Adventures in Minecraft ch8,
  Alien Invasion including teleporter)
* Building a structure with sloping edges (Adventures in Minecraft ch7, pyramids)
* sandboxing scripts (something new!)
* The lift (Adventures in Minecraft ch10, without hardware, but with walls and sliding doors
  using minecraftstuff Shape object to move doors)
* floorplan building (Adventures in Minecraft ch6, tipchat, a list of room names and program names)
* Starting and stopping scripts (something new!)
* Which type of building? Look all through Adventures in Minecraft for some secret hints
  planted in a number of the chapters!
* controlling the lift (Tkinter user interface panel)

That's enough teasers for now! Keep watching!


David Whale
@whaleygeek
