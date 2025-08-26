from django.core.management.base import BaseCommand
# from jobs.models import Job
import requests
from bs4 import BeautifulSoup
from django.utils import timezone

from scraper_api_service.jobs.models import Job


class Command(BaseCommand):
    help = "Scrape jobs from remoteok.com"

    def handle(self, *args, **kwargs):
        url = "https://remoteok.com/api"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, "html.parser")

        job_rows = soup.find_all("tr", class_="job")

        for job in job_rows:
            title = job.find("h2")
            company = job.find("h3")
            link = "https://remoteok.com"

            if title and company and link:
                Job.objects.update_or_create(
                    url="https://remoteok.com" + link,
                    defaults={
                        "title": title.get_text(strip=True),
                        "company": company.get_text(strip=True),
                        "posted_at": timezone.now(),
                    }
                )
        self.stdout.write(self.style.SUCCESS("Jobs scraped successfully!"))
