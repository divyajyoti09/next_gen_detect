#mkdir -p outdir/logs
#condor_submit_dag -usedagdir -outfile_dir outdir job.dag
condor_submit job_from_job_ids2.sub
