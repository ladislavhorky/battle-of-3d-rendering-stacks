# Sandbox for comparing performance of VTS Geospatial and CesiumJS

This repository serves as a sandbox for comparing performance of various 3D rendering stacks on the same or very similar data. 
So far there is [VTS Geospatial](https://www.melown.com/products/vts-geospatial/) and [CesiumJS](https://cesiumjs.org/), iTowns are planned to be added once there is support for textured meshes in 3D Tiles.

To jumpstart the comparison the repo contains github-pages with a simple smart-city-like web app containing:

* global terrain based on [Viewfinder Panoramas 3 DEM](http://viewfinderpanoramas.org/)
* global [EOX IT Sentinel-2 Cloudless](https://s2maps.eu/) imagery
* a [3D city model](https://www.melown.com/products/vadstena/) from low-altitude UAS imagery in 3D Tiles format
* vector parcel information from Czech [State Administration of Land Surveying and Cadastre](https://www.cuzk.cz/en)

impemented both in VTS Geospatial and CesiumJS. Through the 3D rendering stacks are very different feature-wise, this setup using the same underlaying data allows for direct performace comparison. Feel free to fork the repo and tweak the example to match your use-case. Upon forking and creating one commit to trigger github pages build, the web wth comparison will be accessible at `<github username>.github.io/battle-of-3d-rendering-stacks/`.

If you want to play just with the frontend, the repo is practically self-contained. If you would like to play also with VTS Backend (add, replace, change some data), read the instructions below describing how the VTS Backend for this example was set up.

The terrain, imagery and the 3D model are provided as VTS Public Resources, free for purposes of development and testing. See below.

## Setting up your own VTS Backend

In case you want to further experiment with adding your own data or with provided VTS Public Resources, here is how you can set your own instance of VTS Backend and replicate configuration used in this example.

### Install VTS Backend

You will need a recent Ubuntu LTS, all server components are then [installed through a single Debian package](http://vtsdocs.melown.com/en/latest/tutorials/vtsbackend.html#setting-vts-backend).

### Fuse 3D city model with surrounding terrain

Once you install VTS Backend, you can use the 3D city model and terrain from VTS Public Resources and fuse them together. Clone this repo as the `vts-backend` folder contains files you will need. Path to where your repo is denoted as `$VTS`. Do everything as `vts` user:

```bash
$ # switch to VTS user
$ suvts

$ # add terrain to storage to be merged with 3D city model we add later
$ vts --add store/stage.melown2015 \
      --tileset "//cdn.melown.com/vts/melown2015/terrain/global/viewfinder3/" \
      --bottom
      
$ # add 3D city model under id benatky-nad-jizerou, it will be fused with the terrain
$ vts --add store/stage.melown201 \
      --tileset "//cdn.melown.com/vts/melown2015/true3d/czech/benatky-nad-jizerou@2/" \
      --tilesetId benatky-nad-jizerou \
      --top

$ # copy map-configuration from repo
$ cp $VTS/vts-backend/benatky-parcels store/map-config/
```

Now you can go to http://<yourserver>:8070/store/map-config/benatky-parcels and you should see the 3D city model fused with the terrain.
  
### Prepare parcel data

First we need to set up the DEM for heightcoding the data:
```bash
$ # do everything under VTS user
$ suvts

$ # prepare DEM - can be then actually used as other terrain but we need it only for heightcoding
$ mapproxy-setup-resource --referenceFrame melown2015 \
                          --id benatky-nad-jizerou-dem \
                          --group battle-of-3d-stacks \
                          --dataset $VTS/vts-backend/heightcoding-dem.tif
                          --attribution "{copy}2005-16 Jonathan de Ferranti" \
                          --attribution "{copy}{Y} Melown Technologies SE"

```
Now we can set up the parcels. We will create tiled geodata resource from provided MBTiles file. The MBTiles file were created from `all-parcels.json` by [tippecanoe](https://github.com/mapbox/tippecanoe) tool by following command (for reference):

```bash
$ tippecanoe -o all-parcels-15-better-tileres.mbtiles -z 15 -Z 15 -B 15 -d 16 -D 16 -ps all-parcels.json
```
To set the parcels up, we will simply copy resource files and configuration files to appropriate paths and then ping VTS Mapproxy register and start serving them.

```bash
$ # do everything under VTS user
$ suvts

$ # copy resource files
$ cp $VTS/vts-backend/parcels.style mapproxy/datasets/battle-of-3d-stacks/
$ cp $VTS/vts-backend/all-parcels-15-better-tileres.mbtiles mapproxy/datasets/battle-of-3d-stacks/

$ # copy vts mapproxy resource config json
$ cp $VTS/vts-backend/benatky-parcels.json /etc/vts/mapproxy/examples.d/

$ # tell vts mapproxy there are new resources
$ /etc/init.d/vts-backend-mapproxy force-update
```

You can check the resource is ready in mapproxy log - look for lines beginning `Ready to serve <resource>`:
```
$ tail /var/log/vts/mapproxy.log
```
Once VTS Mapproxy is updated, go to http://<yourserver>:8070/store/map-config/benatky-parcels to see the result!
