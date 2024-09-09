from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Card(models.Model):
    TYPE_CHOICES = [
        ('Regular', 'Regular'),
        ('Reverse Foil', 'Reverse Foil'),
        ('Foil', 'Foil'),
        ('Rare', 'Rare'),
        ('PSA', 'PSA')
    ]

    GRADE_CHOICES = [
        ('Not Graded', 'Not Graded'),
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5'),
        ('6','6'),
        ('7','7'),
        ('8','8'),
        ('9','9'),
        ('10','10'),
    ]
    SET_CHOICES = [
        # Base Set Era
        ('Base Set', 'Base Set'),
        ('Jungle', 'Jungle'),
        ('Fossil', 'Fossil'),
        ('Base Set 2', 'Base Set 2'),
        ('Team Rocket', 'Team Rocket'),

        # Neo Era
        ('Neo Genesis', 'Neo Genesis'),
        ('Neo Discovery', 'Neo Discovery'),
        ('Neo Revelation', 'Neo Revelation'),
        ('Neo Destiny', 'Neo Destiny'),

        # E-Card Era
        ('Expedition Base Set', 'Expedition Base Set'),
        ('Aquapolis', 'Aquapolis'),
        ('Skyridge', 'Skyridge'),

        # EX Series
        ('EX Ruby & Sapphire', 'EX Ruby & Sapphire'),
        ('EX Sandstorm', 'EX Sandstorm'),
        ('EX Dragon', 'EX Dragon'),
        ('EX Team Magma vs. Team Aqua', 'EX Team Magma vs. Team Aqua'),
        ('EX Hidden Legends', 'EX Hidden Legends'),
        ('EX FireRed & LeafGreen', 'EX FireRed & LeafGreen'),
        ('EX Deoxys', 'EX Deoxys'),
        ('EX Emerald', 'EX Emerald'),
        ('EX Unseen Forces', 'EX Unseen Forces'),
        ('EX Delta Species', 'EX Delta Species'),
        ('EX Legend Maker', 'EX Legend Maker'),
        ('EX Holon Phantoms', 'EX Holon Phantoms'),
        ('EX Crystal Guardians', 'EX Crystal Guardians'),
        ('EX Dragon Frontiers', 'EX Dragon Frontiers'),
        ('EX Power Keepers', 'EX Power Keepers'),

        # Diamond & Pearl Series
        ('Diamond & Pearl Base Set', 'Diamond & Pearl Base Set'),
        ('Mysterious Treasures', 'Mysterious Treasures'),
        ('Secret Wonders', 'Secret Wonders'),
        ('Great Encounters', 'Great Encounters'),
        ('Majestic Dawn', 'Majestic Dawn'),
        ('Legends Awakened', 'Legends Awakened'),
        ('Stormfront', 'Stormfront'),

        # Platinum Series
        ('Platinum Base Set', 'Platinum Base Set'),
        ('Rising Rivals', 'Rising Rivals'),
        ('Supreme Victors', 'Supreme Victors'),
        ('Arceus', 'Arceus'),

        # HeartGold & SoulSilver Series
        ('HeartGold & SoulSilver Base Set', 'HeartGold & SoulSilver Base Set'),
        ('Unleashed', 'Unleashed'),
        ('Undaunted', 'Undaunted'),
        ('Triumphant', 'Triumphant'),

        # Black & White Series
        ('Black & White Base Set', 'Black & White Base Set'),
        ('Emerging Powers', 'Emerging Powers'),
        ('Noble Victories', 'Noble Victories'),
        ('Next Destinies', 'Next Destinies'),
        ('Dark Explorers', 'Dark Explorers'),
        ('Dragons Exalted', 'Dragons Exalted'),
        ('Boundaries Crossed', 'Boundaries Crossed'),
        ('Plasma Storm', 'Plasma Storm'),
        ('Plasma Freeze', 'Plasma Freeze'),
        ('Plasma Blast', 'Plasma Blast'),
        ('Legendary Treasures', 'Legendary Treasures'),

        # XY Series
        ('XY Base Set', 'XY Base Set'),
        ('Flashfire', 'Flashfire'),
        ('Furious Fists', 'Furious Fists'),
        ('Phantom Forces', 'Phantom Forces'),
        ('Primal Clash', 'Primal Clash'),
        ('Roaring Skies', 'Roaring Skies'),
        ('Ancient Origins', 'Ancient Origins'),
        ('BREAKthrough', 'BREAKthrough'),
        ('BREAKpoint', 'BREAKpoint'),
        ('Fates Collide', 'Fates Collide'),
        ('Steam Siege', 'Steam Siege'),
        ('Evolutions', 'Evolutions'),

        # Sun & Moon Series
        ('Sun & Moon Base Set', 'Sun & Moon Base Set'),
        ('Guardians Rising', 'Guardians Rising'),
        ('Burning Shadows', 'Burning Shadows'),
        ('Crimson Invasion', 'Crimson Invasion'),
        ('Ultra Prism', 'Ultra Prism'),
        ('Forbidden Light', 'Forbidden Light'),
        ('Celestial Storm', 'Celestial Storm'),
        ('Lost Thunder', 'Lost Thunder'),
        ('Team Up', 'Team Up'),
        ('Unbroken Bonds', 'Unbroken Bonds'),
        ('Unified Minds', 'Unified Minds'),
        ('Cosmic Eclipse', 'Cosmic Eclipse'),

        # Sword & Shield Series
        ('Sword & Shield Base Set', 'Sword & Shield Base Set'),
        ('Rebel Clash', 'Rebel Clash'),
        ('Darkness Ablaze', 'Darkness Ablaze'),
        ('Vivid Voltage', 'Vivid Voltage'),
        ('Battle Styles', 'Battle Styles'),
        ('Chilling Reign', 'Chilling Reign'),
        ('Evolving Skies', 'Evolving Skies'),
        ('Fusion Strike', 'Fusion Strike'),
        ('Brilliant Stars', 'Brilliant Stars'),
        ('Astral Radiance', 'Astral Radiance'),
        ('Lost Origin', 'Lost Origin'),
        ('Silver Tempest', 'Silver Tempest'),

        # Scarlet & Violet Series
        ('Scarlet & Violet Base Set', 'Scarlet & Violet Base Set'),
        ('Paldea Evolved', 'Paldea Evolved'),
        ('Obsidian Flames', 'Obsidian Flames'),
        ('Paradox Rift', 'Paradox Rift'),
    ]

    name = models.CharField(max_length=255)
    series = models.CharField(max_length=200, choices=SET_CHOICES)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES)

    
    def __str__(self):
        return self.name

class CardImage(models.Model):
    card = models.ForeignKey(Card, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cards/')
    
    def __str__(self):
        return f"Image for {self.card.name}"


class Cart(models.Model):
    session_id = models.CharField(max_length=255)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    added_on = models.DateTimeField(auto_now_add=True)
