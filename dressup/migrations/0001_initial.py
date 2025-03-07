# Generated by Django 5.1.2 on 2025-01-30 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Avatar',
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image_path", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "body",
                    models.CharField(
                        choices=[
                            ("01", "straight_body"),
                            ("02", "curvy_body"),
                            ("03", "hourglass_body"),
                            ("04", "pear_body"),
                            ("05", "apple_body"),
                            ("06", "athletic_body"),
                            ("07", "petite_body"),
                        ],
                        default="01",
                        max_length=2,
                    ),
                ),
                (
                    "skin",
                    models.CharField(
                        choices=[
                            ("01", "light"),
                            ("02", "medium"),
                            ("03", "dark"),
                            ("04", "pale"),
                            ("05", "tan"),
                        ],
                        default="light",
                        max_length=10,
                    ),
                ),
                (
                    "hair",
                    models.CharField(
                        choices=[
                            ("01", "short_hair"),
                            ("02", "long_straight_hair"),
                            ("03", "long_curly_hair"),
                            ("04", "long_wavy_hair"),
                            ("05", "bob_cut"),
                            ("06", "pig_tails"),
                            ("07", "bald"),
                            ("08", "short_curly_hair"),
                            ("09", "short_wavy_hair"),
                            ("10", "long_straight_bangs"),
                            ("11", "long_curly_bangs"),
                            ("12", "long_wavy_bangs"),
                            ("13", "bob_cut_bangs"),
                            ("14", "pig_tails_bangs"),
                            ("15", "short_curly_bangs"),
                            ("16", "short_wavy_bangs"),
                        ],
                        default="01",
                        max_length=2,
                    ),
                ),
                (
                    "hair_color",
                    models.CharField(
                        choices=[
                            ("01", "black"),
                            ("02", "brown"),
                            ("03", "blonde"),
                            ("04", "red"),
                            ("05", "blue"),
                            ("06", "green"),
                            ("07", "purple"),
                            ("08", "pink"),
                            ("09", "rainbow"),
                        ],
                        default="black",
                        max_length=10,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "shoes",
                    models.CharField(
                        choices=[
                            ("00", "ugly shoes"),
                            ("01", "Sneakers"),
                            ("02", "Boots"),
                            ("03", "Heels"),
                            ("04", "Flats"),
                            ("05", "Sandals"),
                            ("06", "Wedges"),
                            ("07", "Mules"),
                            ("08", "Pumps"),
                            ("09", "Platforms"),
                            ("10", "Ankle Boots"),
                            ("11", "Thigh High Boots"),
                            ("12", "Knee High Boots"),
                        ],
                        default="00",
                        max_length=100,
                    ),
                ),
                (
                    "accessories",
                    models.CharField(
                        choices=[
                            ("00", "None"),
                            ("01", "Hat"),
                            ("02", "Scarf"),
                            ("03", "Gloves"),
                            ("04", "Sunglasses"),
                            ("05", "Handbag"),
                            ("06", "Necklace"),
                            ("07", "Bracelet"),
                            ("08", "Earrings"),
                            ("09", "collar"),
                            ("10", "Belt"),
                        ],
                        default="00",
                        max_length=100,
                    ),
                ),
                (
                    "skirt",
                    models.CharField(
                        choices=[
                            ("00", "ugly shorts"),
                            ("01", "Mini Skirt"),
                            ("02", "Midi Skirt"),
                            ("03", "Maxi Skirt"),
                            ("04", "Pencil Skirt"),
                            ("05", "Pleated Skirt"),
                            ("06", "A-Line Skirt"),
                        ],
                        default="00",
                        max_length=100,
                    ),
                ),
                (
                    "top",
                    models.CharField(
                        choices=[
                            ("00", "ugly top"),
                            ("01", "T-Shirt"),
                            ("02", "Blouse"),
                            ("03", "Crop Top"),
                            ("04", "Bra"),
                            ("05", "Corset"),
                            ("06", "Bustier"),
                        ],
                        default="00",
                        max_length=100,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("body", "Body"),
                            ("hair", "Hair"),
                            ("top", "Tops"),
                            ("skirt", "Skirts"),
                            ("shoes", "Shoes"),
                            ("accessory", "Accessories"),
                            ("makeup", "Makeup"),
                            ("wig", "Wigs"),
                            ("jewellery", "Jewellery"),
                            ("lingerie", "Lingerie"),
                            ("background", "Backgrounds"),
                        ],
                        max_length=50,
                    ),
                ),
                ("image_path", models.CharField(blank=True, max_length=200, null=True)),
                ("price_points", models.IntegerField(blank=True, default=0, null=True)),
                (
                    "price_dollars",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=6, null=True
                    ),
                ),
                ("premium_only", models.BooleanField(default=False)),
                ("is_locked", models.BooleanField(default=False)),
                ("description", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="LeaderboardEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("points", models.IntegerField()),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PhotoShoot',
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "photographer_type",
                    models.CharField(
                        choices=[
                            ("photo_booth", "Photo Booth"),
                            ("creepy", "Creepy Photographer"),
                            ("hot", "Hot Photographer"),
                        ],
                        max_length=20,
                    ),
                ),
                ("purchased_at", models.DateTimeField(auto_now_add=True)),
                ("image", models.ImageField(upload_to="photoshoots/")),
                ("used", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PurchasedItem',
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("purchased_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("is_equipped", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("shop_id", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "shop_type",
                    models.CharField(
                        choices=[
                            ("salon", "Salon"),
                            ("thrift_shop", "Thrift Shop"),
                            ("high_end", "High-End Department"),
                            ("designer", "Designer"),
                            ("jewellery", "Jewellery"),
                            ("lingerie", "Lingerie"),
                            ("shoes", "Shoes"),
                            ("designer_shoes", "Designer Shoes"),
                            ("wig_shop", "Wig Shop"),
                            ("gym", "Gym"),
                            ("bank", "Bank"),
                            ("photography_studio", "Photography Studio"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "shop_level",
                    models.CharField(
                        choices=[
                            ("basic", "Basic"),
                            ("premium", "Premium"),
                            ("cute", "Cute"),
                            ("hawt", "Hawt"),
                            ("sexy", "Sexy"),
                        ],
                        default="basic",
                        max_length=50,
                    ),
                ),
                ("premium_only", models.BooleanField(default=False)),
                ("is_locked", models.BooleanField(default=False)),
                ("description", models.TextField(blank=True)),
                ("image_path", models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]
