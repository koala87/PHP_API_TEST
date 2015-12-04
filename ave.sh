cat tmp | awk '{sum+=$1} END{print sum/NR}'
