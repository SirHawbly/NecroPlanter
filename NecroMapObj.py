#!/usr/local/bin/python3

# -----------------------------------------------------------------------------

"""
   Copyright (c) 2019 Christopher Bartlett
   [This program is licensed under the "MIT License"]
   Please see the file LICENSE in the source
   distribution of this software for license terms.
"""

# -----------------------------------------------------------------------------


import sqlite3
import random

# -----------------------------------------------------------------------------


class Coordinate(object):
    x = 0
    y = 0
    
    def __init__(self, _y, _x):
        self.x = _x
        self.y = _y

    def __eq__(self, o):
        return (self.y == o.y) and (self.x == o.x)

    def __str__(self):
        return '[{}, {} ]'.format(self.y, self.x)
    
    def __hash__(self):
        return id(self)

    def mod(self, c):
        return Coordinate(self.y + c.y, self.x + c.x)
      
    def distance(self, c):
        return abs(self.y - c.y) + abs(self.x - c.x)

# -----------------------------------------------------------------------------

class Map(object):

    # --
    space_val = 1
    space = ' '
    wall_val = 0
    wall = '#'

    # --
    height = 0
    width = 0
    map = []
    neighbors = []
    group_map = []
    groups = []

    # --
    coords = []
    walls = []
    spaces = []

    # --
    directions = [Coordinate(-1, 0), Coordinate(1, 0),
                    Coordinate(0, -1), Coordinate(0, 1)]
    num_alive = 0

    # -------------------------------------------------------------------------


    # constructor
    def __init__(self, h, w):
        """
        Given that the width and height are correct, then 
        instantiate an array for map, count the alive cells
        and get all neighbors.
        """

        # verify that the dimensions are positive.
        if (h <= 0) or (w <= 0):
            assert(False)

        # roll the random seed
        random.seed()

        # set the dimensions, and generate a map and list
        # of the neighbors.
        self.height = h
        self.width = w
        self.map = self.blank_array()
        self.neighbors = self.get_neighbors()

        # play the game of life twice, hopefully it is 
        # enough.
        for _ in range(0,2):
            self.game_of_life()

        self.update_map()

        # finish up the map, connecting the groups inside.
        # self.finalize_map()

    # -------------------------------------------------------------------------

    # updates the map after it has changed
    def update_map(self):
        """
        TODO
        """

        # count the amount of cells that are alive, and
        # create a list of all the groups insite.
        self.num_alive = self.count_alive()
        
        self.coords = self.make_coord_list()
        self.walls = [x for x in self.coords if self.map_coord(x) == self.wall_val]
        self.spaces = [y for y in self.coords if self.map_coord(y) == self.space_val]
        self.groups = self.get_groupings()
        self.make_group_map()
        self.connect_groups()

    # tostring()
    def __str__(self):
        dim = '[{} by {}] '.format(self.height, self.width)
        stats = 'with {} spaces'.format(self.num_alive)
        return dim + stats

    # -------------------------------------------------------------------------
    

    # returns an array of strings 
    def get_group_string(self):
        """
        TODO
        """

        m = []

        for row in self.group_map:
            m += [str(row) + '\n']

        return m

    # -------------------------------------------------------------------------


    # Given a y and an x, verify that it is in the bounds
    # of the map array.
    def in_bounds(self, y, x):
        """
        Check that both the y and x coordinates that were 
        passed in are in bounds (between 0 and their 
        corresponding bound), return if both are in range.
        """

        return (0 <= y < self.height) and (0 <= x < self.width)

    # -------------------------------------------------------------------------


    # return the value in map of a coordinate pair, -1 is 
    # returned if the bounds are out of the map's scope.
    def map_coord(self, coord):
        """
        Return the value in the map that corresponds to a 
        given coordinate variable. check that the 
        components are in bounds first.
        """

        # if we arenty in bounds return -1
        if (not self.in_bounds(coord.y, coord.x)):
            return -1

        # else we can return the map value
        return self.map[coord.y][coord.x]

    # -------------------------------------------------------------------------


    # assert that all of the rows in the array (a) are of 
    # size width, and that there are size length of them.
    def assert_array_size(self, fun_name, a):
        """
        Assert that all rows in the map are of size width,
        and that there are height amount of rows in map.
        if this is not the case, kill the program, and 
        print out an error message.
        """

        # form a error header.
        error = '{} - '.format(fun_name)

        # go through all rows in the map...
        for row in a:

            # verify that each row is of correct length.
            # print(len(j), self.width)
            assert((len(row) == self.width), error + 'bad row length')
        
        # verify that there are the right amount of rows in
        # the map.
        # print(len(self.map), self.height)
        assert((len(a) == self.height), error + 'bad amount of rows')

        return 

    # -------------------------------------------------------------------------


    # generates an array of H rows of 0s and 1s W long
    def blank_array(self):
        """
        Create an array that is Height long, by creating 
        rows that are Width long. These rows are either
        walls or spaces, depending on a random value. Then
        return it out.
        """

        # set up a return list.
        return_array = []

        # for height times, add a row to the return list
        for _ in range(0, self.height):

            temp = []

            # for width times, add a random bit into the 
            # current row.
            for _ in range(0, self.width):
                r = random.randint(0, 1)
                temp += [self.space_val] if r == 0 else [self.wall_val]

            # add the row into the return array.
            return_array += [temp]

        # check the old map value, then return the array
        self.assert_array_size('blank_array', return_array)
        return return_array

    # -------------------------------------------------------------------------


    # counts all of the alive cells inside of the map array
    def count_alive(self):
        """
        Scroll through the map array, tracking of number of 
        values in it that match the saved space value. 
        """

        # set the alive count to 0
        num_alive = 0

        # run through all cells in the map array, and if 
        # the cell is a space cell, increment the alive 
        # value.
        for j in range(0, self.height):
            for i in range(0, self.width):
                if (self.map[j][i] == self.space_val):
                    num_alive += 1

        # check the map contents, and return the alive val.
        self.assert_array_size('count_alive', self.map)
        return num_alive

    # -------------------------------------------------------------------------


    # get the count of all of the neighboring cells that 
    # are considered alive (spaces).
    def get_point_neighbor(self, y, x):
        """
        Given a coordinate into the map array, check all
        neighboring cells, tallying up all of them that are
        alive. Skips all of the coordinates that are point-
        ing to the given coordinate, or that don't lie in
        the bounds of the array.
        """

        # set count to 0
        count = 0

        # go through all of the possible combinations of 
        # moves you can make from a cell
        for j in [-1, 0, 1]:
            for i in [-1, 0, 1]:

                # if the move is [0,0] or out of bounds we
                # skip it.
                if not 0 <= y+j < self.height:
                    continue
                elif not 0 <= x+i < self.width:
                    continue
                elif [j, i] == [0, 0]:
                    continue

                # else, if we have a space value, increment
                # count.
                elif self.map[y+j][x+i] == self.space_val:
                    count += 1

        # check the map contents, and return the count 
        # value.
        self.assert_array_size('get_point_neighbor', self.map)
        return count

    # -------------------------------------------------------------------------


    # pulls an array of neighbor counts and return it as an 
    def get_neighbors(self):
        """
        Pulls all the neighbor counts from all of the cells
        inside of the map array. It then stores all of them
        into an array which is then returned.
        """

        # create an empty list for neighbors.
        neighbors = []

        # go through all of the rows in the map array
        for j in range(0, self.height):
          
            row = []
            
            # go through the items in the row, and add the 
            # amount of neighbors that item has to the 
            # array.
            for i in range(0, self.width):
                row += [self.get_point_neighbor(j, i)]

            # add the row into the neighbors array.
            neighbors += [row]

        # check the map, and return the neighbors array.
        self.assert_array_size('get_neighbors', self.neighbors)
        return neighbors

    # -------------------------------------------------------------------------


    # create a list of coordinate tuples based off of the
    # map dimensions
    def make_coord_list(self):
        """
        create and return a list of the possible coordinate 
        that can be accessed in the map, then return it 
        out.
        """

        cs = []

        # for all coordinate combinations, create a 
        # coordinate obj, and add it to cs
        for j in range(0, self.height):
            for i in range(0, self.width):
                cs += [Coordinate(j,i), ]

        # print(cs)
        
        # check the map contents, and return the coordinate
        # list
        self.assert_array_size('make_coord_list', self.map)
        return cs

    # -------------------------------------------------------------------------


    # gives a list of lists, that represents all the groups
    # inside of the map.
    def get_groupings(self):
        """
        Parses the map and returns a list of all the groups
        inside of it that are bounded by walls.
        """

        # set up the groups return value
        contig_groups = []
        seen_coords = []
        
        for c in self.spaces:
            
            if c in seen_coords:
                continue

            new_coords = [c]
            old_coords = []

            while True:
                
                try:
                    t = new_coords.pop()

                    # if the item in this list has been 
                    # looked at, skip it.
                    if t in seen_coords:
                        continue

                    # add it to the old list, we dont need
                    # to search it again.
                    old_coords += [t]

                    # generate the cardinal cells that are 
                    # around the current coord.
                    dirs = [x.mod(t) for x in self.directions]

                    # go through all the cardinal directions
                    # and check if they are space cells.
                    for d in dirs:
                        if self.map_coord(d) == self.space_val:
                            # print('d in spaces', d)
                            new_coords += [d]

                    # we have searched all around t, we 
                    # can put it into seen.
                    seen_coords += [t]

                except:
                    # print('list exhausted')
                    break
            
            # add the last group into the contiguous list.
            contig_groups += [old_coords]

        # return the list of groups
        return contig_groups

    # -------------------------------------------------------------------------


    # function to set the group_map variable after the map
    # and groups list has been made.
    def make_group_map(self):
        """
        sets the group_map variable to be an array of 
        arrays that holds a version of the map, but with 
        different a specific letter to represent all items
        inside of a contiguous group.
        """
      
        # set the map to nil, then fill it with rows of 
        # spaces to represent the walls in the map
        self.group_map = []
        for _ in range(0, self.height):
            temp = []
            for _ in range(0, self.width):
                temp += [' ']
            self.group_map += [temp]

        # start at group number 0, and set the value in the
        # group's cells to 65 + group number, and convert
        # it into a char. (chr(65) == 'A')
        g_num = 0 
        for group in self.groups:
            for c in group:
                self.group_map[c.y][c.x] = str(chr(g_num + 65))
            g_num += 1

        self.assert_array_size('make_group_map', self.group_map)

    # -------------------------------------------------------------------------


    # run game of life with the walls being the alive type
    # of cells.
    def game_of_life(self):
        """
        Snakes through the neighbors array, and checks the 
        values of different cooridnates, based on the given
        value, it either: dies, grows, or lives. Then it 
        updates the neighbors array.
        """

        # update the number of neighbors for all coords.
        self.neighbors = self.get_neighbors()

        # go through all of the cells in the map,. and play
        # the Game of Life, with them based off neighbors.
        for j in range(0, self.height):
            for i in range(0, self.width):
            
                # dies of under population
                if (0 <= self.neighbors[j][i] <= 1):
                    self.map[j][i] = self.space_val
                # survives if alive
                elif (2 <= self.neighbors[j][i] <= 3):
                    self.map[j][i] = self.map[j][i]
                # becomes alive if 4
                elif (4 == self.neighbors[j][i]):
                    self.map[j][i] = self.wall_val
                # dies of over population
                if (5 <= self.neighbors[j][i]):
                    self.map[j][i] = self.space_val

        # check to see if the array sizes are alright.
        self.assert_array_size('game_of_life', self.map)

        # update the number of neighbors for all coords.
        self.neighbors = self.get_neighbors()

        # return out
        return

    # -------------------------------------------------------------------------
    

    # TODO
    # connects all the items in the groups to make a larger
    # contigous map.
    def connect_groups(self):
        """
        connect all groups of coordinates that are less 
        then a specific value
        """
        """
        end_group = [self.groups[0]]

        if len(self.groups) == 1:
            return end_group

        for group in self.groups[1:]:
            
            if len(group) < 5: 
                continue
            
            print(len(group))

            closest_coord = group[0]
            closest_dist = self.width
            for coord in group[1:]:
                for point in end_group:
                    if coord.distance(point) < closest_dist:
                        closest_coord = point
                        closest_dist = coord.distance(point)

            print(closest_coord, closest_dist)
        """

        return False

    # -------------------------------------------------------------------------
    

    # TODO
    def get_map_string(self):
        """
        TODO
        """

        text = ''
        
        for j in range(0, 2):
            if (j == 0): text += '   '
            else: text += ' |'

            # for each column in the row, print out the col
            # number, or a hyphen if its the second row
            for i in range(0, self.width):

                if (j == 0): 
                    text += '{} '.format((i%10+1)%10)
                else: 
                    text += '--'

            if j == 0: 
                text += '\n' 
            else:
                text += '-|\n'

        for row, i in zip(self.group_map, range(0, len(self.map))):

            text += str((i%10+1)%10) + '| '

            for char in row:
                text += char + ' '

            if j == 0: m += '\n' 
            else: text += '|\n'
        
        text += ' |'

        for i in range(0, self.width):
            text += '--'
    
        text += '-|'

        return text


    # -------------------------------------------------------------------------


    # print out the headers for the print map and neighbor
    # functions.
    def print_header(self):
        """
        Prints a row of the column names which are the 
        indecies into a given row.
        """

        text = ''

        # print out the starting two chars for the first 
        # two rows
        for j in range(0, 2):
            
            if (j == 0):
                text += '   '
                # print('   ', end='')
            else: 
                text += ' |'
                # print(' |', end='')

            # for each column in the row, print out the col
            # number, or a hyphen if its the second row
            for i in range(0, self.width):
                
                if (j == 0): 
                    text += '{} '.format(i%10)
                    # print('{}'.format(i%10), end=' ')
                else: 
                    text += '--'
                    # print('--', end='')

            text += '\n'
            # print()

        # check the map array.
        self.assert_array_size('print_header', self.map)
        return text

    # -------------------------------------------------------------------------


    # prints the map out with headers and wall and space 
    # characters instead of values.
    def print_map(self):
        """
        Prints out all rows in the map with corresponding
        row numbers.
        """

        text = ''

        # print out a starting message, and print headers.
        # print('printing map')
        text += self.print_header()

        # print out the row numbers and the contents of the
        # rows, with the values in the map represented by
        # space and wall characters.
        for j in range(0, self.height):

            text += '{}| '.format(j%10)
            # print('{}|'.format(j%10), end=' ')

            for i in range(0, self.width):

                if (self.map[j][i] == self.space_val):
                    text += '{} '.format(self.space)
                    # print(self.space, end=' ')

                else: 
                    text += '{} '.format(self.wall)
                    # print(self.wall, end=' ')

            text += '\n'
            # print()

        # print the ending message, then check the map.
        # print('end of map\n')
        self.assert_array_size('print_map', self.map)
        return text

    # -------------------------------------------------------------------------


    # prints out all of the contents of the neighbors 
    # array.
    def print_neighbors(self):
        """
        prints out all values of the neighbors in the 
        neighbors array, with corresponding row numbers.
        """

        text = ''

        # print out a status message, and headers.
        # print('printing neighbors')
        text += self.print_header()

        # go through all cells in the map, printing the row 
        # number before the row's contents
        for j in range(0, self.height):
        
            text += '{}| '.format((1+j)%10)
            # print('{}|'.format((1+j)%10), end=' ')
        
            for i in range(0, self.width):
                text += '{} '.format(self.neighbors[j][i])
                # print(self.neighbors[j][i], end=' ')
        
            text += '\n'
            # print()

        # print out the end message, and check the map
        # print('end of neighbors\n')
        self.assert_array_size('print_neighbors', self.neighbors)

        return text

    # -------------------------------------------------------------------------


    # print the map by groups
    def print_groups(self):
        """
        print out the map using the current groups that are
        stored. uses a char to designate a grouping (starts
        at 'a'), with walls being spaces.
        """

        text = ''

        # print out a starting message, and print headers.
        # print('printing groups')
        text += self.print_header()

        # print out the row numbers and the contents of the
        # rows, with the values in m represented by groups
        # and wall characters.
        for j in range(0, self.height):

            text += '{}| '.format(j%10)
            # print('{}|'.format(j%10), end=' ')
          
            for i in range(0, self.width):
                text += '{} '.format(self.group_map[j][i])
                # print(self.group_map[j][i], end=' ')

            text += '\n'
            # print()

        # print the ending message, then check the map.
        # print('end of groups\n')
        self.assert_array_size('print_groups', self.group_map)
        
        return text

    # -----------------------------------------------------------------------------


    # write the array (a) to a specified output file.
    def print_to_file(self, output, a):
        """
        writes an array to the provided file, with spaces 
        to delimit the different cells.
        """

        # open the output file, deleting the past version
        with open(output, 'w+') as output_file:
            for line in a:

                out_line = ''
              
                # go through the lines in the array, adding all
                # items with a space after. add '\n' at the end
                for item in line:
                    # print(item)
                    out_line += item + ' '

                output_file.write(out_line + '\n')

        self.assert_array_size('print_to_file', a)
        return

# -----------------------------------------------------------------------------


# if this file is run 
if __name__ == '__main__':
    
    x = Map(24, 48)
    print('making a map: ' + str(x) + '\n')

    # print out the 3 different maps that are created upon
    # creation.
    
    # x.print_map()
    print( x.print_map() )

    # x.print_neighbors()
    print( x.print_neighbors() )

    # x.print_groups()
    print( x.print_groups() )
    
    # write groups to file 
    x.print_to_file('thingo.txt', x.group_map)
    
    # 
    # x.read_from_file('thingo.txt')

# -----------------------------------------------------------------------------
