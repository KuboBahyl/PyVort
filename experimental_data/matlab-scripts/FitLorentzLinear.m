function [Intercept,Slope,AmplitudeVrms,LinewidthHz,CenterfreqHz,phaseRad,FUV,est_max] = FitLorentzLinear(fileName,headerSize)
%% performs a Lorentzian fit (with linear bgnd) on the data in an f-sweep file

%% Load the f-sweep file into a table after handling decimal points vs. commas (also creates a *.dat) and do the fitting
    
    format long;
    
    newFileName = strrep(fileName,'.txt','.dat'); % put together a new file name for the modified files
    fidold = fopen(fileName); % open the existing file
    fidnew = fopen(newFileName,'w');
    if ((fidold~=-1)&&(fidnew~=-1))
        myLine = fgetl(fidold);

        while ischar(myLine)% replace decimal commas for points
            fprintf(fidnew,'%s\n',strrep(myLine,',','.'));
            myLine = fgetl(fidold);
        end
        fclose(fidold);
        fclose(fidnew);

        % read data from file
        FswpData = readtable(newFileName,'Delimiter','\t','HeaderLines',headerSize); % read the data into a table
        
        a = [0 0 0 0 0]; % define parameter vector for first fitting function
        b = [0 0 0 0 0 0]; % define parameter vector for second fitting function
        % a(1) - bgnd intercept;
        % a(2) - bgnd slope;
        % a(3) - amplitude*linewidth^2;
        % a(4) - linewidth;
        % a(5) - frequency^2;
        
        % define fitting variables (frequency and in-phase response)
        f = FswpData.Frequency_Hz_;
        ampl = FswpData.X_Vrms_;
        
        % if frequencies are non-singular
        if(f(1)~=f(2))
            
            % define fitting function (Lorentzian absorption + linear bgnd)
            F = @(a,freq)a(1) + freq*a(2) + a(3)./(a(4)^2+((freq-a(5)./freq).^2));
            % define another fitting function (Lorentzian absorption +
            % dispersion + linear bgnd)
            G = @(b,freq)b(1) + freq*b(2) + cos(b(6))*b(3)./(b(4)^2+((freq-b(5)./freq).^2)) - sin(b(6))*b(3)/b(4).*(b(5)./freq - freq)./(b(4)^2+((freq-b(5)./freq).^2));


            % estimate linear bgnd
            my_x = [f(2),f(end-1)]';
            my_y = [ampl(2),ampl(end-1)]';
            bgnd = [ones(length(my_x),1) my_x]\my_y; 

            % estimate Lorentzian
            corr_y = ampl-(bgnd(1) + f*bgnd(2));
            est_max = max(corr_y);
            my_freq = f(find(corr_y==est_max,1));

            my_width = abs((f(1) - f(end))/8);
            my_amplitude = est_max;

            y0 = [bgnd(1) bgnd(2) my_amplitude*my_width^2 my_width my_freq^2 0]; % initial parameter values

            % specify fitting options
            options = optimoptions('lsqcurvefit','Algorithm','levenberg-marquardt','TolFun',1e-14,'TolX',1e-14,'ScaleProblem','Jacobian','MaxFunEvals',10000,'MaxIter',2000);

            %parameter lower and upper bounds
            lb = [];
            ub = [];

            % select data near end points to determine the background
            my_x = [f(1),f(2),f(3),f(4),f(end-3),f(end-2),f(end-1),f(end)]';
            my_y = [ampl(1),ampl(2),ampl(3),ampl(4),ampl(end-3),ampl(end-2),ampl(end-1),ampl(end)]';

            % preliminary fit of ends to get real bgnd
            [y,resnorm,residual,exitflag,output] = lsqcurvefit(G,y0,my_x,my_y,lb,ub,options);

            % fix our estimates
            corr_y = ampl-(y(1) + f*y(2));
            est_max = max(corr_y); % this might be used as amplitude if the fit quality is not great
            my_freq = f(find(corr_y==est_max,1));

            my_width = abs((f(1) - f(end))/8);
            my_amplitude = est_max;

            x0 = [y(1) y(2) my_amplitude*my_width^2 my_width my_freq^2 0]; % initial parameter values

            % do the real fitting
            [x,resnorm,residual,exitflag,output] = lsqcurvefit(G,x0,f,ampl,lb,ub,options);

            % visual check of the fit                
            %plot(f,ampl,'ro')
            %hold on
            %plot(f,F(x,f))
            %hold on
            %plot(f,y(1)+y(2)*f)
            %hold off

            SS_data = sum(((ampl-(x(1)+x(2)*f)) - mean(ampl-(x(1)+x(2)*f))).^2); % sum of squares (linear bgnd withdrawn)
            SS_fit = resnorm; % sum of squares of the residuals
            FUV = SS_fit/SS_data; % fraction of unexplained variance
            Intercept = x(1);
            Slope = x(2);
            AmplitudeVrms = x(3)/(x(4)^2);
            LinewidthHz = x(4);
            CenterfreqHz = sqrt(x(5));
            phaseRad = x(6);
        else
            FUV = 1; % fraction of unexplained variance
            Intercept = 0;
            Slope = 0;
            AmplitudeVrms = 0;
            LinewidthHz = 0;
            CenterfreqHz = 0;
            phaseRad = 0;
            est_max = 0;
        end
    else
        FUV = 1; % fraction of unexplained variance
        Intercept = 0;
        Slope = 0;
        AmplitudeVrms = 0;
        LinewidthHz = 0;
        CenterfreqHz = 0;
        phaseRad = 0;
        est_max = 0;
    end
end
        