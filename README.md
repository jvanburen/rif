# Resistance Is Futile

See our devpost at https://devpost.com/software/resistance-is-futile/

## Inspiration
Resistors have coded colored bands that you can use to tell their resistance values.
We have a friend in ECE who is red-green colorblind, so he can't read resistor color bands, because he can't distinguish them.

## What it does
You put a resistor onto the green plate and its camera reads the color bands, and tells you the decoded value.

## How we built it
We designed a housing for the pi and the camera that would ensure even lighting for the video. We took training images of resistors and trained our computer vision algorithms to recognize the resistors and their colors. Then we designed a display to show the decoded values.

## Challenges we ran into
Our original computer vision algorithm was too slow for the raspberry pi.

## Accomplishments that we're proud of
We're proud it works at all!

## What we learned
We learned about the importance of good training data and the importance of starting early.

## What's next for Resistance Is Futile
Adjust the housing: Make it more robust. Improve the CV algorithms to both run faster and give better results. Maybe add a sorting feature in a future iteration.

## Specifics of the implementation
Don't judge us too much, this was a hackathon, not a Computer Vision homework!

Training:
1. We take training images and manually pick out the resistor color bands and the background.
2. We train a NormalBayesClassifier (`bg_classifier`) to recognize the background vs the resistor.
3. We train a NormalBayesClassifier (`color_classifier`) to distinguish the different resistor colors.

Running:
1. capture an input image `I` and convert it to the CIE L*a*b* color space
2. Down-sample `I` to 256x256
3. Apply `bg_classifier` to each pixel to get a rough estimate of foreground vs background
4. Apply the morphological opening operator with a 5x5 box kernel (5 iterations)
5. Find the largest contour `C` in the resulting image, check its area is in the range [800, 2300] pixels.
6. Scale up `C` and pick the corresponding pixels from the original (not down-sampled) image I
7. Apply `color_classifier` to each pixel in the contour.
8. Find the 3 most commonly occurring colors. (We're not looking for the gold/silver bands!)
9. Find the centroid of the contour `C`
10. Find the centroid of the pixels in each of the most commonly occurring colors
11. Determine which color `r` has the centroid furthest from the centroid of `C`. This is the color band on the edge.
12. Sort the other 2 colors by the distance from their centroids to the centroid of `r`. This should give us the correct ordering of color bands.
13. Look up the color bands in a table and display the result.
