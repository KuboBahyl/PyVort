%% Loads the time trace of temperatures from StartDate to EndDate. These need to be provided as strings in the same format as the time strings in the AVS files (specified below for parsing).

function [TempTrace] = GetTempTrace(AVSfolder,StartDate,EndDate)
    AVSfilename = CombineAVSfiles(AVSfolder,'all.dat'); % join all AVS files in the folder to one (and add header)
    MyAVStable = readtable(AVSfilename,'Delimiter','\t'); % load as table
    
    formatIn = 'yyyy-mm-dd HH:MM:SS'; % format of the time records in the joined file
    StartTime = datenum(char(StartDate),formatIn); % convert time strings to Matlab times
    EndTime = datenum(char(EndDate),formatIn); % convert time strings to Matlab times
    MyAVStable.MatlabTimes = datenum(char(MyAVStable.DateTime),formatIn); % convert time strings to Matlab times
    MyAVStable = MyAVStable((MyAVStable.MatlabTimes >= StartTime) & (MyAVStable.MatlabTimes <= EndTime),:); % select elements between StartTime and EndTime (included)
    
    TempTrace = table(MyAVStable.MatlabTimes,MyAVStable.R_mixMR_Ohm,MyAVStable.T_mixMR_mK,'VariableNames',{'MatlabTime' 'R_Ohm' 'T_mK'}); % specify which thermometer to use
    TempTrace = TempTrace(~isnan(TempTrace.T_mK),:); % leave out NaNs
    clear MyAVStable;   
end