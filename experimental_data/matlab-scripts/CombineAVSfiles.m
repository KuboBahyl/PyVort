%% Joins all AVS files from the given folder into one file given by filename

function [AVSfilename] = CombineAVSfiles(AVSfolder,AVSfilename)
    AVSTable = struct2table(dir(AVSfolder)); % list everything in the folder
    AVSfiles = AVSTable.name(AVSTable.isdir==0,:); % extract filenames
    AVSfiles = fullfile(AVSfolder,AVSfiles); % and convert to full paths
    clear AVSTable;
    AVSfilename = fullfile(AVSfolder,AVSfilename); % convert to full path
    if (~exist(AVSfilename,'file')) % check if file already exists (in which case do nothing)
        fidAVS = fopen(AVSfilename,'w');
        % print a header
        fprintf(fidAVS,'DateTime\tR_1Kpot_Ohm\tR_still_Ohm\tR_plate_Ohm\tR_mix_Ohm\tR_mixMR_Ohm\tR6_Ohm\tR7_Ohm\tR8_Ohm\tT_1Kpot_mK\tT_still_mK\tT_plate_mK\tT_mix_mK\tT_mixMR_mK\tT6_mK\tT7_mK\tT8_mK\tI_carbon_mA\tI_still_mA\tI_mix_mA\n');
        %copy all lines from all files
        for FileIndex = 1:length(AVSfiles)
            fid = fopen(char(AVSfiles(FileIndex)));
            myNewLine = fgets(fid);
            while (ischar(myNewLine))
                fprintf(fidAVS,'%s',strrep(strrep(myNewLine,',','.'),'-2100000.000000','NaN'));
                myNewLine = fgets(fid);
            end
            fclose(fid);
        end
        fclose(fidAVS);
    end
    clear AVSfiles;
end