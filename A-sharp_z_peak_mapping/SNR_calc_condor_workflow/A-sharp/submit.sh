#mkdir -p outdir/logs
#condor_submit_dag -usedagdir -outfile_dir outdir job.dag
condor_submit job.sub
