class JobDescriptionSummarizer:
    def __init__(self, gemini_api):
        self.gemini_api = gemini_api

    def summarize(self, job_description):
        return self.gemini_api.get_job_description_summary(job_description)
