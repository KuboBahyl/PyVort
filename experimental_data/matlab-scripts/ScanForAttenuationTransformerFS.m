function [attdB,transformerUsed] = ScanForAttenuationTransformerFS(myHeader,numCharacters)
    key = 'dB';
    index = strfind(myHeader,key);
    if ~isempty(index)
        myString = myHeader(1:index-1); % selects a processing string before the occurrence of 'dB'
        while (~ismember(myString(length(myString)),numCharacters)) % removes non-numerical characters from the end
            myString = myString(1:length(myString)-1);
        end
        numString = '';
        while (ismember(myString(end),numCharacters)) % keeps together the charactgers representing the last number
            numString = strcat(myString(end),numString);
            myString = myString(1:length(myString)-1);
        end
        attdB = str2double(numString); %scans the numerical string and returns the value of the resistance
    else
        attdB = 0; % if the key is not found, assume 0 dB
    end
    % check for transformer use (noted usually as -30 dB)
    if (attdB<0)
        transformerUsed = true;
        attdB = 0;
    else
        transformerUsed = false;
    end
end
