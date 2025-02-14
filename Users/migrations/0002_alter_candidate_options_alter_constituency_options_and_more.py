# Generated by Django 5.1.6 on 2025-02-10 19:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='candidate',
            options={'verbose_name': 'Candidate', 'verbose_name_plural': 'Candidates'},
        ),
        migrations.AlterModelOptions(
            name='constituency',
            options={'verbose_name': 'Constituency', 'verbose_name_plural': 'Constituencies'},
        ),
        migrations.AlterModelOptions(
            name='usercredentials',
            options={'verbose_name': 'UserCredential', 'verbose_name_plural': 'UserCredentials'},
        ),
        migrations.AlterModelOptions(
            name='voter',
            options={'verbose_name': 'Voter', 'verbose_name_plural': 'Voters'},
        ),
        migrations.AlterModelOptions(
            name='votingofficer',
            options={'verbose_name': 'VotingOfficer', 'verbose_name_plural': 'VotingOfficers'},
        ),
    ]
