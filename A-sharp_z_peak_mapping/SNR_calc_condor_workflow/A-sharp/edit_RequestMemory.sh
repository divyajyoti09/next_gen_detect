condor_q -hold 153161035 | awk 'NR>4 {print $1}' | while read job; do
    condor_qedit "$job" RequestMemory 20000
done
