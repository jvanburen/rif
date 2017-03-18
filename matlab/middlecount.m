function [lo, hi] = middlecount(A, k)
    if ndims(A) ~= 1
        A = A(:);
    end
    S = sort(A);
    N = numel(S) - 1;
    cutoff = (1.0 - k) / 2.0;
    lo = S(1 + floor(N * cutoff));
    hi = S(1 + floor(N * (1.0 - cutoff)));
end