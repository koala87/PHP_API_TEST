awk 'BEGIN{max=0} {if($1>max)max=$1 fi} END{print max}'
