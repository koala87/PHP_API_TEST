awk 'BEGIN{min=9999999} {if($1<min)min=$1 fi} END{print min}'
