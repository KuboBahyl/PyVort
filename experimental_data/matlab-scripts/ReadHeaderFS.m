function [myHeader,headerSize] = ReadHeaderFS(fileName)    
    fid = fopen(fileName);
    if (fid~=-1)
        myNewLine = fgetl(fid);
        myHeader = myNewLine; % everything will be put together in one string myHeader (original separate lines will be now separated by semicolons)
        headerSize = -1;
        while ((isempty(str2num(myNewLine))) || (~isnumeric(str2num(myNewLine))))
            headerSize = headerSize + 1;
            myNewLine = fgetl(fid);
            if ((isempty(str2num(myNewLine))) || (~isnumeric(str2num(myNewLine)))) 
                myHeader = strcat(myHeader,';',myNewLine);
            end
        end
        fclose(fid);
    else
        myHeader = '';headerSize = NaN;
    end
end