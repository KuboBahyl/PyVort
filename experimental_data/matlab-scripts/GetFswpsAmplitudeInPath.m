function GetFswpsAmplitudeInPath(myPath)

    numCharacters = ['0','1','2','3','4','5','6','7','8','9','-','+']; % define characters that can represent numbers
    results = struct('Temp_K',0,'Mode','','NominalDrive_Vrms',0,'Amplitude_Vrms',0);
   
    forksettingsfile = 'd:\mff\!exp\software\Matlab\Forks_SS\SS_fork_settings.txt';%path to file with fork properties
    FP = GetForkProperties(forksettingsfile,1); % load fork properties (Name,LongName,L,T,W,D,rho,HWD)
    FP.Meff = 0.25*FP.T*FP.W*FP.L*FP.rho; % calculate the effective mass
    FP.a1 = sqrt(4*pi*FP.Meff*FP.HWD1); % calculate the fork constant from the loaded HWD
    FP.a2 = sqrt(4*pi*FP.Meff*FP.HWD2);
    
    listing = struct2cell(dir(myPath));
    listing = listing(1,3:end);
    tempDirs = strcat(myPath,listing,'\');
    temperatures = str2double(strrep(listing,'p','.'));

    l=0;
    for i=1:length(tempDirs)
        myNewPath = char(tempDirs(1,i));
        listing = struct2cell(dir(myNewPath));
        listing = listing(1,3:end);
        modeDirs = strcat(myNewPath,listing,'\');
        modes = char(listing);

        for j=1:length(modeDirs)
            myNewPath = char(modeDirs(1,j));
            listing = struct2cell(dir(strcat(myNewPath,'*.txt')));
            listing = listing(1,:);
            fswpFiles = strcat(myNewPath,listing);
            drives = str2double(strrep(listing,'.txt',''));
            
            for k=1:length(fswpFiles)
                
                display(char(fswpFiles(k)));
                [myHeader,headerSize] = ReadHeaderFS(char(fswpFiles(k)));% open and read the header, at the same time determining the number of lines
                if (~isnan(headerSize))
                    res = ScanForResistanceGainFS(myHeader,numCharacters);% Find the resistance or I/V gain from the header

                    if (modes(j,:)=='fund')
                        ForkConstant = FP.a1;
                    elseif (modes(j,:)=='over')
                        ForkConstant = FP.a2;
                    else
                        ForkConstant = NaN;
                    end
                Amplitude = CalcFswpAmplitude(char(fswpFiles(k)),6,ForkConstant,res);
                l=l+1;
                Results(l).Temp_K = temperatures(i);
                Results(l).Mode = modes(j,:);
                Results(l).NominalDrive_Vrms = drives(k);
                Results(l).Amplitude_Vrms = Amplitude;
    
                end
            end
        end
    end
    
    writetable(struct2table(Results),strcat(myPath,'Results.dat'),'Delimiter','\t');
end