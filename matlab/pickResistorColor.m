function [thecolor] = pickResistorColor(I, existing)
    if nargin < 2
        existing = struct('L', [], 'A', [], 'B', []);
    end
    close all;
    imshow(I);
    h = impoly;
    api = iptgetapi(h);
    mask = api.createMask;
    lab = rgb2lab(I);
    L = lab(:,:,1);
    A = lab(:,:,2);
    B = lab(:,:,3);
    thecolor = struct('L', vertcat(existing.L, L(mask)), ...
                      'A', vertcat(existing.A, A(mask)), ...
                      'B', vertcat(existing.B, B(mask)));
    close all;
end
