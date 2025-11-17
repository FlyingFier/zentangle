import svgwrite

def add_zentangle_step(dwg, polygon_points, step, total_steps):
    #TODO: step calculation type implementation
    factor = 1 / (total_steps - step)
    # factor = 1 / total_steps

    # We need to start from 1 angle and move slightly inwards towards the next line
    # we got x points and keep replacing the point with a new point along the next line and do this iteratively for y steps.
    p0 = polygon_points[0]
    p1 = polygon_points[1]
    p2 = polygon_points[2]

    # find a new point along the line from p1 to p2
    def interpolate(pt1, pt2, t):
        return (pt1[0] + (pt2[0] - pt1[0]) * t, pt1[1] + (pt2[1] - pt1[1]) * t)

    p1_new = interpolate(p1, p2, factor)
    # create a triangle with p0, p1, p1_new
    points = [p0, p1, p1_new]
    triangle = dwg.polygon(points=points, fill="none", stroke="black", stroke_width=1)
    dwg.add(triangle)

    return [p1_new, *polygon_points[2:], polygon_points[0]]

def zentangle_polygon(dwg, polygon_points, steps):
    for step in range(steps):
        for __ in range(len(polygon_points)):
            polygon_points = add_zentangle_step(dwg, polygon_points, step, steps)

def zentanlge_from_points(points, steps):
    dwg = svgwrite.Drawing(size=(480, 480))
    zentangle_polygon(dwg, points, steps)
    return dwg

def main():
    dwg = svgwrite.Drawing("zentangling.svg", size=(500, 500))

    # points = [(100, 400), (250, 100), (400, 400)]
    points = [
        (100, 100),
        (400, 100),
        (400, 400),
        (100, 400)
    ]
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill="white"))
    triangle = dwg.polygon(points=points, fill="none", stroke="black", stroke_width=2)

    zentangle_polygon(dwg, points, steps=20)

    dwg.add(triangle)
    dwg.save()

if __name__ == '__main__':
    main()