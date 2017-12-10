%% Processes the fit file completely

function [] = ProcessFitFile(fitFileFolder,fitFilePath,FP,resultsFolder,temperature,fid,filterFilePath)
    %% Get fit file header - determine no. of lines
    
    disp('Reading fit file header ...');
    myLine = fgetl(fid);
    headerSize = -2;
    while ((isempty(str2num(myLine))) || (~isnumeric(str2num(myLine))))
        headerSize = headerSize + 1;
        myLine = fgetl(fid);
    end

    disp('...done.');

    clear myLine closeResult;

    %% Load fit file as table - ignoring header information and define runs

    disp('Loading fit file into table and determining run ranges ...');
    
    myFitTable = readtable(fitFilePath,'Delimiter','\t','HeaderLines',headerSize); 

    %Get run starts (in seconds - absolute time) and ranges (as indices of the fit table)
    runStarts(1) = myFitTable{1,2};
    runRanges(1).Start = 1;
    runRanges(1).End = height(myFitTable);
    for RowIndex = 1:height(myFitTable)
        if (myFitTable{RowIndex,2}~=runStarts(length(runStarts)))
            runRanges(length(runStarts)).End = RowIndex-1;
            runRanges(length(runStarts)+1).Start = RowIndex;
            runStarts(length(runStarts)+1)=myFitTable{RowIndex,2}; 
        end
        runRanges(length(runRanges)).End = RowIndex;
    end

    disp('...done.');

    %clear runStarts;

    % There is no need to actually split the table for each run
    % Access later via: runRanges(RunIndex).Start:runRanges(RunIndex).End

    %% Get data folders for each individual run
    
    disp('Getting folder names for each run ...');
    
    MyDir = dir(resultsFolder);
    runFolders = repmat(struct('Folder','a'),length(MyDir)-2,1);
    formatIn = 'yyyy-mm-dd_HH-MM-SS';

    for RunIndex = 1:length(MyDir)-2
        runFolders(RunIndex).Folder = strcat(resultsFolder,MyDir(RunIndex+2).name,'/',FP.LongName,'/');
        folderExists(RunIndex) = (exist(runFolders(RunIndex).Folder) == 7);
        runFolderTimes(RunIndex) = datenum(MyDir(RunIndex+2).name(5:end),formatIn);
    end

    runStartTimes = LabVIEW2MatlabTime(runStarts);
    timeShift = 2/24; %time shift in days - in folder names with respect to MatlabTime
    
    
    % find the actual folders representing the runs using a minimum of time
    % difference between fit file record and the folder itself
    for RunIndex = 1:length(runRanges)
        [M,I] = min(abs(runStartTimes(RunIndex)+timeShift-runFolderTimes));
        usedFolders(RunIndex) = runFolders(I);
        if (M<(5/1440))
            usedFolderExists(RunIndex) = folderExists(I);        
        else
            usedFolderExists(RunIndex) = false;        
        end
    end
    
    %filter folders if they do not exist...
    runFolders = usedFolders(usedFolderExists);
    %runFolders = usedFolders(ones(1,length(usedFolderExists)));
    runRanges = runRanges(usedFolderExists);
    %runRanges = runRanges(ones(1,length(usedFolderExists)));
    
    disp('...done.');

    clear MyTable folderExists usedFolders usedFolderExists;

    %% Move all files from subfolders into the data folder and delete the subfolders (if any)
    
    disp('Moving files from subfolders to run folders ...');
    
    for RunIndex = 1:length(runFolders)
        MyDir = dir(runFolders(RunIndex).Folder);
        subFolders = MyDir([MyDir(1:length(MyDir)).isdir]==1);
        subFolders = subFolders(3:end);
        for SubIndex = 1:length(subFolders)
            fullSubPath = strcat(runFolders(RunIndex).Folder,subFolders(SubIndex).name,'/');
            MySubDir = dir(fullSubPath);
            subFiles = MySubDir([MySubDir(:).isdir]==0,:);
            for FileIndex = 1:length(subFiles)
                presentFilePath = strcat(fullSubPath,subFiles(FileIndex).name);
                newFilePath = strcat(runFolders(RunIndex).Folder,subFiles(FileIndex).name);
                movefile(presentFilePath,newFilePath);
            end
            rmdir(fullSubPath);
        end
    end

    disp('...done.');
    
    clear MyTable subFolders SubIndex ;

    % this leaves all the data files in the runFolders(RunIndex) directories
    % these data files include f-sweeps as well as other types of data
    % each *.txt file in the given directory has a unique file number -> use as ID

    %% For each run, compose a table of file names of f-sweep files and file numbers, then process them one by one

    disp('Indexing fswp files and processing them ...');
    myFitTable.AttenuationFactor = zeros(length(myFitTable.FileNumber),1); 
    myFitTable.InputRes_Ohm = zeros(length(myFitTable.FileNumber),1);
    myFitTable.TransformerGain = zeros(length(myFitTable.FileNumber),1);
    myFitTable.ModeNumber = zeros(length(myFitTable.FileNumber),1);
    myFitTable.ForkConstant = zeros(length(myFitTable.FileNumber),1);
    myFitTable.CalcAmplitude_Vrms = zeros(length(myFitTable.FileNumber),1);

    numCharacters = ['0','1','2','3','4','5','6','7','8','9','-','+']; % define characters that can represent numbers
    Warn = warning('off','MATLAB:table:ModifiedVarnames');

    for RunIndex = 1:length(runFolders) % The following needs to be done for each run...

        FileIndexStruct = GetFileIndexStructFS(runFolders(RunIndex).Folder); % Make a table linking file numbers to full file paths

        % now process each row of myFitTable belonging to this run, loading the corresponding f-sweep and extracting essential information
        if ~isempty(FileIndexStruct)
            for RowIndex = runRanges(RunIndex).Start:runRanges(RunIndex).End
                % first get the essential information
                if ~isempty(FileIndexStruct([FileIndexStruct(:).Number]==myFitTable.FileNumber(RowIndex)))
                    FSWPFileName = FileIndexStruct([FileIndexStruct(:).Number]==myFitTable.FileNumber(RowIndex)).Name; % get the file name from the FileIndexTable, use FileNumber as key
                    disp(FSWPFileName);
                    [myHeader,headerSize] = ReadHeaderFS(FSWPFileName);% open and read the header, at the same time determining the number of lines
                    if (~isnan(headerSize))
                        res = ScanForResistanceGainFS(myHeader,numCharacters);% Find the resistance or I/V gain from the header
                        [attdB,transformerUsed] = ScanForAttenuationTransformerFS(myHeader,numCharacters);% Find the attenuation from the header
                        attMultiplier = 10^(-attdB/20);% convert dB to a multiplier
                      

                        % now for some processing...
                        myFitTable.AttenuationFactor(RowIndex) = attMultiplier; %set the resistance and attenuation for the appropriate file number
                        myFitTable.InputRes_Ohm(RowIndex) = res;

                        if (abs(myFitTable.CenterFrequency_Hz_(RowIndex)-FP.f1)<FP.f1)
                            myFitTable.ModeNumber(RowIndex) = 1;
                            myFitTable.ForkConstant(RowIndex) = FP.a1;
                        elseif (~isnan(FP.f2)&&(abs(myFitTable.CenterFrequency_Hz_(RowIndex)-FP.f2)<FP.f1))
                            myFitTable.ModeNumber(RowIndex) = 2;
                            myFitTable.ForkConstant(RowIndex) = FP.a2;
                        else
                            myFitTable.ModeNumber(RowIndex) = NaN;
                            myFitTable.ForkConstant(RowIndex) = NaN;
                        end

                        if transformerUsed % set the transformer gain used
                            if myFitTable.ModeNumber(RowIndex) == 1
                                myFitTable.TransformerGain(RowIndex) = FP.TrG1;
                            elseif myFitTable.ModeNumber(RowIndex) == 2
                                myFitTable.TransformerGain(RowIndex) = FP.TrG2;
                            else
                                myFitTable.TransformerGain(RowIndex) = NaN;
                            end
                        else
                            myFitTable.TransformerGain(RowIndex) = 1;
                        end
                        myFitTable.CalcAmplitude_Vrms(RowIndex) = CalcFswpAmplitude(FSWPFileName,headerSize,myFitTable.ForkConstant(RowIndex),myFitTable.InputRes_Ohm(RowIndex)); %calculate the new amplitude for each sweep
                        %myFitTable.CalcAmplitude_Vrms(RowIndex) = myFitTable.Amplitude_Vrms_(RowIndex); %or use the fitted values
                    end
                end
            end
        end
        clear FSWPFileName myHeader headerSize res attdB transformerUsed attMultiplier;
    end

    warning(Warn.state,Warn.identifier);

    disp('...done.');

    clear Warn FileIndexTable;

    %% Finally calculate the desired quantities across the entire myFitTable

    disp('Calculating additional quantities ...');
    
      % Electrical quantities, but corrected
      myFitTable.RealExcit_Vrms = myFitTable.Excitation_Vrms_.*myFitTable.AttenuationFactor.*myFitTable.TransformerGain; %Real Excitation - drive corrected for attenuation and transformer (where applicable)
      myFitTable.RealAmpl_Arms = myFitTable.CalcAmplitude_Vrms./myFitTable.InputRes_Ohm; % Just converts voltage to current; uses the calculated amplitude
      myFitTable.CorrAmpl_Excit_invOhm = myFitTable.RealAmpl_Arms./myFitTable.RealExcit_Vrms; %Corrected Amplitude/Real Excitation
      myFitTable.CorrAmplXWidth_Excit_invOhmsec = myFitTable.RealAmpl_Arms.*myFitTable.Linewidth_Hz_./myFitTable.RealExcit_Vrms; %height * width / drive (corrected amplitude * width / real excitation)
      myFitTable.CorrExcit_Ampl_2_Ohm_invA = myFitTable.RealExcit_Vrms./(myFitTable.RealAmpl_Arms.^2); % Real Excitation / (Corrected Amplitude)^26

       
      % Mechanical quantities
      myFitTable.Force_N_peak = sqrt(2)/2*myFitTable.ForkConstant.*myFitTable.RealExcit_Vrms;%Calculate peak force[N]
      myFitTable.Velocity_m_invs_peak = sqrt(2)*myFitTable.RealAmpl_Arms./myFitTable.ForkConstant;%Calculate peak velocity[ms-1]
      myFitTable.Power_W = myFitTable.Force_N_peak.*myFitTable.Velocity_m_invs_peak./2;%Calculate mean power
      myFitTable.DragCoef = 2*myFitTable.Force_N_peak./(myFitTable.Velocity_m_invs_peak.^2 * FP.L * FP.W * He4density(temperature));% Calculate the drag coefficient

      disp('...done.');


    %% Get the temperature time trace, and the table of fixed "nominal" temperatures

%     disp('Reading the temperature time trace ...');
%     
%     AVSfolder = 'd:\mff\!exp\data\fridge\avs-47\2014-11-27\'; % specify folder with thermometry data
%     StartDate = '2014-12-01 00:00:00'; % trace starting from this date/time
%     EndDate = '2015-07-01 00:00:00'; % ending at this date/time
%     TempTrace = GetTempTrace(AVSfolder,StartDate,EndDate); % extract the time trace
% 
%     FixedTempFilename = 'd:\mff\!exp\software\Matlab\Forks_SS\Fixed_temperatures.txt';
%     FixedTempTable = GetFixedTempTable(FixedTempFilename,true,true,TempTrace); % load the table with "fixed" temperatures
% 
%     disp('...done.');
% 
%     clear AVSfolder StartDate EndDate FixedTempFilename;


    %% Add temperature information to myFitTable

    disp('Calculating and writing temperature info to the fit table ...');
    
    %initialize variables
    myFitTable.MatlabTimeStart=zeros(height(myFitTable),1);
    myFitTable.MatlabTimeEnd=zeros(height(myFitTable),1);
    myFitTable.NominalTemp_mK=zeros(height(myFitTable),1);
%     myFitTable.Tavg_mK=zeros(height(myFitTable),1);
%     myFitTable.Tmin_mK=zeros(height(myFitTable),1);
%     myFitTable.Tmax_mK=zeros(height(myFitTable),1);
%     myFitTable.Tstdev_mK=zeros(height(myFitTable),1);
%     myFitTable.TempDiff_mK=zeros(height(myFitTable),1);

    %fill in values
    for RowIndex = 1:height(myFitTable)
        myRow = table2struct(myFitTable(RowIndex,:));
        myFitTable.MatlabTimeStart(RowIndex) = LabVIEW2MatlabTime(myRow.RunStart_s_ + myRow.StartTime_s_); % calculate matlab times
        myFitTable.MatlabTimeEnd(RowIndex) = LabVIEW2MatlabTime(myRow.RunStart_s_ + myRow.EndTime_s_); % calculate matlab times
%        myFitTable.NominalTemp_mK(RowIndex) = GetNominalTemp(FixedTempTable,myFitTable.MatlabTimeStart(RowIndex),myFitTable.MatlabTimeEnd(RowIndex)); % get the nominal temperature (if in transient -> NaN)
        myFitTable.NominalTemp_mK(RowIndex) = temperature*1000; % get the nominal temperature (if in transient -> NaN)
%        myFitTable(RowIndex,{'Tavg_mK','Tmin_mK','Tmax_mK','Tstdev_mK'}) = GetRealTemp(TempTrace,myFitTable.MatlabTimeStart(RowIndex),myFitTable.MatlabTimeEnd(RowIndex)); % get the real temperature
%        myFitTable.TempDiff_mK(RowIndex) = myFitTable.Tavg_mK(RowIndex) -  myFitTable.NominalTemp_mK(RowIndex); % temperature difference from the nominal one
    end

    disp('...done.');

    %% Split to individual nominal temperatures and modes

    disp('Splitting data according to nominal tempratures and resonant modes; writing into separate files ...');
    
%    myFilterStruct = LoadFilterStruct(filterFilePath);
    
%    for TempIndex = 1:height(FixedTempTable)
%        myFitSubTable = myFitTable(myFitTable.NominalTemp_mK == FixedTempTable.T_approx_mK(TempIndex),:);
        myFitSubTable = myFitTable;
        for ModeIndex = 1:4
            myFitSubSubTable = myFitSubTable(myFitSubTable.ModeNumber == ModeIndex,:);
            %%myFilePath = strcat(fitFileFolder,'Fork_',FP.Name,'_mode_',num2str(ModeIndex),'_fs_',num2str(FixedTempTable.T_approx_mK(TempIndex)),'mK.dat');
            myFilePath = strcat(fitFileFolder,'Fork_',FP.Name,'_mode_',num2str(ModeIndex),'_fs_',num2str(1300),'mK.dat');
            
%             matched = NaN;
%             for Index = 1:length(myFilterStruct)
%                 if (strcmp(myFilterStruct(Index).FitFileName,myFilePath))
%                     matched = Index;
%                 end
%             end
%             
%             if height(myFitSubSubTable)>0
%                 writetable(myFitSubSubTable,myFilePath,'Delimiter','\t');
% 
%                 if (~isnan(matched))
%                     myFilterData = myFilterStruct(matched);
%                 
%                     if (~(isnan(myFilterData.Start1)||isnan(myFilterData.End1)))
%                         myFilteredTable = myFitSubSubTable(myFitSubSubTable.FileNumber>=myFilterData.Start1 & myFitSubSubTable.FileNumber<=myFilterData.End1,:);
%                     end
% 
%                     if (~(isnan(myFilterData.Start2)||isnan(myFilterData.End2)))
%                         myFilteredTable = vertcat(myFilteredTable,myFitSubSubTable(myFitSubSubTable.FileNumber>=myFilterData.Start2 & myFitSubSubTable.FileNumber<=myFilterData.End2,:));
%                     end
% 
%                     if (~(isnan(myFilterData.Start3)||isnan(myFilterData.End3)))
%                         myFilteredTable = vertcat(myFilteredTable,myFitSubSubTable(myFitSubSubTable.FileNumber>=myFilterData.Start3 & myFitSubSubTable.FileNumber<=myFilterData.End3,:));
%                     end
% 
%                     if (~(isnan(myFilterData.Start4)||isnan(myFilterData.End4)))
%                         myFilteredTable = vertcat(myFilteredTable,myFitSubSubTable(myFitSubSubTable.FileNumber>=myFilterData.Start4 & myFitSubSubTable.FileNumber<=myFilterData.End4,:));
%                     end
%                     
%                     if (~exist('myFilteredTable','var'))
%                         myFilteredTable = myFitSubSubTable;
%                     end
%                     
%                     myFilteredFixedTable = FixTrG(myFilteredTable,myFilterData.TrG,FP,temperature);
% 
%                 else
%                     myFilteredFixedTable = myFitSubSubTable;
%                 end
%                 
%                 myFilteredFilePath = strcat(fitFileFolder,'Fork_',FP.Name,'_mode_',num2str(ModeIndex),'_fs_',num2str(FixedTempTable.T_approx_mK(TempIndex)),'mK_filtered.dat');
%                 writetable(myFilteredFixedTable,myFilteredFilePath,'Delimiter','\t');
%             end
        end
%    end

    disp('...done.');

    clear myFitSubTable myFilePath;

    %% Save the entire fit file

    disp('Saving the entire new fit file ...');
    
    writetable(myFitTable,fitFilePath,'Delimiter','\t');

    disp('...done.');
end
        
