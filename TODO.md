# TODO

-   ~~process CLPX 2018 to single raster with correct meta and extent~~
-   ~~process HV 2018 to single raster with correct meta and extent~~
-   ~~Document above preprocessing in data_long~~
-   ~~Compute 2018 HV & CLPX depth dDEMS~~
-   ~~Get 2018 probe data into shape for validation~~
-   ~~Run validation process~~
-   ~~Check HV shapefile for ICE points~~
-   ~~Update data_long report with new results~~
-   ~~Why is there a double clpx 2015 entry?~~
-   ~~Apply new offset from new results to HV 2016 depth dDEM~~
-   Finish data_long and data_short
    -   Do we need bare spot analysis (reqs.orthos)?
    -   Do we need any further spatial / regional analysis
    -   Add note about creating depth stack images, ~~and update metadata~~
    -   ~~Trim to where we have data for all years, i.e. if nan for one year then nan for every year~~
-   Methods: Similarity index
-   Methods: Drift mapping
- 1. Create script to compare drift vs. not-drift area (and snow volume) for a variety of depth thresholds. The thresholds should be precentages of the mean depth value for the domain. This should generate simialr results to an experiment done at Tuolumne.
- 2. Use results of (1) to identify a drift inventory for each winter, and for a stack of all winters.
- 3. Generate statistics under each drift..what can we learn? Produce a summary table of drifts. Shape, size, mean depth, max depth, nearest neighbors, etc. (auto corre?)
-   Write Field Areas section
-   ~~Create stack of depth dDEMS~~

Run Happy Valley again with re-processed 2012 surface and report to Chris.
What about CLPX?

Use depth_stack (that has values everywhere, i.e. no NoData holes) to generate drift mask based on threshold analysis. Then use drift mask to develop zonal statistics and to train rf model.
