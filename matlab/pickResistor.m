function [I, poly] = pickResistor(impath)
    close all;
    I = imread(impath);
    imshow(I);
    h = impoly;
    api = iptgetapi(h);
    poly = api.createMask;
    close all;
end