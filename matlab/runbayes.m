function [resistor] = runbayes(I, bayes, thresh)
    if (nargin<3) || isempty(thresh)
      thresh = 0.005;
    end
    lab = rgb2lab(I);

    Lcomp = lab(:,:,1);
    Acomp = lab(:,:,2);
    Bcomp = lab(:,:,3);

    Lall = discretize(Lcomp, bayes.LallEdges, bayes.LallHist);
    Lres = discretize(Lcomp, bayes.LresEdges, bayes.LresHist);
    Aall = discretize(Acomp, bayes.AallEdges, bayes.AallHist);
    Ares = discretize(Acomp, bayes.AresEdges, bayes.AresHist);
    Ball = discretize(Bcomp, bayes.BallEdges, bayes.BallHist);
    Bres = discretize(Bcomp, bayes.BresEdges, bayes.BresHist);

    Lprob = Lres ./ Lall;
    Aprob = Ares ./ Aall;
    Bprob = Bres ./ Ball;

    prod = Lprob .* Aprob .* Bprob;
    probBlur = imgaussfilt(prod, 4);

    threshIm = probBlur > thresh;
%     filled = imfill(threshim, 'holes');
    trimmed = bwareaopen(threshIm, 1000);
    resistor = bwconvhull(trimmed);
end