%% Loads the table of fixed temperatures from a file and optionally computes statistics and overwrites the file

function [FixedTempTable] = GetFixedTempTable(filename,CalcFromTrace,Write,TempTrace)
    if (exist(filename,'file'))
        FixedTempTable = readtable(filename,'Delimiter','\t'); % load as table and sort in ascending order
    else
        varnames = {'T_approx_mK' 'StartTime' 'EndTime' 'T_avg_mK' 'T_min_mK' 'T_max_mK' 'T_stdev_mK'}; % specify variable names
        FixedTempTable = table([],[],[],[],[],[],[],'VariableNames',varnames); % create an empty table with the correct variable names
    end
    
    FixedTempTable = sortrows(FixedTempTable,'T_approx_mK'); % sort according to tamperature labels
    
    formatIn = 'yyyy-mm-dd HH:MM:SS'; % specify format of time strings
    if ischar(FixedTempTable.StartTime)% convert time strings to Matlab times
        FixedTempTable.StartTime = datenum(FixedTempTable.StartTime,formatIn);
    end
    if ischar(FixedTempTable.EndTime) % convert time strings to Matlab times
        FixedTempTable.EndTime = datenum(FixedTempTable.EndTime,formatIn);
    end
    
    if (CalcFromTrace && (exist('TempTrace') == 1)) % optionally recalculate statistics
        for RowIndex = 1:length(FixedTempTable.T_approx_mK)
            TraceExtract = TempTrace((TempTrace.MatlabTime >= FixedTempTable.StartTime(RowIndex)) & (TempTrace.MatlabTime <= FixedTempTable.EndTime(RowIndex)),:); % extract a portion of the time trace
            FixedTempTable(RowIndex,4:end) = GetTempTraceStats(TraceExtract); % Get the statistics and write them
        end
    end
    
    if Write
        writetable(FixedTempTable,filename,'Delimiter','\t'); % optionally overwrite file with modified table
    end
end