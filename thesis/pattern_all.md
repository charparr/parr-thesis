# Snow Depth Pattern Similarity

## Snow Pattern Introduction

Spatial patterns of snow properties (i.e. depth, density, SWE) abound in nature and inhabit spatial scales that range from continental (10<sup>4</sup> km, e.g. ice sheet gradients) to decimetric (e.g. snow surface bedforms). The processes that spawn these patterns function over similarly distant time scales ranging from decadal (climate) to wind rapidly moving snow over the course of a single storm where transport rates can range in the decigrams * m<sup>-2</sup>s<sup>-1</sup>. Observation of snow patterns is predicated by spatial scale and resolution and by the climate class of snow. In windy tundra (and some alpine and prairie) snow classes, distinct spatial patterns of snow depth are created by the scour, transport, and deposition of snow by the wind. Such snow patterns are distinguished by two primary snowcover units: snowdrifts and scour zones. Snowdrifts are "sinks" for windblown snow and possess a relatively thick and dense snowcover. Scoured zones are "sources" for the snowdrifts and are exposed to strong winds capable of eroding the snowcover and transporting it downwind where it is then deposited - unless it sublimates. Snow patterns with strong snowdrift and scour elements with little underlying vegetation (Figure 1) are a function of snow precipitation (P) and snow transport (T). The T component is determined by the interaction of wind and topography, and thus when the T signal is large, the spatial pattern of snow depth is very much dependent on the spatial pattern of topography. Tundra snow depth patterns at the landscape scale are tightly coupled with the snow transport process - which itself is coupled tightly to topographic patterns. Understanding the nature of tundra snow depth patterns, learning how to compare and contrast them, and observing their behavior over time, can reveal a novel heterogeneity within the snow and illuminiate new snow-landscape relationships.

###### Figure 1. A series of watertracks on Alaska's North Slope filled by snowdrifts and punctuated by scoured interfluves. The pattern repeats each year with remarkable consistency.
![alt text](../subsets/hv_watertrack/results/iqa/hv_watertrack_snow_depth_stats.png)

Although scientific interest is snow patterns is not new, our ability to repeatedly measure them in high resolution (1 m) at the landscape scale is. Prior work on spatial snow patterns links the patterns to geographic variables or uses them to inform hydrological models (e.g. Kirnbaur, 1991; Konig and Sturm, 1998; Grayson et al., 2002; Winstral et al., 2002; Parajka et al., 2012) yet few analyze patterns at the landscape or watershed scale (<i>cf.</i> Lauriol et al., 1986) or quanitfy the inter-annual consistency of the patterns (<i>cf.</i> Luce, 2004; Sturm and Wagner, 2010; Qualls and Arogundade, 2013). Snow pattern knowledge is still immature and the record of patterns in nature is short. As remote sensing and modeling capacities expand and resolutions sharpen, the need for robust and efficient methods of comparing spatial patterns is growing (Jetten, 2003). Measuring the similarity of one spatial pattern to another is not trivial. While comparing and interpreting two spatial patterns may be intuitive for human observers, it is a complex task for computers because they are senstive to small changes. For example, minor geometric distortions of a pattern (translation, rotation, warping, etc.), amplitude changes, or additive noise can disproportionately impact standard statistcal measures of pattern fidelity such as mean square error (MSE). The key to better quantitative spatial pattern comparison, and snow pattern knowledge, are computation tools that are robust enough to ignore insignficant changes and efficient enough to handle large datasets. Essentialy we need tools that mimic the power of human observation.

## Snow Pattern Methods

Fortunately recent advances in computer hardware have accelerated progress in the fields of computer vision, image processing, and image quality assessment (IQA) and the replication of the human visual system's exceptional pattern recogitnion capabilities is an active area of research. Although there is no consensus as to the single best algorithm for measuring pattern similarity, IQA research has produced a multitude of metrics that use information about pattern structure and organization over multiple scales to measure the similairty of two images. Each IQA metric has unique set of tradeoffs between complexity, efficiency, and interpretability. For our snow pattern use case we apply four IQA metrics that represent a range of complexities (Table 1).
###### Table 1. A pattern comparison toolbox composed of four IQA metrics.
| IQA Metric                                                      | Perfect Similarity | No Similarity |
|-----------------------------------------------------------------|--------------------|---------------|
| Euclidean-Normalized Mean Square Error (NRMSE)               | 0.0                | 1.0           |
| Structural Similarity Index Method (SSIM)                    | 1.0                | -1.0          |
| Complex Wavelet Structural Similarity Index Method (CW-SSIM) | 1.0                | -1.0          |
| Gradient Magnitude Similiarty Deviation (GMSD)               | 0.0                | 1.0           |
Each of the four IQA metrics are sensitive to different types of pattern (i.e. image) information. NRMSE is only sensitive to pixel-wise arthimetic differences and thus it is not robust with respect to more modern IQA metrics. However, it is included here as a reference point due to a long history of use in signal processing and because of the ease with which it is computed and interpreted (Wang and Bovik, 2009). NRMSE values reported here range between 0.0 and 1.0 where a score of 1.0 indicates perfect similarity - meaning the pattern is being compared to itself. NRMSE values are recorded here but are not ultimately used to analyze pattern fidelity. SSIM is more complex than MSE, but is still a relatively simple and efficient metric that considers the structural information in a pattern that is independent of local mean amplitude (brightness) and contrast. Although SSIM more closely mimics the human visual system because it focuses on where pattern gradients are high or are changing, it is still sensitive to minor geometric distortions. SSIM is also discounted from the ultimate pattern fidelity analysis. The non-structural distortions that hinder SSIM are countered by implementing the technique in the complex wavelet domain. CW-SSIM leverages information about local phase patterns and how the wavelet coeffcients compare across images (Wang and Simoncelli, 2005). GMSD is a similarly robust metric and is the modern endpoint in our IQA toolbox. More efficient than most contemporary methods, GMSD computes gradient information by convolving a Prewitt kernel over the images and then pooling the gradient magntiude differences by a windowed standard deviation to account for local variance (Xue et. al, 2014). Together, CW-SSIM and GMSD are used to quantify pattern similarity far more thoroughly than is possible with standard techniques, and do so in a way that is efficient and reproducible. Each IQA metric returns both a global index value and an array of local metric values with same dimensionality as the input images. The arrays are essentially similarity maps that depict where patterns are cohesive and where they are not with respect to the type of information the metric is sensitive to (e.g. Figure 2).

###### Figure 2. An example of the similarity analysis for a single zone and pair of years: IQA results for the Happy Valley Watertracks.
![alt text](../subsets/hv_watertrack/results/iqa/2013_v._2018.png)

The index values enable intra-pattern comparison over time to identify pattern pairs that or more or less similar to one another. Index values can also be pooled to compare the overall pattern fidelity of different pattern types. Only CW-SSIM (range -1 to +1) and GMSD (range 0 to 1) are used in ranking similarity. Lower ranks indicate greater pattern fidelity (Figure 3).

Figure 3. IQA index values and rankings by comparison pairs for the Happy Valley Watertracks domain.
![alt text](../subsets/hv_watertrack/results/iqa/iqa_indexvals_heatmap.png)
![alt text](../subsets/hv_watertrack/results/iqa/iqa_barchart.png#1)

The combination of our IQA toolbox and expansive snow depth records enable a novel analysis of snow depth pattern similarity. We quantify the interannual similarity of near-peak snow depth patterns across eight snowdrift zones that reprsent a variety of scales, snow depth distributions, and snowdrift features (Figure 4). Similarity is computed for each unique pair of the six years included in our study (N=15), comprising a total of 120 "map-to-map" snow depth pattern comparisons. Using IQA metrics permits a more nuanced and sophisticated pattern analysis and illuminates (as we show later) snow-landscape relationships.

###### Figure 4. Eight snowdrift zones within CLPX and HV. Hillshade illumination from the NW at an altitude of 30 degrees.
![alt text](../subsets/agg_results/subset_snow_and_hillshades.png)

## Snow Pattern Results

The results of the similarity analysis using IQA metrics reveal that patterns of snowdrift and scour at CLPX and HV repeat each winter with great fidelity (e.g. CW-SSIM scores range from 0.52 to 0.86, Figure 5). While there is some variance similarity amongst pairs of winters within each zone, on an absolute scale similarity is overall remarkably consistent. Such high fidelity patterns occur in each subset, although because of the finer similarity discernmnet offered by the IQA toolbox there are slight differences in relative similarity amongst the different landscapes (Figure 6).

###### Figure 5. CW-SSIM results for 120 snow depth pattern comparisons. Possible values range from -1 to 1.
![alt text](../subsets/agg_results/cwssim_heatmap.png)

###### Figure 6. CW-SSIM results grouped by zone. Possible values range from -1 to 1.
![alt text](../subsets/agg_results/cwssim_bars.png)


## Snow Pattern Discussion
Patterns are the same within each study area (Qualls, Sturm)
  so we can create normalized cdsps
  this is good because we have larger area
  and we now know that 2 years is basically enough
But what is the use of finder similarity terms?
  some winters better than others, why?
  some landscapes overall better than othes, why?

--> Filling v non Filling



  There is also (as we dicsuss later) a difference in how each landscape filters variability in the winter weather (Figure 3, bottom).

A few salient things emerge from the similarity analysis. First, the snow depth patterns are remarkably similar and consistent year after year.

The similarity of the tundra snow depth patterns year after year in different types of terrain enables us to confidently create a cumulative snow depth distribution pattern (CDSP) for the entire extent of the study areas by using the normalized mean snow depth from the dataset. We then define drifts and create a snowdrift inventory for each landscape.


Something must be dribing that similarity.
We know snowdrifts are a function of landscape and weather - but how much is landscape. We don't have good weather control (maybe reanalysis shows something) but we know it is more variable than landscape. Weather cant capture the complexity of blowing snow

So what is it about the landscape? We know a drift landscape needs these things: Obstacles, Slope Breaks, Just changing topography and elevation, influenced by both upwind and downwind (how far?) factors.


 Landscape is the
So can we search an array for these landscape factors?

Drifts with deeper, sharper breaks, are going to capture more variability because they do not fill.

Hv watertrack: all EQ Drifts
clpx-outcrops: all nonfilling
Interesting that these are the similairty endmembers.
Do we see a difference in their topographic variables?

With the knowledge that they are similar, plus that landscape is repsonsible,

we can make a snowdrif invventory:

Now:
If the spatial pattern is 85% the same year after year - we  should be able to predict 85% of snow depth by landscape variables alone.



Weather data is sparse for these Areas

Plot: mean not-drift depth vs. mean drift depth




1.  Kirnbauer, R., Blöschl, G., Waldhäusl, P. & Hochstöger, F. An analysis of snow cover patterns as derived from oblique aerial photographs. in Snow, Hydrology and Forests in High Alpine Areas (Proceedings of the Vienna Symposium) 91–100 (IAHS, 1991).
2.  Grayson, R. B., Western, A. W. & Mcmahon, T. A. Advances in the use of observed spatial patterns of catchment hydrological response. Adv. Water Resour. 25, 1313–1334 (2002).
3.  Wealands, S. R., Grayson, R. B. & Walker, J. P. Investigating Spatial Pattern Comparison Methods for Distributed Hydrological Model Assessment.
4.  Konig, M. & Sturm, M. Mapping snow distribution in the Alaskan Arctic using aerial photography and topographic relationships. Water Resour. Res. 34, 3471–3483 (1998).
5.  Parajka, J., Haas, P., Kirnbauer, R., Jansa, J. & Blöschl, G. Potential of time-lapse photography of snow for hydrological purposes at the small catchment scale. Hydrol. Process. 26, 3327–3337 (2012).
6.  Winstral, A., Elder, K. & Davis, R. E. Spatial Snow Modeling of Wind-Redistributed Snow Using Terrain-Based Parameters. Journal of Hydrometeorology (2002). doi:10.1175/1525-7541(2002)003<0524:SSMOWR>2.0.CO;2
7.  Sturm, M. & Wagner, A. M. Using repeated patterns in snow distribution modeling: An Arctic example. Water Resour. Res. (2010). doi:10.1029/2010WR009434
