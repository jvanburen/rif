function showhsv(rgb)
    hsvimg = rgb2hsv(rgb);
    imshow(cat(1,hsvimg(:,:,1).^2, hsvimg(:,:,2).^2, hsvimg(:,:,3).^2));
end