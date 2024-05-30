import math
import random

region = RectangularRegion( (0,0,0), 0, 20, 20)
workspace = Workspace(region)

host1 = new Object on region, with shape SpheroidShape(),
        with width 2,
        with length 2,
        with height 2,
        facing (-90 deg, 45 deg, 0)

host2 = new Object on region, with shape SpheroidShape(),
        with width 2,
        with length 2,
        with height 2,
        facing (-90 deg, 45 deg, 0)

host3 = new Object on region, with shape SpheroidShape(),
        with width 2,
        with length 2,
        with height 2,
        facing (-90 deg, 45 deg, 0)

circle_radius = 2
N = 10
angle_increment = 360 / N

for i in range(random.randint(1,N)):
    angle = angle_increment * i
    radians = math.radians(angle)
    x = host1.position.x + circle_radius * math.cos(radians)
    y = host1.position.y + circle_radius * math.sin(radians)
    z = host1.position.z
    new Object at (x, y, z), with shape SpheroidShape(),
                 with width 1,
                 with length 1,
                 with height 1

for i in range(random.randint(1,N)):
    angle = angle_increment * i
    radians = math.radians(angle)
    x = host2.position.x + circle_radius * math.cos(radians)
    y = host2.position.y + circle_radius * math.sin(radians)
    z = host2.position.z
    new Object at (x, y, z), with shape SpheroidShape(),
                 with width 1,
                 with length 1,
                 with height 1

for i in range(random.randint(1,N)):
    angle = angle_increment * i
    radians = math.radians(angle)
    x = host3.position.x + circle_radius * math.cos(radians)
    y = host3.position.y + circle_radius * math.sin(radians)
    z = host3.position.z
    new Object at (x, y, z), with shape SpheroidShape(),
                 with width 1,
                 with length 1,
                 with height 1