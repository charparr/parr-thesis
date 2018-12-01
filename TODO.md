# TODO

## Old Business
-   Finish Data Section
  - Reduce table size
  - Cull skew, kurt from map errors. format count as int and fix years from agg. table?
  -   Figures for appendices: DSM, Depth Maps, Stack Products

## Introduction
-   Send bullets for introduction to Matthew
-   Review Old Documents for intro ideas

## Field Areas

## Methods
  - what areas are always drifts or not drifts? (creating inventory)
  -
-   Similarity of snow depth patterns
  - We know drifts are similar - what about the entire snow patterns
  - but we do not care about geometric warps
  - so here is the toolbox
-   We know from the above drift inventory and similarity toolbox that snow patterns repeat with high fidelity. What drives the fidelity?
  - Must be something about the landscape
  - So let's try a rf model of different landscape features



-   Create script to compare drift vs. not-drift area (and snow volume) for a variety of depth thresholds. The thresholds should be precentages of the mean depth value for the domain. This should generate simialr results to an experiment done at Tuolumne.
-   Use results of (1) to identify a drift inventory for each winter, and for a stack of all winters.
-   Generate statistics under each drift..what can we learn? Produce a summary table of drifts. Shape, size, mean depth, max depth, nearest neighbors, etc. (auto corre?)
-   Write Field Areas section
- Implement VRM topo metric (https://gis.stackexchange.com/questions/110397/how-to-use-vector-ruggedness-measure-vrm-tool-from-arcscripts-at-latest-version)

## Notes
Learn: Geographically Weighted Regressions

Find a way to smooth DEM or depth maps

really know CI and CV

Contribute similarity metrics to skimage
