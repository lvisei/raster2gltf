from interpolation import interpolation
from mesh import tin, meshExport
from stl2gltf import stl_to_gltf
import pandas as pd
import numpy as np

if __name__ == '__main__':
    data_db = pd.read_csv("./test-data/地表.csv",
                          delimiter=',', usecols=[2, 3, 4]).to_numpy()
    data_db_ztt = pd.read_csv("./test-data/地表-杂填土.csv",
                              delimiter=',', usecols=[2, 3, 6]).to_numpy()
    terrain_db = interpolation(data_db)
    terrain_db_ztt = interpolation(data_db_ztt)
    # print("terrain_db", terrain_db)

    vertices_db, triangles_db = tin(terrain_db)
    vertices_db_ztt, triangles_db_ztt = tin(terrain_db_ztt)

    # 翻转下部地面并移动三角网序号
    vertices_db_length = vertices_db.shape[0]
    triangles_db_ztt = triangles_db_ztt[:, ::-1]+vertices_db_length

    vertices_ztt = np.concatenate((vertices_db, vertices_db_ztt), axis=0)
    triangles_ztt = np.concatenate((triangles_db, triangles_db_ztt), axis=0)

    meshExport(vertices_ztt, triangles_ztt,
               "./output-data/ok-output.stl", binary=True)

    stl_to_gltf("./output-data/ok-output.stl",
                "./output-data/ok-output-gltf", False)
    # stl_to_gltf("./output-data/ok-output.stl", "./output-data/ok-output.glb", True)
