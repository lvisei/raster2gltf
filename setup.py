from interpolation import interpolation
from mesh import tin, meshExport
from stl2gltf import stl_to_gltf

if __name__ == '__main__':
    terrain = interpolation()
    # print("terrain", terrain)

    vertices, triangles = tin(terrain)
    meshExport(vertices, triangles, "./data/ok-output.stl", binary=True)

    stl_to_gltf("./data/ok-output.stl", "./data/ok-output-gltf", False)
    # stl_to_gltf("./data/ok-output.stl", "./data/ok-output.glb", True)
