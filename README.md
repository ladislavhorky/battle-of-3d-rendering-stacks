# Sandbox for comparing performance of VTS Geospatial and CesiumJS

This repository serves as a sandbox for comparing performance of various 3D rendering stacks on the same or very similar data. The web page where you can compare 3D rendering stacks live is [here](https://ladislavhorky.github.io/battle-of-3d-rendering-stacks/).

So far there are [VTS Geospatial](https://www.melown.com/products/vts-geospatial/) and [CesiumJS](https://cesiumjs.org/), iTowns are planned to be added once they support textured meshes in 3D Tiles.

The comparison is based on a basic smart-city app containing:

* global terrain based on [Viewfinder Panoramas 3 DEM](http://viewfinderpanoramas.org/)
* global [EOX IT Sentinel-2 Cloudless](https://s2maps.eu/) imagery
* a [3D city model](https://www.melown.com/products/vadstena/) from low-altitude UAS imagery in 3D Tiles format
* vector parcel information from Czech [State Administration of Land Surveying and Cadastre](https://www.cuzk.cz/en)

Using the same underlaying data (same meshes for terrain and 3D and the same imagery), it is possible to do a performance comparison of the 3D rendering stacks even though they are very dirrent feature-wise.

## Doing you own performance testing

The repo works as github pages, so you can easily tweak the code of the web applications in `vts/index.html` and `cesiumjs/index.html` and see the effect live. To get the github pages working, do the following:

1. fork the repo.
2. Once forked, create one commit to force the github pages to build. (e.g. on GitHub click "edit" the README.md, add space and commit). GiHub pages are ready once a green tick appears next to your commit.
3. Verify your github-pages are working by visiting `https://<your-username>.github.io/battle-of-3d-rendering-stacks`.

This way you may fiddle with the frontend. If you want to add you own terrain, a 3D city model to further test your use-case, you may want to set up your own instance of VTS Backend - see below.

## Setting up your own VTS Backend

In case you want to further experiment with adding your own data or with the data provided for this example, here is how you can set up your own instance of VTS Backend and replicate configuration used in this example.

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

Now you can go to `http://<yourserver>:8070/store/map-config/benatky-parcels` and you should see the 3D city model fused with the terrain.
  
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
Once VTS Mapproxy is updated, go to `http://<yourserver>:8070/store/map-config/benatky-parcels` to see the result!
