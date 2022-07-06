#! /usr/local/bin/bash
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# clear output
$(rm -rf ./output/*)

path_length=(5 8 10 14 15 20 23 25 27 28 30 32)
# echo "${path_length[0]}"

declare -i test_num=0
declare -i start
declare -i end
# h_func="A_h2"
# h_func="IDA_h2"
for h_func in "A_h1" "A_h2" "IDA_h1" "IDA_h2";
# for h_func in "A_h2" "IDA_h1" "IDA_h2";
# for h_func in "IDA_h1" "IDA_h2";
do
    echo -e "Test function ${h_func}\n"
    test_num=0
    while [ $test_num -lt 12 ]
    # for test_num in 10;
    do
        str_num=$(printf '%02d' $test_num)
        echo "testing: ${str_num}"
        command="./a.out ${h_func} input${str_num}.txt target${str_num}.txt"
        # echo "command: ${command}"
        start=$(gdate +%s%N)
        return_str=$(${command})
        end=$(gdate +%s%N)
        # delta_time=$(( (${end}-${start}) / 1000000000 ))
        delta_time=$(echo "scale=4;(${end}-${start}) / 1000000000" | bc)
        echo "Time: ${delta_time}s"
        if [ $return_str == "Failure" ]
        then
            echo -e "${RED}Failure!${NC} without solution."
        else
            length=$(echo -n ${return_str} | wc -c)
            str_length=$(printf '%d' $length)
            if [ ${length} == ${path_length[test_num]} ]
            then
                echo -e "${GREEN}Success!${NC} with solution: ${return_str}."
            else
                echo -e "${RED}Failure!${NC} with $str_length-step solution: ${return_str}."
            fi
        fi
        test_num+=1
    done
done