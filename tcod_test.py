#!/usr/local/bin/python3

# -----------------------------------------------------------------------------

"""
   Copyright (c) 2019 Christopher Bartlett
   [This program is licensed under the "MIT License"]
   Please see the file LICENSE in the source
   distribution of this software for license terms.
"""

# -----------------------------------------------------------------------------

import NecroMapObj
import tcod as libtcod

# -----------------------------------------------------------------------------

MAPh = 48
MAPw = 96

# create a map, with the dimensions above
mapObj = NecroMapObj.Map(MAPh, MAPw)
# mapObj.print_to_file('thingo.txt2')
mapObj.print_to_file('thingo.txt', mapObj.group_map)

# save the dimensions of the screen
screen_width = 100
screen_height = 50 + 1 # TODO kill the +1

# -----------------------------------------------------------------------------


# print out a given string starting at y,x
def putString(s, y, x):
    """
    """

    dx = 0
    for c in s:
        # print(c)
        libtcod.console_put_char(0, x+dx, y, str(c), libtcod.BKGND_NONE)
        dx += 1

# -----------------------------------------------------------------------------


# prints a box from y,x to dy-1,dx-1
def setGuidelines(y, x, dy, dx):
    """
    """

    # check the values provided.
    assert 0 <= y <= dy <= screen_height
    assert 0 <= x <= dx <= screen_width

    # guide lines are one less than the given max length.
    h = dy - 1
    w = dx - 1

    # print out the horizantal sides.
    for _x in range(x, dx-1):
        libtcod.console_put_char(0, _x, y, '-', libtcod.BKGND_NONE)
        libtcod.console_put_char(0, _x, h, '-', libtcod.BKGND_NONE)
    
    # print out the vertical sides.
    for _y in range(y, dy-1):
        libtcod.console_put_char(0, x, _y, '|', libtcod.BKGND_NONE)
        libtcod.console_put_char(0, w, _y, '|', libtcod.BKGND_NONE)
    
    # print out +'s on the verticies.
    libtcod.console_put_char(0, x, y, '+', libtcod.BKGND_NONE)
    libtcod.console_put_char(0, w, y, '+', libtcod.BKGND_NONE)
    libtcod.console_put_char(0, x, h, '+', libtcod.BKGND_NONE)
    libtcod.console_put_char(0, w, h, '+', libtcod.BKGND_NONE)

# -----------------------------------------------------------------------------


# prints out a given obj's group map, with header and side
# rulers.
def setMap(obj, y, x):
    """
    """

    # pull the group map.
    m = obj.group_map

    # print out the headers
    for _x in range(2, obj.width+2):
        libtcod.console_put_char(0, _x+x, 0+y, str((_x-2) % 10), libtcod.BKGND_NONE)
    for _x in range(2, obj.width+2):
        libtcod.console_put_char(0, _x+x, 1+y, '-', libtcod.BKGND_NONE)

    # reset the dy/dx variables
    _x, _y = 2, 2
    # for line in m.split('\n'):
    for line in m:
        libtcod.console_put_char(0, 0+x, _y+y, str((_y-2) % 10), libtcod.BKGND_NONE)
        libtcod.console_put_char(0, 1+x, _y+y, '|', libtcod.BKGND_NONE)

        # print all chars in the line.
        for char in line:
            libtcod.console_put_char(0, _x+x, _y+y, char, libtcod.BKGND_NONE)
            _x += 1

        # reset _x to 2,
        # inc _y.
        _y += 1
        _x = 2

    # map guide numbers and spaces accound for 8x and 4y
    # map box 
    # [2y,2x -> 32y,56x]
    setGuidelines(4-2, 4-2, 4+4+MAPh, 4+4+MAPw) 
    # box under map
    # ]34y,0x -> 35y,58x]
    setGuidelines(2+4+4+MAPh, 0, 2+4+4+MAPh, 2+4+4+MAPw) 
    # box right of map
    # [0y,58x -> 50y,58x]
    setGuidelines(0, 2+4+4+MAPw, screen_height, 2+4+4+MAPw) 

    # guide ruler
    for i in range(0, screen_width): 
        if i%10 == 0 or i%10 == 5:
            libtcod.console_put_char(0, i, 50, str(i % 10), libtcod.BKGND_NONE)        

    # print out some strings
    putString('Stats:', 1, 60)
    putString('Equip:', 3, 60)
    putString('Log:', 5, 60)
    putString('Enemies:', 7, 60)
    putString('Help:', 9, 60)
    putString('Keys', 11, 60)

    # box around screen
    setGuidelines(0, 0, screen_height-1, screen_width) # TODO kill the -1

# -----------------------------------------------------------------------------


# this is main
def main():

    libtcod.console_set_custom_font('courier12x12.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    # TODO
    # tcod_test.py:37: DeprecationWarning: A renderer should be given, see the online documentation.
    # libtcod.console_init_root(screen_width, screen_height, 'NecroPlanter', False)
    libtcod.console_init_root(screen_width, screen_height, 'NecroPlanter', False)

    # TODO
    # tcod_test.py:39: DeprecationWarning: Use the tcod.event module to check for "QUIT" type events.
    # while not libtcod.console_is_window_closed():
    while not libtcod.console_is_window_closed():
        
        # TODO
        # tcod_test.py:40: DeprecationWarning: Set the `con.default_fg` attribute instead.
        # libtcod.console_set_default_foreground(0, libtcod.white)
        libtcod.console_set_default_foreground(0, libtcod.white)

        libtcod.console_put_char(0, 1, 1, '@', libtcod.BKGND_NONE)
        libtcod.console_put_char(0, 5, 5, '#', libtcod.BKGND_NONE)
        libtcod.console_put_char(0, 6, 6, '$', libtcod.BKGND_NONE)
        
        # setMap(mapObj.print_groups())
        # print the map, starting it at 4,4
        setMap(mapObj, 4, 4)

        libtcod.console_flush()

        # tcod_test.py:47: DeprecationWarning: Use the tcod.event.get function to check for events.
        # key = libtcod.console_check_for_keypress()
        key = libtcod.console_check_for_keypress()

        if key.vk == libtcod.KEY_ESCAPE:
            return True

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
