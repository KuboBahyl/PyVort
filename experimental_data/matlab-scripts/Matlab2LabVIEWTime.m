function [LabVIEWtime] = Matlab2LabVIEWTime (MatlabTime)
    formatIn = 'yyyy-mm-dd HH:MM:SS';
    LabVIEWzero = datenum('1904-01-01 00:00:00',formatIn);
    LabVIEWfactor = 60*60*24;
    LabVIEWtime = (MatlabTime - LabVIEWzero) * LabVIEWfactor;
end