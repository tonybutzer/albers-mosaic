# albers-mosaic
ECO and ECOAI - cloud open source project mosiac challenge


# hypothesis

- The cloud will offer efficiencies and opportunities to accelerate science
- lcmap will be ported and likely re-engineered in the cloud
- Adhoc science R&D should start getting ready for these paradigm shifting events

# issue defined 

Parajuli, Sujan
    Hey Butzer, Tony (Contractor) , let me tell our requirements. We have these multiple number of HLS tiles that are overlapped and need to be merged. One problem is there are five different UTM zones (10 - 14N) and that needed to be reprojected to Albers equal conical for final mosaic(this is already figured out) and second one is taking the mean/average values of pixels in the overlapping areas. We have been using arcmap mosaic to new raster for that purpose but we want the same with the open source software on HPC . Seems like your docker and xarray merge may work but will that take into account the case of overlapping areas and take the mean pixel values of those overlapping area?


- similar in some ways to compositing


I wonder if it would be worth tracking down the people that create ARD tiles for Landsat in Albers? - The likely use open source methods rather than ARC software. We could start with Ron Dilley to find the coders. They might be starting with something other than UTM though - something further upstream in the Landsat process.

[Tuesday 3:27 PM] Butzer, Tony (Contractor)
    I found this well documented in Arc Toolbox land



ArcToolbox

(Tools / Data Management / Raster / Mosaic or Tools / Data Management / Raster / Mosaic to New Raster)

The MOSAIC tool combines the geoprocessing of both MERGE and MOSAIC. Overlapping areas can be handled in any one of the following manners:


	
FIRST—The output cell value of the overlapping areas will be the value from the first raster in the list. This is the default, and is analogous to the Raster Calculator MERGE).
	LAST—The output cell value of the overlapping areas will be the value from the last raster in the list.
	BLEND—The output cell value of the overlapping areas will be a blend of values of the overlapped cells. This blend value on a weight-based algorithm is dependent on the distance from the pixel to the edge within the overlapping area. This is 
	MEAN—The output cell value of the overlapping areas will be the mean value of the overlapped cells.
	MINIMUM—The output cell value of the overlapping areas will be the  minimum value of the overlapped cells.
	MAXIMUM—The output cell value of the overlapping areas will be the  maximum value of the overlapped cells.


​[Tuesday 3:28 PM] Butzer, Tony (Contractor)
    I don't think xarray merge is quite as mature or clear in its documentation - easy to use though - but might not be as scientifically definitive


ARC mosaic tool has multiple options we can choose from. One of the drawback using the HLS is the overlapping areas. In so many ways, it is good to have that buffer between tiles but when you try to mosaic the tiles, these overlapping areas create trouble. It is not only two tiles. Around corner you have at least 4 tiles overlapping. And another issue is, when you have different projections (UTM) to deal with

Kelcy has a really useful mosaicing (rather pixel stitching, he likes to call it) script, he developed for LCMAP. It defines the larger extent first using a polygon shapefile and than fill with pixels reading individual tiles. In our case that does not help much, because of the overlapping areas.

I think in some ways this is similar to compositing  - where the base part of the image - non overlap part you only get one observation and then in the overlapping areas you have multiple pixels to choose from or average. I am sure we can build a brute force way to do it with xarray - but we might not get as good a result with a simple xarray merge. 

# approach

- Identify some small simple overlapping test data
	- place this in the cloud data lake
	- setup basic pangeo.chs.usgs.gov access
- pilot some notebooks using concat and merge and slicing/windowing in albers
	- the ARD grid is your Reference Dahal? ??
- Be aware of HLS and the decisions made on projections and gridding
    - UTM
    - MGRS
- Create some visualizations for the overlap
- Demonstrate simple pixel timeseries for overlap
- Study more sophisticated composite (6 band evaluation) and actual SR value
- Masking?
	- GDAL Mask
	- No Data Mask
	- Cloud - shadow - ... applicable ?
    

https://en.wikipedia.org/wiki/Military_Grid_Reference_System#/media/File:Universal_Transverse_Mercator_zones.svg

# steps

1. kickoff meeting


## References 

- https://www.earthdatascience.org/courses/use-data-open-source-python/multispectral-remote-sensing/landsat-in-Python/
- https://rasterio.readthedocs.io/en/latest/topics/masks.html



