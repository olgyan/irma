from math import e

temp_in = int(input("Температура в помещении, °С: "))
temp_out = int(input("Температура на улице, °С: "))
rh_in = int(input("Относительная влажность в помещении, %: "))/100
rh_out = int(input("Относительная влажность на улице, %: "))/100
ah_in = (6.112 * (e ** ((17.67*temp_in) / (243.5 + temp_in)
) * rh_in * 2.1674)) / (273.15 + temp_in)
ah_out = (6.112 * (e ** ((17.67 * temp_out) / (243.5 + temp_out)
) * rh_out * 2.1674)) / (273.15 + temp_out)
rh_new = ah_out * (273.15 + temp_in) / (6.112 * (e ** (
(17.67 * temp_in) / (243.5 + temp_in)) * 2.1674))

print("Проветриваем")
if rh_new > 1:
    print("Конденсат выпадет")
elif rh_new > rh_in:
    print(f"Влажность увеличится до {int(rh_new*100)}%")
elif rh_new < rh_in:
    print(f"Влажность уменьшится до {int(rh_new*100)}%")
else:
    print("Влажность останется какая была")
