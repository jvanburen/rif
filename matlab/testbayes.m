% load('test.mat', 'I', 'polymask');
% I = I;
% polymask = polymask;
lab = rgb2lab(I);

Lcomp = lab(:,:,1);
Acomp = lab(:,:,2);
Bcomp = lab(:,:,3);

LcompRes = Lcomp(polymask);
AcompRes = Acomp(polymask);
BcompRes = Bcomp(polymask);

Lall = getprob(Lcomp, Lcomp, 100);
Lres = getprob(Lcomp, LcompRes, 100);
Aall = getprob(Acomp, Acomp, 255);
Ares = getprob(Acomp, AcompRes, 255);
Ball = getprob(Bcomp, Bcomp, 255);
Bres = getprob(Bcomp, BcompRes, 255);

Lprob = Lres ./ Lall;
Aprob = Ares ./ Aall;
Bprob = Bres ./ Ball;

prod = Lprob .* Aprob .* Bprob;
probBlur = imgaussfilt(prod, 4);

thresh = probBlur > 0.005;
filled = imfill(thresh, 'holes');

resistor = bwareaopen(filled, 1000);

function [prob] = getprob(input, values, nbins)
    [N,edges] = histcounts(values, nbins);
    prob = discretize(input,edges,N);
end

function [prob] = makehist(values, nbins)
    [N,edges] = histcounts(values, nbins);
    prob = discretize(input,edges,N);
end