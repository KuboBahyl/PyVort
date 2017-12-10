function [myFilterStruct] = LoadFilterStruct(filterFilePath)
    myFilterStruct = table2struct(readtable(filterFilePath,'Delimiter','\t','Format','%s %f %f %f %f %f %f %f %f %f')); % read data
end