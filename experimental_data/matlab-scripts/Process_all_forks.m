%% Processes all fork data sequentially
clear all;

Forks = int16([1 2 3 4 5 6 7]); % list of all tuning forks available
ProcessForks = int16([2]); % tuning forks to process
Folder1 = struct('Name','../Data-Clean/Sample/'); %%path to fit files folder
FolderList = [Folder1];

for ForkIndex = Forks(ProcessForks);
    for FolderIndex = 1:length(FolderList)
        disp(ForkIndex);
        disp(FolderList(FolderIndex).Name);
        fitFileFolder = FolderList(FolderIndex).Name; %file path to fit files
        LoadFitFile(fitFileFolder,ForkIndex);
    end
end