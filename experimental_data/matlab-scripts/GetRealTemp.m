function [RealTempData] = GetRealTemp(TempTrace,StartTime,EndTime)
    TraceSubset = TempTrace((TempTrace.MatlabTime >= StartTime) & (TempTrace.MatlabTime <= EndTime),:);
    if (length(TraceSubset.MatlabTime) > 0)
        T_avg_mK = sum(TraceSubset.T_mK)/length(TraceSubset.T_mK); % use average T
        T_min_mK = min(TraceSubset.T_mK);
        T_max_mK = max(TraceSubset.T_mK);
        T_stdev_mK = std(TraceSubset.T_mK);
    else
        myIndex = find(TempTrace.MatlabTime > StartTime,1);
        T_future_mK = TempTrace.T_mK(myIndex); % find T at nearest future point
        T_past_mK = TempTrace.T_mK(max(1,myIndex-1)); % find T at nearest past point
        T_avg_mK = (T_future_mK+T_past_mK)/2;
        T_min_mK = min([T_future_mK,T_past_mK]);
        T_max_mK = max([T_future_mK,T_past_mK]);
        T_stdev_mK = std([T_future_mK,T_past_mK]);
    end
    RealTempData = table(T_avg_mK,T_min_mK,T_max_mK,T_stdev_mK,'VariableNames',{'T_avg_mK','T_min_mK','T_max_mK','T_stdev_mK'});
end