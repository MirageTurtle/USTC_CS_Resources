#! /usr/local/bin/bash
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

declare -i test_id=1
declare -i n=0
# devices=["cpu","gpu"]

for device in "cpu";
do
    # while [ $test_id -lt 3 ]
    for test_id in 1 2 3;
    # for test_id in 3;
    do
        echo "testing: ${device}${test_id}"
        n=0
        while [ $n -lt 11 ]
        do
            command="./${device}${test_id}.out ${n}"
            result=$(${command})
            if [ ${result: -1} == "s" ]
            then
                echo -e "${GREEN}SUCCESS!${NC}n: ${n} Time cost: ${result}"
            else
                echo -e "${RED}FAILURE!${NC}"
            fi
            n+=1
        done
    done
done