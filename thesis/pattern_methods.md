# Snow Depth Pattern Similarity

Snow depth patterns at CLPX and Happy Valley are replicated year after year with great fidelity (Figure w/ annual insets and some stats - can have statistical (i.e. CV and spatial info (moran's I) and even a fractical (hausdorff>?) component.)). The inter-annual similarity is created by the consistent arrangement of two snow classes: snowdrift and scour. While the size and shape of snowdrifts does change each year, their location and general morphology does not, and this produces
very consistent gradient values in the snow depth pattern.

Snow patterns exist in nature on landscapes where wind and topography
structure the distribution of snow.  A snow pattern is a spatial distribution of a physical snow variable (usually depth, though it could be density, etc.) which that is spatially autocorrelated but neither uniform nor random. In tundra snow regions, the patterns arise where the wind and topography structure the distribution of the snow. Prior studies (REFS) have shown that this interaction produces patterns that appear “similar” from one year to the next, but what does “similar” mean?

Measuring the similarity of one pattern to another is not trivial. Although comparing two spatial patterns is intuitively simple for humans, it can be a complex task for machines. Quantitative image (i.e. pattern) quality assessment (IQA) is an active field of research at the intersection of signal processing and human vision science. Work in that field has shown that there is no single best method for measuring the similarity of two patterns, but by selecting and applying a set of IQA tools, a more sophisticated assessment of similarity can be done. Here, we have adapted these tools and created a toolbox that we have used to examine tundra snow pattern similarities and differences. The toolbox allows us to define a novel and more continuous scale for “similarity” which permits more subtle differentiation than a simple  binary “similar or not similar” metric. This more sophisticated analysis allows new avenues of exploration of snow patterns, and (as we show) leads to more nuanced knowledge about snow-wind-topography processes.

We use CW-SSIM. A major drawback of the conventional (i.e. spatial) domain SSIM algorithm is that it is highly sensitive to translation, scaling and rotation of images. Extending the method to the complex
  wavelet transform domain makes it insensitive to these “non-structured” image distortions that are typically caused
  by the movement of the image acquisition devices, rather than the changes of the structures of the objects in the
  visual scene.




But just how similar are they?

Something must be dribing that similarity.
We know snowdrifts are a function of landscape and weather - but how much is landscape. We don't have good weather control (maybe reanalysis shows something) but we know it is more variable than landscape. Weather cant capture the complexity of blowing snow

So what is it about the landscape? We know a drift landscape needs these things: Obstacles, Slope Breaks, Just changing topography and elevation, influenced by both upwind and downwind (how far?) factors.


 Landscape is the
So can we search an array for these landscape factors?
