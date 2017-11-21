#!/bin/bash
# sn 7 : total row 33277
# sn 8 : total row 53310
# rs 7 : 7230
# rs 8 : 10493
#
#
#

TYPE=$1
KEY=$2
DATE=$3
TOT=$4
LOOP=$5

FRST=0
MARGIN=`perl -w -e "use POSIX; print ceil($TOT/$LOOP), qq{\n}"`
LAST=$((MARGIN-1))

#argumen rs 1 6 10 3
echo $TYPE
echo $KEY
echo $DATE
echo $TOT
echo $LOOP

for i in $(seq 1 $LOOP); do
 
  if [ $LAST -ge $TOT ]; then
      echo "step" $i  
      LAST=$TOT
      echo $FRST
      echo $LAST
      echo "jalanin perintah"
      { nohup python step3_bom_crawler.py $TYPE $DATE $FRST $LAST $KEY $i; } 2> log/log_$TYPE_$DATE_$i &
      FRST=$((FRST+MARGIN))
      break
  else
      echo "step" $i     
      echo $FRST
      echo $LAST
      echo "jalanin perintah"
      { nohup python step3_bom_crawler.py $TYPE $DATE $FRST $LAST $KEY $i; } 2> log/log_$TYPE_$DATE_$i &
      LAST=$((LAST+MARGIN))
      FRST=$((FRST+MARGIN))
  fi
done