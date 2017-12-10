function [Amplitude] = CalcFswpAmplitude(fileName,headerSize,forkConst,resistor)
  %Load f-sweep file and redo Lorentzian fit
  [Intercept,Slope,AmplitudeVrms,LinewidthHz,CenterfreqHz,phaseRad,FUV,est_max] = FitLorentzLinear(fileName,headerSize);
  
  velocity_threshold = 0.05; % in m/s; this specifies the threshold to consider a sweep "at low drive" or "linear", i.e., where the Lorentzian fit can be trusted
  low_drive_threshold = velocity_threshold*forkConst*resistor; % the same threshold expressed in voltage
  
  
  if(FUV<1) % if the file was read ok
      if((FUV<0.001)|(est_max<=low_drive_threshold)) % if Lorentzian(+linear) fit ok or if very low drive
          Amplitude = AmplitudeVrms; % use the fitted value
      else
          %weight = min((FUV-0.001)*200,1);
          weight = 1; % weight to be used in calculating the final amplitude
          Amplitude = (1-weight)*AmplitudeVrms + (weight)*est_max; %set amplitude to the maximum value (bgnd withdrawn)
      end
  else
       Amplitude = NaN;
  end
end