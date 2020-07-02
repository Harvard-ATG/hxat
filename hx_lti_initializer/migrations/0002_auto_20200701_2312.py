# Generated by Django 2.2.10 on 2020-07-01 23:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hx_lti_initializer', '0001_initial'),
    ]

    operations = [
        # Create temp copy of the LTIResourceLinkConfig table and then truncate
        migrations.RunSQL(
            sql="""
            CREATE TABLE IF NOT EXISTS hx_lti_initializer_ltiresourcelinkconfig_20200701 
            AS SELECT * FROM hx_lti_initializer_ltiresourcelinkconfig;
            """
        ),
        migrations.RunSQL(
            sql="DELETE FROM hx_lti_initializer_ltiresourcelinkconfig;",
        ),
        # Replace collection_id and object_id fields with assignment_target.
        # The assignment_target represents a particular target object and assignment within a course.
        # This should ensure that deleting an assignment or the combination of assignment and target
        # will cascade as expected.
        migrations.RemoveField(
            model_name='ltiresourcelinkconfig',
            name='collection_id',
        ),
        migrations.RemoveField(
            model_name='ltiresourcelinkconfig',
            name='object_id',
        ),
        migrations.AddField(
            model_name='ltiresourcelinkconfig',
            name='assignment_target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hx_lti_assignment.AssignmentTargets'),
        ),
        # Set uniqueness constraint on resource_link_id
        migrations.AlterField(
            model_name='ltiresourcelinkconfig',
            name='resource_link_id',
            field=models.CharField(max_length=255, unique=True),
        ),
        # Re-populate the LTIResourceLinkConfig table, but this time with the Assignment PKs
        # Note that this query is more complicated than it should be because it has to handle the case
        # where a target object is duplicated within an assignment/collection (e.g. Lorem Ipsum repeated twice).
        # Since that's an edge case for this migration, we're just going to pick one, otherwise we'll get
        # a primary key violation. 
        migrations.RunSQL(
            sql="""
            INSERT INTO hx_lti_initializer_ltiresourcelinkconfig (id, resource_link_id, assignment_target_id)
            SELECT id, resource_link_id, MAX(assignment_target_id)
            FROM (
                    SELECT
                            c.id AS id,
                            c.resource_link_id AS resource_link_id,
                            at.id AS assignment_target_id
                    FROM hx_lti_initializer_ltiresourcelinkconfig_20200701 c
                            JOIN hx_lti_assignment_assignment a ON (c.collection_id = a.assignment_id)
                            JOIN hx_lti_assignment_assignmenttargets at
                                ON (a.id = at.assignment_id AND at.target_object_id = c.object_id::INTEGER)

                    ORDER BY c.id, c.resource_link_id, at.id
            ) x
            GROUP BY id, resource_link_id;
            """
        ),
    ]
