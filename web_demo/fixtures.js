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
      "name": "scalar__velocity",
      "initial": [
        328.3245
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
      "name": "uniform_2d__slope",
      "initial": [
        0.0124,
        0.0059,
        0.0186,
        0.0116,
        0.0174,
        0.0050,
        0.0113,
        0.0177,
        0.0138,
        0.0189,
        0.0036,
        0.0042
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
      "name": "uniform_3d__soil_temp",
      "initial": [
        38.353,
        38.595,
        37.404,
        35.485,
        33.805,
        34.369,
        38.609,
        36.339,
        34.061,
        33.797,
        35.907,
        33.977,
        33.917,
        38.704,
        39.175,
        32.596,
        35.215,
        38.831,
        33.257,
        37.832,
        36.852,
        35.515,
        33.693,
        33.748
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
      "name": "rectilinear_2d__precip_rate",
      "initial": [
        38.342,
        31.174,
        45.544,
        14.186,
        34.703,
        49.875,
        24.987,
        40.632,
        32.443,
        24.699,
        0.911,
        18.312
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
      "name": "rectilinear_3d__saturation",
      "initial": [
        0.292,
        0.318,
        0.355,
        0.616,
        0.689,
        0.516,
        0.178,
        0.382,
        0.360,
        0.670,
        0.170,
        0.205,
        0.631,
        0.523,
        0.879,
        0.832,
        0.475,
        0.567,
        0.591,
        0.960,
        0.999,
        0.421,
        0.210,
        0.360
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
      "name": "points_2d__snow_depth",
      "initial": [
        0.1,
        0.3,
        0.2,
        0.2,
        0.32,
        0.11
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
      "name": "points_3d__water_level",
      "initial": [
        4.42,
        1.882,
        1.230,
        3.212,
        0.846,
        2.763
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
      "name": "unstructured_edges__flow_velocity",
      "initial": [
        2.1,
        1.894,
        1.773,
        2.435
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
      "name": "unstructured_mixed__depth",
      "initial": [
        4.976,
        1.597,
        1.238,
        3.327,
        1.942,
        3.793
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
      "name": "unstructured_mixed__flux",
      "initial": [
        0.436,
        0.867,
        -0.119,
        0.232,
        1.351,
        1.295,
        0.787,
        0.501
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
      "name": "unstructured_mixed__precipitation_rate",
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
      "name": "scalar__anomaly_class",
      "initial": [
        -3
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
      "name": "scalar__qc_code",
      "initial": [
        2
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
      "name": "scalar__scaled_temp",
      "initial": [
        2345
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
      "name": "scalar__stream_order",
      "initial": [
        5
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
      "name": "scalar__flow_direction_code",
      "initial": [
        -72
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
      "name": "scalar__contributing_cells",
      "initial": [
        384
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
      "name": "scalar__storage_capacity",
      "initial": [
        7030259239
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
      "name": "scalar__processed_cells",
      "initial": [
        83939242345
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
      "name": "scalar__area_sqkm",
      "initial": [
        253.23412
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
      "name": "scalar__manning_roughness",
      "initial": [
        0.035
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
