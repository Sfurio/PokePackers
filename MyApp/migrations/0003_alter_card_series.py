# Generated by Django 4.2.4 on 2024-09-07 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0002_rename_set_card_series_card_description_card_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='series',
            field=models.CharField(choices=[('Base Set', 'Base Set'), ('Jungle', 'Jungle'), ('Fossil', 'Fossil'), ('Base Set 2', 'Base Set 2'), ('Team Rocket', 'Team Rocket'), ('Neo Genesis', 'Neo Genesis'), ('Neo Discovery', 'Neo Discovery'), ('Neo Revelation', 'Neo Revelation'), ('Neo Destiny', 'Neo Destiny'), ('Expedition Base Set', 'Expedition Base Set'), ('Aquapolis', 'Aquapolis'), ('Skyridge', 'Skyridge'), ('EX Ruby & Sapphire', 'EX Ruby & Sapphire'), ('EX Sandstorm', 'EX Sandstorm'), ('EX Dragon', 'EX Dragon'), ('EX Team Magma vs. Team Aqua', 'EX Team Magma vs. Team Aqua'), ('EX Hidden Legends', 'EX Hidden Legends'), ('EX FireRed & LeafGreen', 'EX FireRed & LeafGreen'), ('EX Deoxys', 'EX Deoxys'), ('EX Emerald', 'EX Emerald'), ('EX Unseen Forces', 'EX Unseen Forces'), ('EX Delta Species', 'EX Delta Species'), ('EX Legend Maker', 'EX Legend Maker'), ('EX Holon Phantoms', 'EX Holon Phantoms'), ('EX Crystal Guardians', 'EX Crystal Guardians'), ('EX Dragon Frontiers', 'EX Dragon Frontiers'), ('EX Power Keepers', 'EX Power Keepers'), ('Diamond & Pearl Base Set', 'Diamond & Pearl Base Set'), ('Mysterious Treasures', 'Mysterious Treasures'), ('Secret Wonders', 'Secret Wonders'), ('Great Encounters', 'Great Encounters'), ('Majestic Dawn', 'Majestic Dawn'), ('Legends Awakened', 'Legends Awakened'), ('Stormfront', 'Stormfront'), ('Platinum Base Set', 'Platinum Base Set'), ('Rising Rivals', 'Rising Rivals'), ('Supreme Victors', 'Supreme Victors'), ('Arceus', 'Arceus'), ('HeartGold & SoulSilver Base Set', 'HeartGold & SoulSilver Base Set'), ('Unleashed', 'Unleashed'), ('Undaunted', 'Undaunted'), ('Triumphant', 'Triumphant'), ('Black & White Base Set', 'Black & White Base Set'), ('Emerging Powers', 'Emerging Powers'), ('Noble Victories', 'Noble Victories'), ('Next Destinies', 'Next Destinies'), ('Dark Explorers', 'Dark Explorers'), ('Dragons Exalted', 'Dragons Exalted'), ('Boundaries Crossed', 'Boundaries Crossed'), ('Plasma Storm', 'Plasma Storm'), ('Plasma Freeze', 'Plasma Freeze'), ('Plasma Blast', 'Plasma Blast'), ('Legendary Treasures', 'Legendary Treasures'), ('XY Base Set', 'XY Base Set'), ('Flashfire', 'Flashfire'), ('Furious Fists', 'Furious Fists'), ('Phantom Forces', 'Phantom Forces'), ('Primal Clash', 'Primal Clash'), ('Roaring Skies', 'Roaring Skies'), ('Ancient Origins', 'Ancient Origins'), ('BREAKthrough', 'BREAKthrough'), ('BREAKpoint', 'BREAKpoint'), ('Fates Collide', 'Fates Collide'), ('Steam Siege', 'Steam Siege'), ('Evolutions', 'Evolutions'), ('Sun & Moon Base Set', 'Sun & Moon Base Set'), ('Guardians Rising', 'Guardians Rising'), ('Burning Shadows', 'Burning Shadows'), ('Crimson Invasion', 'Crimson Invasion'), ('Ultra Prism', 'Ultra Prism'), ('Forbidden Light', 'Forbidden Light'), ('Celestial Storm', 'Celestial Storm'), ('Lost Thunder', 'Lost Thunder'), ('Team Up', 'Team Up'), ('Unbroken Bonds', 'Unbroken Bonds'), ('Unified Minds', 'Unified Minds'), ('Cosmic Eclipse', 'Cosmic Eclipse'), ('Sword & Shield Base Set', 'Sword & Shield Base Set'), ('Rebel Clash', 'Rebel Clash'), ('Darkness Ablaze', 'Darkness Ablaze'), ('Vivid Voltage', 'Vivid Voltage'), ('Battle Styles', 'Battle Styles'), ('Chilling Reign', 'Chilling Reign'), ('Evolving Skies', 'Evolving Skies'), ('Fusion Strike', 'Fusion Strike'), ('Brilliant Stars', 'Brilliant Stars'), ('Astral Radiance', 'Astral Radiance'), ('Lost Origin', 'Lost Origin'), ('Silver Tempest', 'Silver Tempest'), ('Scarlet & Violet Base Set', 'Scarlet & Violet Base Set'), ('Paldea Evolved', 'Paldea Evolved'), ('Obsidian Flames', 'Obsidian Flames'), ('Paradox Rift', 'Paradox Rift')], max_length=200),
        ),
    ]
