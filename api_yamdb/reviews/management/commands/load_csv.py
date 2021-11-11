import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from reviews.models import Category, Comment, Genre, Review, Title, Genre_Title
from users.models import MyUser as User

MODEL_NAME_FILE = {
    'category': (Category, 'category.csv'),
    'comment': (Comment, 'comments.csv'),
    'genre': (Genre, 'genre.csv'),
    'genre_title': (Genre_Title, 'genre_title.csv'),
    'review': (Review, 'review.csv',),
    'title': (Title, 'titles.csv'),
    'user': (User, 'users.csv'),
}


class Command(BaseCommand):
    help = 'Load data from csv file to model'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='name of model')

    def get_csv_file(self, filename):
        return os.path.join(settings.BASE_DIR, 'static', 'data', filename)

    def clear_model(self, model_name):
        try:
            model_name.objects.all().delete()
        except Exception as e:
            raise CommandError(
                f'Error in clearing {model_name}: {str(e)}'
            )

    def print_to_terminal(self, message):
        self.stdout.write(self.style.SUCCESS(message))

    def load_data_to_db(self, model, csv_file, model_name):
        field_names = [f.name for f in model._meta.get_fields()]
        file_path = self.get_csv_file(csv_file)
        self.print_to_terminal(f'load file: {csv_file} to model: {model_name}')
        line = 0
        try:
            with open(file_path) as file:
                csv_reader = csv.reader(file, delimiter=',')
                self.clear_model(model)
                for row in csv_reader:
                    if row != '' and line > 0:
                        data = [row[i] for i in range(1, len(field_names))]
                        params = dict(zip(field_names[1:], data))
                        _, created = model.objects.get_or_create(**params)
                    line += 1
            self.print_to_terminal(
                f'{line - 1} objects added to {model_name.capitalize()} model'
            )
        except FileNotFoundError:
            raise CommandError(f'File {file_path} does not exist')

    def load_all_models(self):
        for model_name, (model, csv_file) in MODEL_NAME_FILE.items():
            self.load_data_to_db(model, csv_file, model_name)

    def handle(self, *args, **kwargs):
        model_name = kwargs.get('model_name').lower()
        if model_name == 'all':
            self.load_all_models()
        else:
            try:
                model, csv_file = MODEL_NAME_FILE[model_name]
            except KeyError as e:
                raise CommandError(f'Model {str(e)} does not exist')
            self.load_data_to_db(model, csv_file, model_name)
