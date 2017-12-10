function [NominalTemp_mK] = GetNominalTemp(FixedTempTable,StartTime,EndTime)
    NominalTemp_mK = NaN;
    for RowInd = 1:length(FixedTempTable.T_approx_mK)
        if ((StartTime >= FixedTempTable.StartTime(RowInd)) && (EndTime <= FixedTempTable.EndTime(RowInd)))
            NominalTemp_mK = FixedTempTable.T_approx_mK(RowInd);
        end
    end
end