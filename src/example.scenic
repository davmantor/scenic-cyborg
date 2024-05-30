import math

region = RectangularRegion( (0,0,0), 0, 20, 20)
workspace = Workspace(region)

ego = new Object on region, with shape SpheroidShape(),
        with width 2,
        with length 2,
        with height 2,
        facing (-90 deg, 45 deg, 0)


circle_radius = 2
N = 3
angle_increment = 360 / N

for i in range(N):
    angle = angle_increment * i
    radians = math.radians(angle)
    x = ego.position.x + circle_radius * math.cos(radians)
    y = ego.position.y + circle_radius * math.sin(radians)
    z = ego.position.z
    new Object at (x, y, z), with shape SpheroidShape(),
                 with width 1,
                 with length 1,
                 with height 1