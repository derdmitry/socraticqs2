# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ct', '0014_fsmgroup'),
        ('lti', '0002_auto_20150429_0310'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseRef',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'Creation date and time')),
                ('context_id', models.CharField(max_length=254, verbose_name=b'LTI context_id')),
                ('tc_guid', models.CharField(max_length=128, verbose_name=b'LTI tool_consumer_instance_guid')),
                ('course', models.OneToOneField(verbose_name=b'Courslet Course', to='ct.Course')),
                ('instructors', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name=b'Course Instructors')),
                ('parent', models.ForeignKey(verbose_name=b'Previous generation of Course', blank=True, to='lti.CourseRef', null=True)),
            ],
            options={
                'verbose_name': 'CourseRef',
                'verbose_name_plural': 'CourseRefs',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='courseref',
            unique_together=set([('context_id', 'course')]),
        ),
    ]
