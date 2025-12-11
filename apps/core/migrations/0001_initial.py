# Generated migration for Core app

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user account should be considered active. Uncheck this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('role', models.CharField(choices=[('admin', 'Administrador'), ('coordenador', 'Coordenador'), ('professor', 'Professor'), ('aluno', 'Aluno'), ('responsavel', 'Responsável')], default='aluno', max_length=20, verbose_name='Papel')),
                ('bio', models.TextField(blank=True, verbose_name='Biografia')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/', verbose_name='Avatar')),
                ('phone', models.CharField(blank=True, max_length=20, verbose_name='Telefone')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuário',
                'verbose_name_plural': 'Usuários',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('create', 'Criação'), ('update', 'Atualização'), ('delete', 'Exclusão'), ('view', 'Visualização')], max_length=20, verbose_name='Ação')),
                ('model_name', models.CharField(max_length=100, verbose_name='Nome do Modelo')),
                ('object_id', models.IntegerField(verbose_name='ID do Objeto')),
                ('changes', models.JSONField(blank=True, default=dict, verbose_name='Mudanças')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='Endereço IP')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Timestamp')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='audit_logs', to='core.user', verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Log de Auditoria',
                'verbose_name_plural': 'Logs de Auditoria',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Título')),
                ('message', models.TextField(verbose_name='Mensagem')),
                ('priority', models.CharField(choices=[('low', 'Baixa'), ('medium', 'Média'), ('high', 'Alta'), ('urgent', 'Urgente')], default='medium', max_length=20, verbose_name='Prioridade')),
                ('status', models.CharField(choices=[('unread', 'Não Lida'), ('read', 'Lida'), ('archived', 'Arquivada')], default='unread', max_length=20, verbose_name='Status')),
                ('link', models.URLField(blank=True, verbose_name='Link')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('read_at', models.DateTimeField(blank=True, null=True, verbose_name='Lido em')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='core.user', verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Notificação',
                'verbose_name_plural': 'Notificações',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='auditlog',
            index=models.Index(fields=['user', '-timestamp'], name='core_auditl_user_id_timestamp_idx'),
        ),
        migrations.AddIndex(
            model_name='auditlog',
            index=models.Index(fields=['model_name', 'object_id'], name='core_auditl_model_name_object_id_idx'),
        ),
        migrations.AddIndex(
            model_name='notification',
            index=models.Index(fields=['user', '-created_at'], name='core_notifi_user_id_created_at_idx'),
        ),
        migrations.AddIndex(
            model_name='notification',
            index=models.Index(fields=['user', 'status'], name='core_notifi_user_id_status_idx'),
        ),
    ]
