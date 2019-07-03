clear;clc;
inputfile = strcat('lottery.csv');lottery = dlmread(inputfile);
for a=1:1:72
    EU(a,1)=lottery(a,2)*lottery(a,3)+lottery(a,4)*lottery(a,5)+lottery(a,6)*lottery(a,7);  % EU risk neutral
    if lottery(a,7)~=0
        MedLot(a,1)=lottery(a,4);                                       % median income
        RandLot(a,1)=lottery(a,6)+(lottery(a,2)-lottery(a,6))*rand;     % random income
    else
        MedLot(a,1)=(lottery(a,2)+lottery(a,4)+1)/2;                    % median income
        RandLot(a,1)=lottery(a,4)+(lottery(a,2)-lottery(a,4))*rand;     % random income
    end
end
% Average income; col 1 = EU income, col 2 = median lottery income, col 3 = random lottery income
avincome(1,1)=mean(EU);avincome(1,2)=mean(MedLot);avincome(1,3)=mean(RandLot);