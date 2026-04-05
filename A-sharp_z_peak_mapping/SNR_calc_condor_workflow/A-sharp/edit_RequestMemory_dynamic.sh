#!/usr/bin/sh
condor_q -held \
-constraint 'regexp("(?i)memory usage", HoldReason)' \
-af ClusterId ProcId RequestMemory \
| while read cid pid mem; do
    job="${cid}.${pid}"
    new_mem=$((mem + 2048))
    echo "$job: $mem -> $new_mem"
    condor_qedit "$job" RequestMemory "$new_mem"
    condor_release "$job"
done
