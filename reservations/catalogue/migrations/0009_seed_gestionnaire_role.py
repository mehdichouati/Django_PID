from django.db import migrations

def create_gestionnaire_role(apps, schema_editor):
    Role = apps.get_model('catalogue', 'Role')
    Role.objects.get_or_create(role='gestionnaire')

def remove_gestionnaire_role(apps, schema_editor):
    Role = apps.get_model('catalogue', 'Role')
    Role.objects.filter(role='gestionnaire').delete()

class Migration(migrations.Migration):
    dependencies = [
        ('catalogue', '0008_usermeta_affiliate_level'),
    ]
    operations = [
        migrations.RunPython(create_gestionnaire_role, remove_gestionnaire_role),
    ]