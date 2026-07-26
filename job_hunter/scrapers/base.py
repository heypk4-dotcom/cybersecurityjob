from abc import ABC, abstractmethod

class BaseScraper(ABC):
    
    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def search_jobs(self, keywords, location):
        pass

    @abstractmethod
    def extract_job_details(self):
        """
        Should return a list of dictionaries, each containing:
        {title, company, location, link, description}
        """
        pass
