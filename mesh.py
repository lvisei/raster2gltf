import quantized_mesh_encoder
from pydelatin import Delatin
from pydelatin.util import rescale_positions
import pykrige.kriging_tools as kt
import meshio
import pandas as pd


def tin(terrain, width=504, height=955):
    # https://github.com/kylebarron/pydelatin
    tin = Delatin(terrain, max_error=0.001,
                  border_size=1, border_height=1)
    vertices, triangles = tin.vertices, tin.triangles
    print("vertices", tin.vertices.shape)
    print("triangles", tin.triangles.shape)
    # pd.DataFrame(tin.vertices).to_csv("./data/vertices.csv")
    # pd.DataFrame(tin.triangles).to_csv("./data/triangles.csv")
    print("error", tin.error)

    return vertices, triangles


def meshExport(vertices, triangles, filePath, binary=False):
    points = vertices
    cells = [("triangle", triangles)]

    mesh = meshio.Mesh(points, cells)

    meshio.write(
        filePath,  # str, os.PathLike, or buffer/ open file
        mesh,
        # file_format="stl",  # optional if first argument is a path; inferred from extension
        binary=binary
    )


def meshExportTerrain(vertices, triangles, bounds):
    # Rescale vertices linearly from pixel units to world coordinates
    rescaled_vertices = rescale_positions(vertices, bounds)

    with open('./data/ok-output.terrain', 'wb') as f:
        quantized_mesh_encoder.encode(f, rescaled_vertices, triangles)


if __name__ == '__main__':

    grid_array, x, y, cellsize, no_data = kt.read_asc_grid("./data/ok-output.asc")

    vertices, triangles = tin(grid_array)
    meshExport(vertices, triangles, "./data/ok-output.stl", binary=False)
    # bounds = [x.min(), y.min(), x.max(), y.max()]
    # meshExportTerrain(vertices, triangles, bounds)
