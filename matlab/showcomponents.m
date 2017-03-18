function [h] = showcomponents(im)
    h = imagesc(cat(1,im(:,:,1), im(:,:,2), im(:,:,3)));
end