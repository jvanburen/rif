function [res] = catcomps(im)
    res = vertcat(im(:,:,1), im(:,:,2), im(:,:,3));
end