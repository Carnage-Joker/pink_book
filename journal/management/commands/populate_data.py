from django.core.management.base import BaseCommand
from journal.models import Resource, ResourceCategory, ResourceComment
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        self.populate_data()

    def populate_data(self):
        CustomUser = get_user_model()

        # Creating sample users for comments
        user1, created = CustomUser.objects.get_or_create(
            sissy_name="MissSissy-fried",
            email="dpinkprincess1@thepinkprincess.com",
            defaults={'is_staff': True, 'password': "iamasissysoso1234"}
        )
        if created:
            user1.set_password("iamasissysoso1234")
            user1.save()

        user2, created = CustomUser.objects.get_or_create(
            sissy_name="QueensissyPrincess",
            email="dsissy@thepinkprincess.com",
            defaults={'is_staff': True, 'password': "iamasissysoso1234"}
        )
        if created:
            user2.set_password("iamasissysoso1234")
            user2.save()

        # Creating resources
        resource1 = Resource.objects.get_or_create(
            title="Transgender Map",
            description="Comprehensive guide on transitioning and understanding gender identity.",
            link="https://www.transgendermap.com",
            allow_comments=True
        )

        resource2 = Resource.objects.get_or_create(
            title="Sissy School",
            description="A supportive community with forums, chat rooms, and resources for sissies.",
            link="https://www.sissyschool.com",
            allow_comments=True
        )

        resource3 = Resource.objects.get_or_create(
            title="SissyLovr",
            description="A range of realistic toys and products tailored for sissies.",
            link="https://www.sissylovr.com",
            allow_comments=True
        )

        resource4 = Resource.objects.get_or_create(
            title="Trevor Project",
            description="Crisis intervention and suicide prevention services for LGBTQ youth.",
            link="https://www.thetrevorproject.org",
            allow_comments=True
        )

        resource5 = Resource.objects.get_or_create(
            title="Gender Spectrum",
            description="Resources for exploring gender and understanding non-binary identities.",
            link="https://www.genderspectrum.org",
            allow_comments=True
        )

        resource6 = Resource.objects.get_or_create(
            title="Sissify",
            description="Offers training programs, guides, and resources for sissies to embrace their femininity.",
            link="https://www.sissify.com",
            allow_comments=True
        )

        resource7 = Resource.objects.get_or_create(
            title="En Femme",
            description="Fashion and lingerie designed specifically for crossdressers and sissies.",
            link="https://www.enfemme.com",
            allow_comments=True
        )

        # Adding 10 more resources
        resource8 = Resource.objects.get_or_create(
            title="Transformation Magazine",
            description="Monthly publication dedicated to the art of crossdressing and gender transformation.",
            link="https://www.transformation.co.uk",
            allow_comments=True
        )

        resource9 = Resource.objects.get_or_create(
            title="Jessica Who?",
            description="A popular blog and YouTube channel that discusses life as a crossdresser.",
            link="https://www.jessica-who.com",
            allow_comments=True
        )

        resource10 = Resource.objects.get_or_create(
            title="Crossdresser Heaven",
            description="Community and resources for crossdressers, including forums, articles, and support groups.",
            link="https://www.crossdresserheaven.com",
            allow_comments=True
        )

        resource11 = Resource.objects.get_or_create(
            title="The Gender Reveal Podcast",
            description="Podcast that interviews non-binary and transgender individuals, sharing their stories and experiences.",
            link="https://www.genderpodcast.com",
            allow_comments=True
        )

        resource12 = Resource.objects.get_or_create(
            title="FTM Magazine",
            description="Magazine dedicated to the female-to-male transgender community.",
            link="https://www.ftmmagazine.com",
            allow_comments=True
        )

        resource13 = Resource.objects.get_or_create(
            title="Wicked Wanda's",
            description="Store offering a wide range of adult toys, lingerie, and accessories.",
            link="https://www.wickedwandas.ca",
            allow_comments=True
        )

        resource14 = Resource.objects.get_or_create(
            title="Trans Femme",
            description="Dedicated to providing transgender women with information, resources, and support.",
            link="https://www.transfemme.com",
            allow_comments=True
        )

        resource15 = Resource.objects.get_or_create(
            title="The Sissy Parlor",
            description="A blog that shares tips, stories, and resources for sissies and crossdressers.",
            link="https://www.thesissyparlor.com",
            allow_comments=True
        )

        resource16 = Resource.objects.get_or_create(
            title="Pink Essentials",
            description="Online store offering sissy essentials, from clothing to accessories.",
            link="https://www.pinkessentials.com",
            allow_comments=True
        )

        resource17 = Resource.objects.get_or_create(
            title="Glamour Boutique",
            description="Retailer specializing in crossdressing and transgender clothing, wigs, and makeup.",
            link="https://www.glamourboutique.com",
            allow_comments=True
        )

        # Creating resource categories
        self_discovery = ResourceCategory.objects.get_or_create(
            name="Self-Discovery")
        support_communities = ResourceCategory.objects.get_or_create(
            name="Support Communities")
        guides_tutorials = ResourceCategory.objects.get_or_create(
            name="Guides and Tutorials")
        shopping = ResourceCategory.objects.get_or_create(name="Shopping")
        mental_health = ResourceCategory.objects.get_or_create(
            name="Mental Health")
        books_literature = ResourceCategory.objects.get_or_create(
            name="Books and Literature")

        # Assign resources to categories
        self_discovery[0].resources.add(
            resource1[0], resource5[0], resource14[0])
        support_communities[0].resources.add(
            resource2[0], resource10[0], resource11[0], resource15[0])
        guides_tutorials[0].resources.add(
            resource6[0], resource9[0], resource13[0])
        shopping[0].resources.add(
            resource3[0], resource7[0], resource8[0], resource16[0], resource17[0])
        mental_health[0].resources.add(resource4[0])
        books_literature[0].resources.add(resource12[0])

        # Creating comments
        ResourceComment.objects.get_or_create(
            content="This guide is amazing!", author=user1, resource=resource1[0])
        ResourceComment.objects.get_or_create(
            content="So helpful and supportive!", author=user2, resource=resource2[0])
        ResourceComment.objects.get_or_create(
            content="I found exactly what I needed!", author=user1, resource=resource3[0])
        ResourceComment.objects.get_or_create(
            content="Great resource for mental health!", author=user2, resource=resource4[0])

        self.stdout.write(self.style.SUCCESS(
            'Successfully populated the database with sample data'))
