# Generated by Django 5.1.6 on 2025-02-10 19:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Constituency',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('constituency_id', models.AutoField(primary_key=True, serialize=False)),
                ('district', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('population', models.IntegerField(blank=True, null=True)),
                ('number_of_voters', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserCredentials',
            fields=[
                ('mobile', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('candidate_id', models.AutoField(primary_key=True, serialize=False)),
                ('political_party', models.CharField(max_length=100)),
                ('age', models.PositiveIntegerField()),
                ('manifesto', models.TextField(blank=True, null=True)),
                ('education', models.CharField(blank=True, max_length=100, null=True)),
                ('constituency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.constituency')),
                ('user_credentials', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Users.usercredentials')),
            ],
        ),
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('aadhar_number', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('verified', models.BooleanField(default=False)),
                ('age', models.PositiveIntegerField()),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10)),
                ('constituency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.constituency')),
                ('user_credentials', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Users.usercredentials')),
            ],
        ),
        migrations.CreateModel(
            name='VotingOfficer',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('voting_officer_id', models.AutoField(primary_key=True, serialize=False)),
                ('experience', models.PositiveIntegerField(blank=True, null=True)),
                ('designation', models.CharField(default='Voting Officer', max_length=100)),
                ('user_credentials', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Users.usercredentials')),
            ],
        ),
    ]
