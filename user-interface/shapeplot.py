''''import shapefile as shp
import matplotlib.pyplot as plt
from descartes import PolygonPatch


sf = shp.Reader("GBR_adm/GBR_adm0")
shapes = sf.shapes()
records = sf.records()

plt.figure()
for shape in shapes:
    x = [i[0] for i in shape.points]
    y = [i[1] for i in shape.points]
    plt.plot(x,y)
    # for point in shape.points:
    #     x,y = point
    #     plt.plot(x,y)
    break

fig = plt.figure()
ax = fig.gca()
BLUE = '#6699cc'
poly = sf.iterShapes().next().__geo_interface__
ax.add_patch(PolygonPatch(poly, fc=BLUE, ec=BLUE, alpha=0.5, zorder=2 ))
ax.axis('scaled')
#plt.show()

plt.show()

# for shape in shapes:
#      print shape.shapeType
#      for part in shape.parts:
#          print part
#
# for record in records:
#     print record
# for name in dir(shapes):
#      if not name.startswith('__'):
#          print name

# plt.figure()
# for shape in sf.shapeRecords():
#     x = [i[0] for i in shape.shape.points[:]]
#     y = [i[1] for i in shape.shape.points[:]]
#     #print x, ",", y
#     plt.plot(x,y)
# plt.show()'''''