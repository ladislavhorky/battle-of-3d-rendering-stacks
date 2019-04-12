# Sandbox for comparing performance of VTS Geospatial and CesiumJS

This repository serves as a sandbox for comparing performance of various 3D rendering stacks on the same or very similar data. The web page where you can compare 3D rendering stacks live is [here](https://ladislavhorky.github.io/battle-of-3d-rendering-stacks/).

So far there are [VTS Geospatial](https://www.melown.com/products/vts-geospatial/) and [CesiumJS](https://cesiumjs.org/), iTowns are planned to be added once they support textured meshes in 3D Tiles.

The comparison is based on a basic smart-city app containing:

* global terrain based on [Viewfinder Panoramas 3 DEM](http://viewfinderpanoramas.org/dem3.html)
* global [EOX IT Sentinel-2 Cloudless](https://s2maps.eu/) imagery
* a [3D city model](https://www.melown.com/products/vadstena/) from low-altitude UAS imagery in 3D Tiles format
* vector parcel information from Czech [State Administration of Land Surveying and Cadastre](https://www.cuzk.cz/en)

This repository was created to accompany my talk "Battle of 3D Rendering Stacks" held at FOSS4G-NA 2019, San Diego, April 2019.

## Doing you own performance testing

The repo works as github pages, so you can easily tweak the code of the web applications in `vts/index.html` and `cesiumjs/index.html` and see the effect live. To get the github pages working, do the following:

1. fork the repo.
2. Once forked, create one commit to force the github pages to build. (e.g. on GitHub click "edit" the README.md, add space and commit). GiHub pages are ready once a green tick appears next to your commit.
3. Verify your github-pages are working by visiting `https://<your-username>.github.io/battle-of-3d-rendering-stacks`.

This way you may experiment with the frontend. If you want to add you own terrain or a 3D city model to further test your use-case, you may want to set up your own instance of VTS Backend - see below.

## Setting up your own VTS Backend

In case you want to further experiment with adding your own data or with the data provided for this example, here is how you can set up your own instance of VTS Backend and replicate configuration used in this example.

### Install VTS Backend and clone this repo

You will need a recent Ubuntu LTS, all server components are then [installed through a single Debian package](http://vtsdocs.melown.com/en/latest/tutorials/vtsbackend.html#setting-vts-backend).

Once you install VTS Backend, clone this repo into VTS user home directory: 

```bash
$ # switch to VTS user
$ suvts

$ mkdir git
$ git clone https://github.com/ladislavhorky/battle-of-3d-rendering-stacks.git

```

### Fuse 3D city model with global terrain

First, we shall fuse the 3D model of Benátky nad Jizerou with Viewfinder Panoramas DEM-based terrain:

```bash
$ # switch to VTS user if you have not done so
$ suvts

$ # add terrain to storage to be merged with 3D city model we add later
$ vts --add store/stage.melown2015 \
      --tileset "//cdn.melown.com/vts/melown2015/terrain/global/viewfinder3/" \
      --bottom
      
$ # add 3D city model under id benatky-nad-jizerou, it will be fused with the terrain
$ vts --add store/stage.melown2015 \
      --tileset "//cdn.melown.com/vts/melown2015/true3d/czech/benatky-nad-jizerou@2/" \
      --tilesetId benatky-nad-jizerou \
      --top

$ # copy map-configuration from repo
$ cp git/battle-of-3d-rendering-stacks/vts-backend/benatky-parcels store/map-config/
```

Now you can go to `http://localhost:8070/store/map-config/benatky-parcels` and you should see the 3D city model fused with the terrain. If you are not running VTS Backend on `localhost`, change it to appropriate server name.
  
### Prepare parcel data

First we need to set up the DEM for heightcoding the data:
```bash
$ # do everything under VTS user if you have not done so
$ suvts

$ # prepare DEM - can be then actually used as other terrain but we need it only for heightcoding
$ mapproxy-setup-resource --referenceFrame melown2015 \
                          --id benatky-nad-jizerou-dem \
                          --group battle-of-3d-stacks \
                          --dataset $VTS/vts-backend/heightcoding-dem.tif
                          --attribution "{copy}2005-16 Jonathan de Ferranti" \
                          --attribution "{copy}{Y} Melown Technologies SE"

```
Now we can set up the parcels. We will create tiled geodata resource from provided MBTiles file. The MBTiles file were created from `git/battle-of-3d-rendering-stacks/resources/all-parcels.json` with [tippecanoe](https://github.com/mapbox/tippecanoe) tool by following command (for reference):

```bash
$ tippecanoe -o all-parcels-15-better-tileres.mbtiles -z 15 -Z 15 -B 15 -d 16 -D 16 -ps all-parcels.json
```
To set up the parcels, we will simply copy resource and configuration files to appropriate paths and then ping VTS Mapproxy to register them and start serving them.

```bash
$ # do everything under VTS user if you have not done so
$ suvts

$ # copy resource files
$ cp git/battle-of-3d-rendering-stacks/vts-backend/parcels.style mapproxy/datasets/battle-of-3d-stacks/
$ cp git/battle-of-3d-rendering-stacks/vts-backend/all-parcels-15-better-tileres.mbtiles mapproxy/datasets/battle-of-3d-stacks/

$ # copy vts mapproxy resource config json
$ cp git/battle-of-3d-rendering-stacks/vts-backend/benatky-parcels.json /etc/vts/mapproxy/examples.d/

$ # tell vts mapproxy there are new resources
$ /etc/init.d/vts-backend-mapproxy force-update
```

You can check the resource is ready in mapproxy log - look for lines beginning `Ready to serve <resource>`:
```
$ tail /var/log/vts/mapproxy.log
```
Once VTS Mapproxy is updated, go to `http://localhost:8070/store/map-config/benatky-parcels` to see the result!

## Legal notice

Please respect any license restrictions applicable to the data sources used
in this demonstration. Respective copyright holders are clearly marked in the
bottom-right area of the map window in case of VTS Geospatial and in bottom-left area of the map window in case of CesiumJS.
