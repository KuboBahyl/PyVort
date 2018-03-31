path ='d:\mff\!exp\data\fridge\2015-02-12\Results\Run_2015-02-12_09-58-43\Tuning fork 5\\Fork_TF5_fs_';
numCharacters = ['0','1','2','3','4','5','6','7','8','9','-','+']; % define characters that can represent numbers

for i = 64:99
    filename = strcat(path,num2str(i),'.dat');
    CorrectHeader(filename,numCharacters,-30); % change dB to -30 -> transformer was used
    filename = strcat(path,num2str(i),'.txt');
    CorrectHeader(filename,numCharacters,-30); % change dB to -30 -> transformer was used
end
