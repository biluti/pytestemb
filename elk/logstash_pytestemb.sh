until ~/bin/logstash-1.4.2/bin/logstash -f ~/workspace/elastic/logstash_pytestemb.txt; do
    echo "#########################################################"
    echo "'logstash' exit with code $?.  Respawning.." >&1
    echo "#########################################################"
    echo "wait 30 sec"
    sleep 30
    echo "retry"
done
