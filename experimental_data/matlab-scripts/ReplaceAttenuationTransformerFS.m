function [newHeader] = ReplaceAttenuationTransformerFS(myHeader,numCharacters,newValuedB)
    key = 'dB';
    index = strfind(myHeader,key);
    if ~isempty(index)
        while (~ismember(myHeader(index),numCharacters)) % skips non-numerical characters from the value of index to the front
            index = index - 1;
        end
        endIndex = index;
        numString = '';
        while (ismember(myHeader(index),numCharacters)) % keeps together the charactgers representing the last number
            numString = strcat(myHeader(index),numString);
            index = index - 1;;
        end
        startIndex = index;
        newHeader = strcat(myHeader(1:startIndex-1),strrep(myHeader(startIndex:endIndex),numString,num2str(newValuedB)),myHeader(endIndex+1:end));
    end
end
