# Generated by Django 2.0.6 on 2018-07-21 00:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.EmailField(max_length=254)),
                ('created_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_at', models.DateTimeField(default=None, null=True)),
                ('status', models.CharField(choices=[('Draft', 'Draft'), ('Online', 'Online'), ('Started', 'Started'), ('Completed', 'Completed')], max_length=20)),
                ('hash_str', models.CharField(db_index=True, max_length=64)),
                ('created_at', models.DateTimeField()),
                ('duration', models.IntegerField()),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myservices.Candidate')),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('difficulty', models.CharField(max_length=20)),
                ('problem_name', models.CharField(max_length=20)),
                ('problem_path', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submit_id', models.IntegerField(default=None, null=True)),
                ('result', models.CharField(default=None, max_length=20, null=True)),
                ('submit_at', models.DateTimeField()),
                ('interview', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myservices.Interview')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myservices.Problem')),
            ],
        ),
        migrations.AddField(
            model_name='interview',
            name='problems',
            field=models.ManyToManyField(to='myservices.Problem'),
        ),
    ]
