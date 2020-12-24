import struct
import operator
from gltflib import (
    GLTF, GLTFModel, Asset, Scene, Node, Mesh, Primitive, Attributes, Buffer, BufferView, Accessor, AccessorType,
    BufferTarget, ComponentType, GLBResource, FileResource)

# https://github.com/sergkr/gltflib

vertices = [
    (-4774424.719997984, 4163079.2597148907, 671001.6353722484),
    (-4748098.650098154, 4163079.259714891, 837217.8990777463),
    (-4689289.5292739635, 4246272.966707474, 742710.4976137652)
]

vertex_bytearray = bytearray()
for vertex in vertices:
    for value in vertex:
        vertex_bytearray.extend(struct.pack('f', value))
bytelen = len(vertex_bytearray)
mins = [min([operator.itemgetter(i)(vertex) for vertex in vertices])
        for i in range(3)]
maxs = [max([operator.itemgetter(i)(vertex) for vertex in vertices])
        for i in range(3)]
model = GLTFModel(
    asset=Asset(version='2.0'),
    scenes=[Scene(nodes=[0])],
    nodes=[Node(mesh=0)],
    meshes=[Mesh(primitives=[Primitive(attributes=Attributes(POSITION=0))])],
    buffers=[Buffer(byteLength=bytelen, uri='vertices.bin')],
    bufferViews=[BufferView(buffer=0, byteOffset=0, byteLength=bytelen,
                            target=BufferTarget.ARRAY_BUFFER.value)],
    accessors=[Accessor(bufferView=0, byteOffset=0, componentType=ComponentType.FLOAT.value, count=len(vertices),
                        type=AccessorType.VEC3.value, min=mins, max=maxs)]
)

resource = FileResource('vertices.bin', data=vertex_bytearray)
gltf = GLTF(model=model, resources=[resource])
gltf.export('./data/triangle.gltf')
