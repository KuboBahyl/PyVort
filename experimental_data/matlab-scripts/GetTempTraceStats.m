%% Calculates statistics of temperature time trace

function [StatsTable] = GetTempTraceStats(TraceExtract)
    if (length(TraceExtract.T_mK)>0)
        avg = sum(TraceExtract.T_mK)/length(TraceExtract.T_mK);
        mini = min(TraceExtract.T_mK);
        maxi = max(TraceExtract.T_mK);
        stdev = std(TraceExtract.T_mK);
    else
        avg = NaN;
        mini = NaN;
        maxi = NaN;
        stdev = NaN;
    end
    StatsTable = table(avg,mini,maxi,stdev);
end
