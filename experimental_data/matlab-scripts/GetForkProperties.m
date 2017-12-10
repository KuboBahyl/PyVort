%% Loads tuning fork settings from a table in a text file

function [forkproperties] = GetForkProperties(settingsFilePath,ForkIndex)
%% Load the settings file into a table
forkproperties = table2struct(readtable(settingsFilePath,'Delimiter','\t','Format','%s %s %f %f %f %f %f %f %f %f %f %f %f')); % read data
forkproperties = forkproperties(ForkIndex); % select the correct fork