import os

for root, dirs, files in os.walk('.'):
    if 'migrations' in dirs:
        migrations_path = os.path.join(root, 'migrations')
        for file in os.listdir(migrations_path):
            if file != '__init__.py' and file.endswith('.py'):
                os.remove(os.path.join(migrations_path, file))
            if file.endswith('.pyc'):
                os.remove(os.path.join(migrations_path, file))
