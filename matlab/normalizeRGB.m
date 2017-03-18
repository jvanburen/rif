function [RGB] = normalizeRGB(R, G, B)
    
    if (nargin == 1)
      if ismatrix(R)
        B = double(R(:,:));
        G = double(R(:,:));
        R = double(R);
      else
        B = double(R(:,:,3));
        G = double(R(:,:,2));
        R = double(R(:,:,1));
      end
    end

    if (max(R(:)) > 1.0) || (max(G(:)) > 1.0) || (max(B(:)) > 1.0)
      R = R/255;
      G = G/255;
      B = B/255;
    end
    
    RGB = cat(3, R, G, B);
end