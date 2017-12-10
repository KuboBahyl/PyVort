%% corrects mistakes in fswp files, especially attenuation value

function [] = CorrectHeader(FSWPFileName,numCharacters,newValuedB)

    [myHeader,headerSize] = ReadHeaderFS(FSWPFileName);
    myHeader = strrep(myHeader,';',char(10));
    newHeader = ReplaceAttenuationTransformerFS(myHeader,numCharacters,newValuedB);

    myLines(1).Line = 'a';

    fid = fopen(FSWPFileName);
    if (fid~=-1)
        for RowIndex = 1:headerSize+1
            myNewLine = fgetl(fid);
        end
        
        myNewLine = fgets(fid);
        index = 1;
        while ischar(myNewLine)
            myLines(index).Line = myNewLine;
            index = index + 1;
            myNewLine = fgets(fid);
        end
        fclose(fid);
    end
    
    fid = fopen(FSWPFileName,'w');
    if (~(fid==-1))
        fprintf(fid,newHeader);
        fprintf(fid,'\n');
        for index = 1:length(myLines)
            fprintf(fid,myLines(index).Line);
        end
        fclose(fid);
    end
end
            

