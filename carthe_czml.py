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

# run in terria with:
# http://comt.sura.org/proxy_3001#https://raw.githubusercontent.com/mjturtora/carthe_czml/master/TerriaJS%20Files/CARTHE_JSON.json


from datetime import datetime
from decimal import Decimal
from czml import czml


def read_file(number_to_read):
    glad = []
    i = 1
    with open('..\data\GLAD_15min_filtered\GLAD_15min_filtered.dat', 'r') as f:
        while True:
            line = f.readline()
            # file ends with blank line
            if len(line) == 0:
                break
            # header rows start with '%'
            elif line[0] != '%':
                if len(glad) == 0:
                    glad.append(line.split())
                # test for new drifter name, just to make testing quicker.
                elif glad[len(glad) - 1][0] != line.split()[0]:
                    i += 1
                    if i > number_to_read:
                        break
                    else:
                        glad.append(line.split())
                else:
                    glad.append(line.split())
    return glad


def build_drifter_dict(glad):
    drifter_dict = {}
    cartographic_position = []
    i = 0
    drifter = glad[0][0]
    for row in glad:
        # next two rows alter time span and interval
        if i < 4 and drifter == row[0]:  # very large number to read all (400000)
            if (int(i) % 4) != 0:  # 4 for hourly from 15 min data
                i += 1
                continue
            # todo: still ugly but better:
            drifter_dict, cartographic_position = extract_drifter_data(
                cartographic_position, drifter_dict, row)
            i += 1
        elif row[0] != drifter:
            drifter = row[0]
            cartographic_position = []
            i = 1
            drifter_dict, cartographic_position = extract_drifter_data(
                cartographic_position, drifter_dict, row)
    return drifter_dict


def extract_drifter_data(cartographic_position, drifter_dict, row):
    # todo: verify proper time zone handling
    dt = datetime.strptime(row[1] + ' ' + row[2], "%Y-%m-%d %H:%M:%S.%f")
    dt = dt.replace(microsecond=0)
    cartographic_position.append(dt)
    # print datetime.strftime(dt_object, "%Y-%m-%d %H:%M:%S.%f")
    latitude = Decimal(row[3].strip("'"))  # test if strip is really needed
    longitude = Decimal(row[4].strip("'"))
    # print latitude, longitude
    cartographic_position.append(longitude)
    cartographic_position.append(latitude)
    cartographic_position.append(0)  # assume zero elevation
    drifter_dict[row[0]] = cartographic_position
    return drifter_dict, cartographic_position


def get_drifter_names(glad):
    # Build list of unique names and print number (initial inventory step)
    unique_names = []
    for row in glad:
        if row[0] not in unique_names:
            unique_names.append(row[0])
    print 'Number of names = ', len(unique_names)
    print unique_names
    # get 297 individual drifters (unique names)
    return unique_names


if __name__ == "__main__":
    # input data and build dictionary
    # argument restricts number of drifters read for testing
    glad = read_file(number_to_read=3)  # 300 for max
    # print 'glad length = ', len(glad)
    # unique_names = get_drifter_names(glad)

    # load position data into dict keyed by drifter id
    drifter_dict = build_drifter_dict(glad)

    # set constant properties

    # Define a standard point style (could get fancy later, color groups might be fun)
    point = czml.Point(pixelSize=3,
                       color={'rgba': [255, 255, 255, 255]},
                       outlineWidth=1,
                       outlineColor={'rgba': [0, 0, 0, 255]},
                       show=True
                       )

    '''
    # test example loads position into Path. Doesn't seem to work right.
    # ...and path awfully slow so skip it.
    m1 = czml.Material(solidColor=czml.SolidColor(color={'rgba': [0, 0, 255, 255]}))
    p1 = czml.Path(show=True, width=1, leadTime=0, trailTime=650000,
                   resolution=5, material=m1)  # , position=v1)
    '''

    # Initialize a document
    doc = czml.CZML()

    # Create and append the document packet
    packet1 = czml.CZMLPacket(id='document',
                              name='CARTHE GLAD Drifter data',  # but name not implemented
                              version='1.0')
    doc.packets.append(packet1)

    # for each drifter, initialize packet with id, then load with other items
    for drifter in drifter_dict:
        packet = czml.CZMLPacket(id=drifter)
        print drifter

        packet.description = czml.Description(string=drifter)
        packet.point = point

        '''
        # drop all label stuff but leave code for later
        # todo: figure out why label properties aren't working, but labels are too messy
        # with all the points anyway.
        drifter_name = czml.Label(text=drifter[-3:], show=True)
        drifter_name.scale = 0.5
        drifter_name.fillColor = {'rgba': [255, 255, 255, 255]}
        drifter_name.labelStyle = "FILL_AND_OUTLINE"
        drifter_name.horizontalOrigin = "Left"
        packet.label = drifter_name
        '''

        # todo: vary availability by drifter or set global in doc packet
        # todo: get distribution of times
        packet.availability = "2012-07-20T05:15:00.143960Z/2012-10-23T05:00:22Z"
        packet.position = czml.Position(cartographicDegrees=drifter_dict[drifter])

        doc.packets.append(packet)
        del packet

    # Write the CZML document to a file
    filename = "..\output\example.czml"
    doc.write(filename)
