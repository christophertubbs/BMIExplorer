/** Static mirror of BMI Explorer fixtures; no Python runs in the browser.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
export const BASELINE = {
  "description": "Nine coexisting grids: scalar; uniform/rectilinear/points ranks 2 and 3; unstructured ranks 1 and 2.",
  "grids": [
    {
      "kind": "scalar",
      "shape": [],
      "spacing": [],
      "origin": [],
      "label": "scalar",
      "rank": 0,
      "x": [],
      "y": [],
      "z": [],
      "edge_nodes": [],
      "face_nodes": [],
      "face_edges": [],
      "nodes_per_face": []
    },
    {
      "kind": "uniform_rectilinear",
      "shape": [
        3,
        4
      ],
      "spacing": [
        2.0,
        5.0
      ],
      "origin": [
        10.0,
        100.0
      ],
      "label": "uniform_2d",
      "rank": 2,
      "x": [],
      "y": [],
      "z": [],
      "edge_nodes": [],
      "face_nodes": [],
      "face_edges": [],
      "nodes_per_face": []
    },
    {
      "kind": "uniform_rectilinear",
      "shape": [
        2,
        3,
        4
      ],
      "spacing": [
        7.0,
        2.0,
        5.0
      ],
      "origin": [
        0.0,
        10.0,
        100.0
      ],
      "label": "uniform_3d",
      "rank": 3,
      "x": [],
      "y": [],
      "z": [],
      "edge_nodes": [],
      "face_nodes": [],
      "face_edges": [],
      "nodes_per_face": []
    },
    {
      "kind": "rectilinear",
      "shape": [
        3,
        4
      ],
      "spacing": [],
      "origin": [],
      "label": "rectilinear_2d",
      "rank": 2,
      "x": [
        100.0,
        102.0,
        107.0,
        115.0
      ],
      "y": [
        10.0,
        11.0,
        14.0
      ],
      "z": [],
      "edge_nodes": [],
      "face_nodes": [],
      "face_edges": [],
      "nodes_per_face": []
    },
    {
      "kind": "rectilinear",
      "shape": [
        2,
        3,
        4
      ],
      "spacing": [],
      "origin": [],
      "label": "rectilinear_3d",
      "rank": 3,
      "x": [
        100.0,
        102.0,
        107.0,
        115.0
      ],
      "y": [
        10.0,
        11.0,
        14.0
      ],
      "z": [
        0.0,
        7.0
      ],
      "edge_nodes": [],
      "face_nodes": [],
      "face_edges": [],
      "nodes_per_face": []
    },
    {
      "kind": "points",
      "shape": [],
      "spacing": [],
      "origin": [],
      "label": "points_2d",
      "rank": 2,
      "x": [
        0.0,
        2.0,
        3.0,
        1.0,
        -1.0,
        1.0
      ],
      "y": [
        0.0,
        0.0,
        2.0,
        3.0,
        2.0,
        1.0
      ],
      "z": [],
      "edge_nodes": [],
      "face_nodes": [],
      "face_edges": [],
      "nodes_per_face": []
    },
    {
      "kind": "points",
      "shape": [],
      "spacing": [],
      "origin": [],
      "label": "points_3d",
      "rank": 3,
      "x": [
        0.0,
        2.0,
        3.0,
        1.0,
        -1.0,
        1.0
      ],
      "y": [
        0.0,
        0.0,
        2.0,
        3.0,
        2.0,
        1.0
      ],
      "z": [
        0.0,
        1.0,
        4.0,
        2.0,
        5.0,
        3.0
      ],
      "edge_nodes": [],
      "face_nodes": [],
      "face_edges": [],
      "nodes_per_face": []
    },
    {
      "kind": "unstructured",
      "shape": [],
      "spacing": [],
      "origin": [],
      "label": "unstructured_edges",
      "rank": 1,
      "x": [
        0.0,
        2.0,
        5.0,
        9.0
      ],
      "y": [],
      "z": [],
      "edge_nodes": [
        0,
        1,
        1,
        2,
        2,
        3
      ],
      "face_nodes": [],
      "face_edges": [],
      "nodes_per_face": []
    },
    {
      "kind": "unstructured",
      "shape": [],
      "spacing": [],
      "origin": [],
      "label": "unstructured_mixed",
      "rank": 2,
      "x": [
        0.0,
        2.0,
        3.0,
        1.0,
        -1.0,
        1.0
      ],
      "y": [
        0.0,
        0.0,
        2.0,
        3.0,
        2.0,
        1.0
      ],
      "z": [],
      "edge_nodes": [
        0,
        1,
        1,
        2,
        2,
        3,
        3,
        4,
        4,
        0,
        1,
        5,
        3,
        5,
        0,
        5
      ],
      "face_nodes": [
        1,
        2,
        3,
        5,
        3,
        4,
        0,
        5,
        0,
        1,
        5
      ],
      "face_edges": [
        1,
        2,
        6,
        5,
        3,
        4,
        7,
        6,
        0,
        5,
        7
      ],
      "nodes_per_face": [
        4,
        4,
        3
      ]
    }
  ],
  "variables": [
    {
      "name": "scalar__value",
      "initial": [
        42.0
      ],
      "units": "1",
      "grid": 0,
      "location": "node",
      "dtype": "float64",
      "primitive": "double",
      "readable": true,
      "writable": true,
      "evolving": true
    },
    {
      "name": "uniform_2d__value",
      "initial": [
        0.0,
        1.0,
        2.0,
        3.0,
        4.0,
        5.0,
        6.0,
        7.0,
        8.0,
        9.0,
        10.0,
        11.0
      ],
      "units": "1",
      "grid": 1,
      "location": "node",
      "dtype": "float64",
      "primitive": "double",
      "readable": true,
      "writable": true,
      "evolving": true
    },
    {
      "name": "uniform_3d__value",
      "initial": [
        0.0,
        1.0,
        2.0,
        3.0,
        4.0,
        5.0,
        6.0,
        7.0,
        8.0,
        9.0,
        10.0,
        11.0,
        12.0,
        13.0,
        14.0,
        15.0,
        16.0,
        17.0,
        18.0,
        19.0,
        20.0,
        21.0,
        22.0,
        23.0
      ],
      "units": "1",
      "grid": 2,
      "location": "node",
      "dtype": "float64",
      "primitive": "double",
      "readable": true,
      "writable": true,
      "evolving": true
    },
    {
      "name": "rectilinear_2d__value",
      "initial": [
        0.0,
        1.0,
        2.0,
        3.0,
        4.0,
        5.0,
        6.0,
        7.0,
        8.0,
        9.0,
        10.0,
        11.0
      ],
      "units": "1",
      "grid": 3,
      "location": "node",
      "dtype": "float64",
      "primitive": "double",
      "readable": true,
      "writable": true,
      "evolving": true
    },
    {
      "name": "rectilinear_3d__value",
      "initial": [
        0.0,
        1.0,
        2.0,
        3.0,
        4.0,
        5.0,
        6.0,
        7.0,
        8.0,
        9.0,
        10.0,
        11.0,
        12.0,
        13.0,
        14.0,
        15.0,
        16.0,
        17.0,
        18.0,
        19.0,
        20.0,
        21.0,
        22.0,
        23.0
      ],
      "units": "1",
      "grid": 4,
      "location": "node",
      "dtype": "float64",
      "primitive": "double",
      "readable": true,
      "writable": true,
      "evolving": true
    },
    {
      "name": "points_2d__value",
      "initial": [
        0.0,
        1.0,
        2.0,
        3.0,
        4.0,
        5.0
      ],
      "units": "1",
      "grid": 5,
      "location": "node",
      "dtype": "float64",
      "primitive": "double",
      "readable": true,
      "writable": true,
      "evolving": true
    },
    {
      "name": "points_3d__value",
      "initial": [
        0.0,
        1.0,
        2.0,
        3.0,
        4.0,
        5.0
      ],
      "units": "1",
      "grid": 6,
      "location": "node",
      "dtype": "float64",
      "primitive": "double",
      "readable": true,
      "writable": true,
      "evolving": true
    },
    {
      "name": "unstructured_edges__value",
      "initial": [
        0.0,
        1.0,
        2.0,
        3.0
      ],
      "units": "1",
      "grid": 7,
      "location": "node",
      "dtype": "float64",
      "primitive": "double",
      "readable": true,
      "writable": true,
      "evolving": true
    },
    {
      "name": "unstructured_mixed__value",
      "initial": [
        0.0,
        1.0,
        2.0,
        3.0,
        4.0,
        5.0
      ],
      "units": "1",
      "grid": 8,
      "location": "node",
      "dtype": "float64",
      "primitive": "double",
      "readable": true,
      "writable": true,
      "evolving": true
    },
    {
      "name": "unstructured_mixed__edge_value",
      "initial": [
        10.0,
        11.0,
        12.0,
        13.0,
        14.0,
        15.0,
        16.0,
        17.0
      ],
      "units": "1",
      "grid": 8,
      "location": "edge",
      "dtype": "float64",
      "primitive": "double",
      "readable": true,
      "writable": true,
      "evolving": true
    },
    {
      "name": "unstructured_mixed__face_value",
      "initial": [
        20.0,
        21.0,
        22.0
      ],
      "units": "1",
      "grid": 8,
      "location": "face",
      "dtype": "float64",
      "primitive": "double",
      "readable": true,
      "writable": true,
      "evolving": true
    },
    {
      "name": "scalar__int8",
      "initial": [
        7
      ],
      "units": "1",
      "grid": 0,
      "location": "node",
      "dtype": "int8",
      "primitive": "signed char",
      "readable": true,
      "writable": true,
      "evolving": false
    },
    {
      "name": "scalar__uint8",
      "initial": [
        7
      ],
      "units": "1",
      "grid": 0,
      "location": "node",
      "dtype": "uint8",
      "primitive": "unsigned char",
      "readable": true,
      "writable": true,
      "evolving": false
    },
    {
      "name": "scalar__int16",
      "initial": [
        7
      ],
      "units": "1",
      "grid": 0,
      "location": "node",
      "dtype": "int16",
      "primitive": "short",
      "readable": true,
      "writable": true,
      "evolving": false
    },
    {
      "name": "scalar__uint16",
      "initial": [
        7
      ],
      "units": "1",
      "grid": 0,
      "location": "node",
      "dtype": "uint16",
      "primitive": "unsigned short",
      "readable": true,
      "writable": true,
      "evolving": false
    },
    {
      "name": "scalar__int32",
      "initial": [
        7
      ],
      "units": "1",
      "grid": 0,
      "location": "node",
      "dtype": "int32",
      "primitive": "int",
      "readable": true,
      "writable": true,
      "evolving": false
    },
    {
      "name": "scalar__uint32",
      "initial": [
        7
      ],
      "units": "1",
      "grid": 0,
      "location": "node",
      "dtype": "uint32",
      "primitive": "unsigned int",
      "readable": true,
      "writable": true,
      "evolving": false
    },
    {
      "name": "scalar__int64",
      "initial": [
        7
      ],
      "units": "1",
      "grid": 0,
      "location": "node",
      "dtype": "int64",
      "primitive": "long long",
      "readable": true,
      "writable": true,
      "evolving": false
    },
    {
      "name": "scalar__uint64",
      "initial": [
        7
      ],
      "units": "1",
      "grid": 0,
      "location": "node",
      "dtype": "uint64",
      "primitive": "unsigned long long",
      "readable": true,
      "writable": true,
      "evolving": false
    },
    {
      "name": "scalar__float32",
      "initial": [
        7
      ],
      "units": "1",
      "grid": 0,
      "location": "node",
      "dtype": "float32",
      "primitive": "float",
      "readable": true,
      "writable": true,
      "evolving": false
    },
    {
      "name": "scalar__float64",
      "initial": [
        7
      ],
      "units": "1",
      "grid": 0,
      "location": "node",
      "dtype": "float64",
      "primitive": "double",
      "readable": true,
      "writable": true,
      "evolving": false
    }
  ]
};
