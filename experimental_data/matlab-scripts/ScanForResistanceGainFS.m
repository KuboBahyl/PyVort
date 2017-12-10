function [res] = ScanForResistanceGainFS(myHeader,numCharacters)
    key = 'res';
    index = strfind(myHeader,key); % looks for the key in the header
    if ~isempty(index) 
        myString = myHeader(index(1)+length(key):end); % selects a processing string after the occurrence of 'res'
        while (~ismember(myString(1),numCharacters)) % removes non-numerical characters from the beginning
            myString = myString(2:end);
        end
        numString = '';
        while (ismember(myString(1),numCharacters)) % keeps together the charactgers representing the first number
            numString = strcat(numString,myString(1));
            myString = myString(2:end);
        end
        res = str2double(numString); %scans the numerical string and returns the value of the resistance
        else
        res = 1000; % if the key is not found, assume that the measurement was done with IV converter of 1k gain; can't go too wrong anyway
    end
end
