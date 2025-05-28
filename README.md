# vectordataalgorithm

**Version:** 1.0.0  
**Author:** [Your Name Here]  
**License:** [Specify License, e.g., MIT]  
**Repository:** [Add repository URL if available]  

## Overview

`vectordataalgorithm` is a Python package providing fundamental geometric data structures and algorithms for standalone GIS (Geographic Information Systems) projects. It supports 2D vector geometry operations for Points, Polylines, and Polygons, enabling spatial analysis, mapping, and geometric computations.

## Features

- **Point**: Represents a 2D point with x and y coordinates.
  - Distance calculation between points
  - Tuple conversion
  - String and repr representations

- **Polyline**: Represents a series of connected points (vertices).
  - Length calculation (sum of segment distances)
  - Check if polyline is closed
  - Segment extraction
  - Reverse vertices

- **Polygon**: Represents a closed shape defined by points.
  - Perimeter (length) calculation
  - Area calculation (Shoelace formula)
  - Centroid computation
  - Bounding box extraction
  - Orientation check (clockwise/counterclockwise)
  - Point-in-polygon test (ray casting algorithm)

## File Structure

```
vectordataalgorithm/
│
├── README.md          # This file
├── setup.py           # Installation script for the package
├── LICENSE            # License file
│
├── vectordataalgorithm/  # Package source code
│   ├── __init__.py    # Initialize the package
│   ├── point.py       # Point class and related functions
│   ├── polyline.py    # Polyline class and related functions
│   └── polygon.py     # Polygon class and related functions
│
└── tests/             # Unit tests for the package
    ├── __init__.py
    ├── test_point.py
    ├── test_polyline.py
    └── test_polygon.py
```

- [`geometry.py`](vectordataalgorithm/vectordataalgorithm/geometry.py): Contains the core classes and algorithms.
- `__init__.py`: Exposes the geometry module.
- `README.md`: This documentation.

## Usage

```python
from vectordataalgorithm.geometry import Point, Polyline, Polygon

# Create points
p1 = Point(0, 0)
p2 = Point(1, 0)
p3 = Point(1, 1)
p4 = Point(0, 1)

# Distance between points
dist = p1.distance_to_other(p2)

# Create a polyline
line = Polyline([p1, p2, p3])

# Polyline length
length = line.Length

# Create a polygon
poly = Polygon([p1, p2, p3, p4])

# Polygon area and centroid
area = poly.Area
centroid = poly.Centroid

# Point-in-polygon test
inside = poly.contains_point(Point(0.5, 0.5))