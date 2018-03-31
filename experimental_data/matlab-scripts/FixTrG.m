function [myFilteredFixedTable] = FixTrG(myFilteredTable,newTrG,FP,temperature)
    for RowIndex = 1:length(myFilteredTable.TransformerGain)
        if (~(myFilteredTable.TransformerGain(RowIndex)==1))
            myFilteredTable.TransformerGain(RowIndex) = newTrG;
        end
    end
    
    % correct electrical quantities
    myFilteredTable.RealExcit_Vrms = myFilteredTable.Excitation_Vrms_.*myFilteredTable.AttenuationFactor.*myFilteredTable.TransformerGain; %Real Excitation - drive corrected for attenuation and transformer (where applicable)
    myFilteredTable.RealAmpl_Arms = myFilteredTable.CalcAmplitude_Vrms./myFilteredTable.InputRes_Ohm; % Just converts voltage to current; uses the calculated amplitude
    myFilteredTable.CorrAmpl_Excit_invOhm = myFilteredTable.RealAmpl_Arms./myFilteredTable.RealExcit_Vrms; %Corrected Amplitude/Real Excitation
    myFilteredTable.CorrAmplXWidth_Excit_invOhmsec = myFilteredTable.RealAmpl_Arms.*myFilteredTable.Linewidth_Hz_./myFilteredTable.RealExcit_Vrms; %height * width / drive (corrected amplitude * width / real excitation)
    myFilteredTable.CorrExcit_Ampl_2_Ohm_invA = myFilteredTable.RealExcit_Vrms./(myFilteredTable.RealAmpl_Arms.^2); % Real Excitation / (Corrected Amplitude)^26

    % correct mechanical quantities
    myFilteredTable.Force_N_peak = sqrt(2)/2*myFilteredTable.ForkConstant.*myFilteredTable.RealExcit_Vrms;%Calculate peak force[N]
    myFilteredTable.Velocity_m_invs_peak = sqrt(2)*myFilteredTable.RealAmpl_Arms./myFilteredTable.ForkConstant;%Calculate peak velocity[ms-1]
    myFilteredTable.Power_W = myFilteredTable.Force_N_peak.*myFilteredTable.Velocity_m_invs_peak./2;%Calculate mean power
    myFilteredTable.DragCoef = 2*myFilteredTable.Force_N_peak./(myFilteredTable.Velocity_m_invs_peak.^2 * FP.L * FP.W * He4density(temperature));% Calculate the drag coefficient
    
    myFilteredFixedTable = myFilteredTable;
end
