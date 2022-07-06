start=$(gdate +%s%N)
command="./a.out"
return_str=$(${command})
end=$(gdate +%s%N)
delta_time=$(echo "scale=4;(${end}-${start}) / 1000000000" | bc)
echo "Time: ${delta_time}s"
echo "Result: ${return_str}"