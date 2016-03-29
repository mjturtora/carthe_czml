#    Copyright (C) 2016 Michael Turtora
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

from datetime import datetime
from decimal import Decimal
from czml import czml

if __name__ == "__main__":
    glad = []
    i = 0
    #carthe_name = []
    with open('GLAD_15min_filtered\GLAD_15min_filtered.dat', 'r') as f:
        while True:
            line = f.readline()
            if len(line) == 0:
                break
            elif line[0] != '%':
                if len(glad) == 0:
                    glad.append(line.split())
                    #carthe_name.append(line.split()[0])
                    #print glad[len(glad)-1][0]
                    print glad
                elif glad[len(glad)-1][0] != line.split()[0]:
                    i += 1
                    if i > 1:
                        break
                    else:
                        glad.append(line.split())
                else:
                    glad.append(line.split())
                    #carthe_name.append(line.split()[0])


    print glad[-1]
    cartographic_position = []
    i = 0
    for row in glad:
        #if i < 1000:  # limit for testing
            #i += 1
        cartographic_position.append(datetime.strptime(row[1] + ' ' + row[2],
                                    "%Y-%m-%d %H:%M:%S.%f")
        )
        latitude = Decimal(row[3].strip("'"))
        longitude = Decimal(row[4].strip("'"))
        #print latitude, longitude
        cartographic_position.append(longitude)
        cartographic_position.append(latitude)
        cartographic_position.append(100)

    print cartographic_position
    '''

    # Build list of unique names and print number
    unique_names = []
    for n in carthe_name:
        if n not in unique_names:
            unique_names.append(n)
            print n
    print 'Number of names = ', len(unique_names)
    # 297 individual drifters (unique names)
    # Create datetime objects for first i rows
    i = 0
    for row in glad:
        if i < 100000:  # limit for testing
            i += 1
            dt_object = datetime.strptime(row[1] + ' ' + row[2],
                                          "%Y-%m-%d %H:%M:%S.%f")
            #print datetime.strftime(dt_object, "%Y-%m-%d %H:%M:%S.%f")

    '''
    # build position list
    # Create a new point
    drifter_name = czml.Label(text='CARTHE_001')
    point = czml.Point(pixelSize=3,
                       color={'rgba': [255, 255, 255, 255]},
                       outlineWidth=1,
                       outlineColor={'rgba': [0, 0, 0, 255]},
                       show=True
                       )

    # Setup path variables
    sc = czml.SolidColor(color={'rgba': [0, 0, 255, 255]})
    m1 = czml.Material(solidColor=sc)
    v1 = czml.Position(cartographicDegrees=cartographic_position)
    # test example loads position into Path. Doesn't seem to work right.
    p1 = czml.Path(show=True, width=1, leadTime=0, trailTime=650000,
                   resolution=5, material=m1)  #, position=v1)
    print p1

    # Initialize a document
    doc = czml.CZML()

    # Create and append the document packet (could add a doc id here)
    packet1 = czml.CZMLPacket(id='document', version='1.0')
    doc.packets.append(packet1)

    # initialize path packet with id, then load with other items
    # packet2 = czml.CZMLPacket(id=glad[0][0]) # drifter name for id
    packet2 = czml.CZMLPacket(id='path')  # hard wired for now.
    packet2.point = point
    packet2.label = drifter_name
    # packet2.availability = "2012-07-20T10:00:00Z/2012-10-09T15:00:00Z"
    packet2.availability = "2012-07-20T05:15:00.143960Z/2012-10-08T05:00:22Z"
    packet2.path = p1
    packet2.position = v1
    doc.packets.append(packet2)

    # Write the CZML document to a file
    filename = "example.czml"
    doc.write(filename)


