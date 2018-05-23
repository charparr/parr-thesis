# Report on the accuracy and validation of airborn lidar and structure-from-motion photogrammetry (SfM) surface height measurements and computation of snow depths.

## Charlie Parr,  5/22/2018
___

### Data
<p>
The data used in this analysis comes from the airborne snow measurement campaigns conducted in two distinct Arctic tundra field areas over the course of six years. The basis of these campaigns was to acquire the elevation of peak winter snowcovers and bare earth surfaces and to interpret the difference between the two seasonal surfaces as snow depth. Each snow depth result is then validated by thousands of conincident manual measurements of snow depth. The report here describes the validation process, error analysis, and error attribution.
</p>
<p>
Each year the snow depth map produced by the seasonal surface differencing is validated by thousand of MagnaProbe measurements. A scripting tool checks the value of the snow depth raster map against the value of the MagnaProbe depth measurement at the same location and then computes the difference. The differences between the MagnaProbe measurement of snow depth and the airborne retreival of snow depth are summarized for each year in Table 1. A total of xx100000xx points were used in this validation analysis. The mean error for the entire analysis is __
</p>
###### Table 1: Validation Results
![alt text](aggregate_results/figs/aggregate_results_summary.png)
<p>
The results in Table 1 indicate a negative bias in the airborne methods. We can visualize this bias by comparing the distributions of MagnaProbe depths and coincident raster snow depths (Figure 1).
</p>
###### Figure 1: MagnaProbe vs. lidar/SfM
![alt text](aggregate_results/figs/probe_v_rstr_violin.png)
