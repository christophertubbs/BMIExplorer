# Primitive type and ABI mapping

Static one-element scalar attributes cover each primitive width with hydrological
names and values (for example `scalar__stream_order=5`, `scalar__area_sqkm=253.25`,
and `scalar__manning_roughness=0.035`). The complete name/dtype/value/unit mapping
is in [fixture configuration](business-configuration.md). Main node/edge/face
examples use double/float64.

| Declared BMI label | NumPy dtype | Teaching C++ equivalent | Bytes |
|---|---|---|---:|
| signed char | int8 | signed char | 1 |
| unsigned char | uint8 | unsigned char | 1 |
| short | int16 | short | 2 |
| unsigned short | uint16 | unsigned short | 2 |
| int | int32 | int | 4 |
| unsigned int | uint32 | unsigned int | 4 |
| long long | int64 | long long | 8 |
| unsigned long long | uint64 | unsigned long long | 8 |
| float | float32 | float | 4 |
| double | float64 | double | 8 |

Geometry shape/connectivity and index buffers use int32; coordinates, spacing and
origin use float64. Initialization checks all listed C widths using ctypes and
rejects an unsupported teaching ABI. C++ does not universally guarantee these
widths. In particular, do not assume np.int_ is int32 or that long is long long.

These primitive spellings are fixture policies, not universal BMI labels. Native
byte order and exact dtype are required. Integer/float widths, signedness and
Python sequences are never silently converted. Allocation/conversion is the
caller's responsibility; dtype-correct buffers retain their bits during reads
and writes, including integer extremes and signed zero. Compound/vector types
and platform-dependent long double are excluded. A collection of values is not
a compound primitive element type.
