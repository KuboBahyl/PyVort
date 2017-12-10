function [FileIndexStruct] = GetFileIndexStructFS(runFolder)
    MyDir = dir(strcat(runFolder,'*fs*.txt')); % get all f-sweep files info (*fs*.txt only)
%    if (height(MyTable) == 1)
%        MyTable(2,:) = MyTable(1,:);
%    end
    
    FileIndexStruct = repmat(struct('Number',0,'Name','a'),length(MyDir),1); % preallocate
    %(zeros(height(MyTable),1),MyTable.name,'VariableNames',{'Number','Name'});
    for FileIndex = 1:length(MyDir) % fill array with correct data
        filename = MyDir(FileIndex).name;
%        if iscell(filename)
%            filename = filename{1,1};
%        end
        FileIndexStruct(FileIndex).Name = strcat(runFolder,filename); % store the file name as an absolute path
        j = max(strfind(filename,'_')); % get lower bound of the file number
        k = max(strfind(filename,'.')); % get upper bound of the file number
        FileIndexStruct(FileIndex).Number = str2num(filename(j+1:k-1)); % get and store the file number
    end
end