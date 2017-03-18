function [cropped, BW] = cropToMask(I, BW) 
    props = regionprops(BW, 'BoundingBox');
    x = floor(props.BoundingBox(1));
    y = floor(props.BoundingBox(2));
    xw = props.BoundingBox(3);
    yw = props.BoundingBox(4);
    cropped = I(y:y+yw, x:x+xw,:);
    BW = BW(y:y+yw, x:x+xw,:);
end