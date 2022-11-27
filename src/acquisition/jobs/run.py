class RunJobsFromDB:
    
    def __init__(self, listen_job, decoder_job, update_status):
        self.listen_job = listen_job
        self.decoder_job = decoder_job
        self.update_status = update_status

    def __call__(self, listen_status):
        while True:
            jobs = self.listen_job(listen_status)
            for job in jobs:
                self.update_status.running(job['id'])
                try:
                    self.decoder_job(job)()
                    self.update_status.done(job['id'])
                except Exception as error:
                    error = str(error)
                    self.update_status.error(job['id'], error)