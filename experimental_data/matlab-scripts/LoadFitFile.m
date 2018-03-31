%% Processing of tuning fork data from *.fit files

function [] = LoadFitFile(fitFileFolder,ForkIndex)
    %% Settings and initialization
    % Tuning fork settings
    forksettingsfile = 'SS_fork_settings.txt';%path to file with fork properties
    FP = GetForkProperties(forksettingsfile,ForkIndex); % load fork properties (Name,LongName,L,T,W,D,rho,HWD)
    FP.Meff = 0.25*FP.T*FP.W*FP.L*FP.rho; % calculate the effective mass
    FP.a1 = sqrt(4*pi*FP.Meff*FP.HWD1); % calculate the fork constant from the loaded HWD
    FP.a2 = sqrt(4*pi*FP.Meff*FP.HWD2);

    %filtering by file number table
    filterFilePath = 'Filenumber_filter.txt';

    disp('Retrieving settings ...');

    MyDir = dir(strcat(fitFileFolder,'Results'));
    tempFolders = repmat(struct('Folder','a'),length(MyDir)-2,1);
    tempStrings = repmat(struct('Str','a'),length(MyDir)-2,1);
        
    for tempIndex = 1:length(MyDir)-2
        tempStrings(tempIndex).Str = MyDir(tempIndex+2).name;
        tempFolders(tempIndex).Folder = strcat(fitFileFolder,'Results/',tempStrings(tempIndex).Str,'/');
        folderExists(tempIndex) = (exist(tempFolders(tempIndex).Folder) == 7);
    end

    tempFolders = tempFolders(folderExists);
    
    for tempIndex = 1:length(tempFolders)
        resultsFolder = tempFolders(tempIndex).Folder; % path to results folder
        temperature = str2double(tempStrings(tempIndex).Str); %% (K) used for calculating density in ProcessFitFile.m
        
        % Filenames and paths

        disp('...done.');
        clear forksettingsfile ForkIndex;

        %% Change file extensions from .fit to .dat (if not done) - for ease of use

        disp('Getting file paths ...');
        fitFilePath = strcat(fitFileFolder,'Fork_',FP.Name,'_fs.fit');
        fitFilePath2 = strrep(fitFilePath,'fit','dat');

        if (exist(fitFilePath, 'file') == 2)
            copyfile(fitFilePath,fitFilePath2,'f');
            fitFilePath = fitFilePath2;
        end;

        fitFilePath = fitFilePath2;

        disp('...done.');
        clear fitFilePath2;

        %% Process fit file

        fid = fopen(fitFilePath);
        if (fid~=-1)
            ProcessFitFile(fitFileFolder,fitFilePath,FP,resultsFolder,temperature,fid,filterFilePath);
            closeResult = fclose(fid);
        end
    
    end
end
