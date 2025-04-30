from django.core.management.base import BaseCommand
from journal.models import Resource


class Command(BaseCommand):
    help = 'Populate the Resource model with predefined entries'


    def handle(self, *args, **kwargs):
        resources = [
            {
                "title": "Translife UK",
                "description": "Offers a comprehensive range of products, including wigs, silicone breast forms, and clothing, specifically designed for the transgender and sissy community.",
                "link": "https://translife.uk/",
                
            },
            {
                "title": "Venus Sissy Training",
                "description": "Provides insights into sissy fashion trends and styling tips to help individuals express their femininity confidently.",
                "link": "https://www.venussissytraining.com/best-sissy-empowerment-resources-2021-2/",
                
            },
            {
                "title": "Sissy Style Magazine",
                "description": "Features articles on skincare routines and makeup essentials tailored for sissies, promoting self-care and beauty.",
                "link": "https://sissystylemagazine.com/sissy-skincare-makeup/",
                
            },
            {
                "title": "Trans Academy",
                "description": "Offers personalized coaching on makeup application, hairstyling, and skincare routines to assist in gender exploration and transition.",
                "link": "https://transacademy.net/",
            
            },
            {
                "title": "Sissy Hive",
                "description": "Discusses the role of diet and exercise in sissy transformation, emphasizing the importance of maintaining a healthy lifestyle.",
                "link": "https://sissyhive.com/exercise-in-sissy-transformation/",
        
            },
            {
                "title": "She Began",
                "description": "Provides guidance on achieving a healthy body shape and incorporating a balanced diet plan to align with one's feminine identity.",
                "link": "https://shebegan.com/how-to-be-a-good-sissy/",
        
            },
            {
                "title": "Sissy Hive",
                "description": "Offers effective sissy training exercises aimed at transforming one's physique to achieve a more feminine appearance.",
                "link": "https://sissyhive.com/effective-sissy-training-exercises-transform/",
        
            },
            {
                "title": "Venus Sissy Training",
                "description": "Provides advanced sissification methods, including physical exercises, to enhance the sissy transformation journey.",
                "link": "https://www.venussissytraining.com/advanced-sissification-methods-for-transformation-3/",
        
            },
            {
                "title": "2A Magazine",
                "description": "Explores the transformative and empowering aspects of sissy training, offering insights into embracing a sissy lifestyle.",
                "link": "https://2amagazine.com/sissy-training-transformative-and-empowering/",
        
            },
            {
                "title": "Hannah McKnight's Blog",
                "description": "A beginner's guide to crossdressing, providing personal experiences and advice on navigating the sissy lifestyle.",
                "link": "https://hannahmcknight.org/a-beginners-guide-to-crossdressing/",
        
            }
        ]

        for resource_data in resources:
            __, created = Resource.objects.get_or_create(
                title=resource_data["title"],
                defaults={
                    "description": resource_data["description"],
                    "link": resource_data["link"],
        
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'Successfully added resource: {resource_data["title"]}'))
            else:
                self.stdout.write(self.style.WARNING(
                    f'Resource already exists: {resource_data["title"]}'))

        self.stdout.write(self.style.SUCCESS('All resources have been populated successfully.'))

