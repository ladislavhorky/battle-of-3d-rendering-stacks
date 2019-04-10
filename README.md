# Sandbox for comparing performance of VTS and CesiumJS

This repository serves as a sandbox for comparing performance of various 3D rendering stacks on the same or very similar data. 
So far there is VTS and CesiumJS, iTowns are planned to be added once there is support for textured meshes in 3D Tiles.

To jumpstart the comparison without doing any server-side configuration, the repo contains github-pages with a simple 
smart-city-like web app containing:
* global terrain and imagery
* a 3D city model
* vector parcel information

impemented both in VTS and CesiumJS using the same underlying data.
