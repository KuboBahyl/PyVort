function [MatlabTime] = LabVIEW2MatlabTime (LabVIEWtime)
    formatIn = 'yyyy-mm-dd HH:MM:SS';
    LabVIEWzero = datenum('1904-01-01 00:00:00',formatIn);
    LabVIEWfactor = 60*60*24;
    MatlabTime = LabVIEWtime/LabVIEWfactor + LabVIEWzero;
end