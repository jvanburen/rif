function [therows, thenames] = makeRowName(structure, name, k, data, names)
    if nargin < 2 || isempty(k) || k < numel(structure.A)
        randidcs = randperm(numel(structure.A), k);
        therows = horzcat(structure.L(randidcs), structure.A(randidcs), structure.B(randidcs));
    else
        therows = horzcat(structure.L, structure.A, structure.B);
    end
    
    if nargin >= 4 && ~isempty(data)
        therows = vertcat(data, therows);
    end
    
    replacenames = nargin < 5 || isempty(names);
    if isnumeric(name)
        thenames = zeros(numel(randidcs), 1);
        thenames(:) = name;
        if replacenames
            thenames = names;
        else
            thenames = vertcat(names, thenames);
        end
    else
        thenames = cell(numel(randidcs), 1);
        thenames(:) = {name};
        if replacenames
            thenames = names;
        else
            thenames = [names; thenames];
        end
    end
end