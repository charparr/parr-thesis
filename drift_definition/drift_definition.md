# Defining drifts

<p>
What exactly is meant by the term 'drift' in the world of snow? Most snow scientists colloquially understand a drift to be an accumulation of snow deposited by wind, often found in the lee of a break in slope or obstacle like a tree or fence. In the field, the 'eyeball' threshold test of "I know a drift when I see it" will suffice. However, that 'eyeball' test is informed by a full set of 3-D information including geometry, texture, shadowing, and even color. In a planar, map-view world of snow depth like that presented here, how should we formally distinguish drift snow from 'not-drift' snow across an entire snow-covered landscape with a variety of snow classes and hetergenous depth? What is the appropriate threshold, and why? Clearly the eyeball test will not suffice because we lack the field perspective and because the map view of Arctic tundra snow depth is complex with nebulous transitions. To clarify our thinking about drifts, we need a quanititative threshold that is consistent across domains and snow classes yet easily computable for each individual case.
</p>
<p>
In search of such a threshold we compute several statistics for many test drift threshold values for each snow depth dDEM (N = 12): the areal fractions of drift and not drift snow, the mean depths of drift and not drift snow, and the snow volume fractions of drift and not-drift snow. We also compute hyspometric curves of drift and not drift snow. Choosing a threshold value relies on knowing the relative depth of drift snow compared to not drift snow. We know drifts are deeper, but by how much? We test drift threshold snow depth values calibrated by the mean snow depth of the entire domain (80% to 200% of the mean depth at 10% intervals).
</p>
<p>
Imagine a world where snow depth is entirely uniform. There are no real drifts, and you could lower the threshold until you reached the mean (and constant) snow depth and not change the drift volume or area fractions (both are zero in this case). After the threshold reaches the mean and constant value of the snow depth, eveything becomes a drift and the volume and areal fractions become 100%. The fractional values, when plotted against the threshold values, become step functions. As our snow world becomes more complex and realistic, we will smooth the step function and change the shape. We would expect that at low threshold values where more snow is considered to be a drift, that increasing the threshold decreases the fractional amount of drift area and drift volume by about the same amount. In other words, by increasing the threshold we are not yet leaving out any drift snow. However, at some threshold value above the mean snow depth this behavior changes, and now the the drift volume decreases more rapidly than the areal fraction because we are leaving out drifts (smaller areas of deeper snow). As the threshold approaches the maximum snow depth, the drift fractional area and volume curves converge and approach zero. The increasing threshold produces an inflection point in the trajectory of the difference between fractional drift volume and drift area (Figure 1).
</p>

###### Figure 1. An Example of a Drift Threshold Test: Fractional Areal and Volume (CLPX, 2017)
![alt text](drift_thresholds_area_vol_CLPX_2017.png)

<p>
The threshold corresponding to the inflection point is where we have already excluded drift snow as indicated by the disparate reductions in fractional drift volume and area. At this threshold we can then conservatively classify all snow of greater or equal depth to be a drift. To make this analysis more global, we have included seven snow depth dDEMs from the Tuolumne Meadows area. This data, collected by ASO in April 2014, represents a much snowier world and a far more rugged environment. The drift volume-area delta curves for each snow dDEM (Figure 2) indicate a range of curves exist across time and study areas, but the inflection threshold is well constrained between 120 and 160 percent of the mean snow depth. Despite the differences in both snow and landscape across each study area, the mean inflection thresholds (vertical lines, Figure 2) are tightly clustered. Rather, it is the drift fractional volume-area delta that indicate signficant distinction (95% confidence).



</p>

###### Figure 2. Summary of the Inflection Drift Thresholds Tests (N = 19) ![alt text](delta_curves_thresholds_study_area_hue.png#1)

<p>
The intersecting areal curves (Figure 1) indicate a space where we might find a suitable depth boundary between drift and not drift snow. When the threshold is low, the drift area and volume are greater than the not-drift area and volume. This makes sense because we are including relatively shallow snow (e.g. 80% of the mean) in the drift category. As the threshold increases, the not-drift areal and volume fractions overtake the drift areal and volume fractions. A threshold somewhere to the right of this intersection (located around 115% in Figure 1) will ensure that there are more areas of not-drift snow than drift-snow, which is consistent with our knowledge and experience with drifts: they are not the most prevalent snow class by area are instead scattered about the landscape. A third curve in Figure 1 indicates the difference between the volume percentage of drift snow and the areal percentage. We see that drifts account for more volume than area, and that there is actuall an inflection point in this curve. At some threshold, the slope of the green line begins to increase and approach zero. The inflection point indicates that a threshold has been reached where enough depth is captured such that increasing the threshold does not 'leave' out significant snow deposits, i.e. by leaving more area out of the drift category, the volume-area relationship stops changing. A good drift threshold, we would expect changes the volume area relationship at each step. By including a little more area, we can include a lot more snow, and conversely by decreasing the area..we decrease the volume by a similar amount until we exclude all the not-drift snow.


We would expect that drifts are larger in years where the threshold is lower, and smaller in years where the threshold is higher.

We would expect that high CVs in the snow depth dDEM produce high thresholds.
interpret as CV

hypsometeric curves (context already existing)
volume filling curves
hyspometric curves for drift and not drift

is the inflection point of the snow depth hypsometric curve a good drift threshold?

does the mean inflection change by study area?

130% of mean.f
