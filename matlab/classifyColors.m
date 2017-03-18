function [classified, I] = classifyColors(I, resistorBW, Mdl)
%     color2rgb = struct('bg', [1 1 1], ...
%                       'orange', [1 0.5 0], ...
%                       'gold',   [0 0.1 0.5], ...
%                       'purple', [0.5 0 0.5], ...
%                       'yellow', [1 1 0], ...
%                       'blackbg', [0 0 0]);
                    % 'gold',   [1 215.0/255.0 0], ...
    color2rgb = [1 1 1 ; 1 0.5 0 ; 0 0.1 0.5 ; 0.5 0 0.5 ; 1 1 0 ; 0 0 0];
    I = normalizeRGB(I);
    
    lab = rgb2lab(I);
    L = lab(:,:,1);
    A = lab(:,:,2);
    B = lab(:,:,3);
    
    
    indices = find(resistorBW);
%     disp 'classifying...' 
    colornames = Mdl.predict([L(indices), A(indices), B(indices)]);
%     disp 'prettifying...'
    [Ri,Gi,Bi] = deal(I(:,:,1),I(:,:,2),I(:,:,3));
   
    classified = zeros(size(resistorBW), 'int8');
    for ii = 1:numel(indices)
        colorname = colornames(ii);
%         rgbcolor = color2rgb.(colorname{:});
        
        rgbcolor = color2rgb(colorname, :);
        i = indices(ii);
        classified(i) = colorname;
        Ri(i) = rgbcolor(1);
        Gi(i) = rgbcolor(2);
        Bi(i) = rgbcolor(3);
    end
    I = cat(3, Ri, Gi, Bi);
    classified = single(classified);
end