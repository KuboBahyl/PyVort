function f = He4density(temperature)
%based on paper by R.J.Donnely and C.F.Barenghi

T_lambda = 2.1768;
rho_lambda = 0.1461087;

t = temperature - T_lambda;
t_a = [t; t.^2];
t_b = [t; t.^2; t.^3; t.^4; t.^5; t.^6; t.^7]; 

a_belTl = [-7.57537, 6.87483]*1e-3;
b_belTl = [3.79937, 1.86557, 4.88345, 0, 0, 0, 0]*1e-3;

a_abTl = [-7.94605, 5.07051]*1e-3;
b_abTl = [-30.3511, -10.2326, -3.00636, 0.240720, -2.45749, 1.53454, -0.308182]*1e-3;

delta_rho_ab = (a_abTl * t_a) .*log(abs(t)) + (b_abTl * t_b);
delta_rho_bel = (a_belTl * t_a) .*log(abs(t)) + (b_belTl * t_b);

delta_rho = (t<0).*delta_rho_bel + (t>0).*delta_rho_ab;
%delta_rho = delta_rho_ab;

%below 1.344 K

rho_0 = 0.1451397;
m = [-1.26935, 7.12413, -16.7461, 8.75342]*1e-5;
T = [temperature.^2;temperature.^3;temperature.^4;temperature.^5];
rho = rho_0 + m*T;

if (temperature < 1.344)
    f = rho * 1e3;
else
f = rho_lambda * (1 + delta_rho)*1e3;
end;

