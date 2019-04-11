# Sandbox for comparing performance of VTS Geospatial and CesiumJS

This repository serves as a sandbox for comparing performance of various 3D rendering stacks on the same or very similar data. 
So far there is [VTS Geospatial](https://www.melown.com/products/vts-geospatial/) and [CesiumJS](https://cesiumjs.org/), iTowns are planned to be added once there is support for textured meshes in 3D Tiles.

To jumpstart the comparison the repo contains github-pages with a simple smart-city-like web app containing:

* global terrain based on [Viewfinder Panoramas 3 DEM](http://viewfinderpanoramas.org/)
* global [EOX IT Sentinel-2 Cloudless](https://s2maps.eu/) imagery
* a [3D city model](https://www.melown.com/products/vadstena/) from low-altitude UAS imagery in 3D Tiles format
* vector parcel information from Czech [State Administration of Land Surveying and Cadastre](https://www.cuzk.cz/en)

impemented both in VTS Geospatial and CesiumJS. Through the 3D rendering stacks are very different feature-wise, this setup using the same underlaying data allows for direct performace comparison. Feel free to fork the repo and tweak the example to match your use-case. Upon forking and creating one commit to trigger github pages build, the web wth comparison will be accessible at `<github username>.github.io/battle-of-3d-rendering-stacks/`.

If you want to play just with the front-end, the repo is practically self-contained. If you would like to play also with VTS Backend (add, replace, change some data), read the instructions below on how the VTS Backend for this example is set up.

## Setting up your own VTS Backend

