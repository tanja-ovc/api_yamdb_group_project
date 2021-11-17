import csv
import os
import sqlite3

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

MODEL_DATA = {
    'user': ('users_myuser',
             'id, username, email, role, bio, first_name, last_name',
             'users.csv'),
    'category': ('reviews_category', 'id, name, slug', 'category.csv'),
    'genre': ('reviews_genre', 'id, name, slug', 'genre.csv'),
    'title': ('reviews_title', 'id, name, year, category_id', 'titles.csv'),
    'genre_title': ('reviews_title_genre', 'id, title_id, genre_id',
                    'genre_title.csv'),
    'review': ('reviews_review',
               'id, title_id, text, author_id, score, pub_date',
               'review.csv',),
    'comment': ('reviews_comment', 'id, review_id, text, author_id, pub_date',
                'comments.csv'),
}


def get_csv_file(filename):
    return os.path.join(settings.BASE_DIR, 'static', 'data', filename)


def get_db_file():
    return os.path.join(settings.BASE_DIR, 'db.sqlite3')


class Command(BaseCommand):
    help = 'Load data from csv file to model'

    def __init__(self, *args, **kwargs):
        self.conn = sqlite3.connect(get_db_file())
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='name of model')

    def print_to_terminal(self, message):
        self.stdout.write(self.style.SUCCESS(message))

    def execute_query(self, query, params=()):
        self.conn.cursor().execute(query, params)
        self.conn.commit()

    def clear_table(self, table_name):
        self.execute_query(f'DELETE FROM {table_name};')
        self.print_to_terminal(f'Delete data from {table_name} table')

    def insert_to_db(self, table_name, fields, values):
        placeholders = ', '.join('?' * len(values))
        sql = f'INSERT INTO {table_name} ({fields}) VALUES ({placeholders})'
        self.execute_query(sql, values)

    def load_data_to_db(self, table_name, fields, csv_file):
        file_path = get_csv_file(csv_file)
        self.print_to_terminal(f'load file: {csv_file} to table: {table_name}')
        line = 0
        try:
            with open(file_path) as file:
                csv_reader = csv.reader(file, delimiter=',')
                self.clear_table(table_name)
                for row in csv_reader:
                    if row != '' and line > 0:
                        self.insert_to_db(table_name, fields, row)
                    line += 1
            self.print_to_terminal(
                f'{line - 1} objects added to {table_name} table'
            )
        except FileNotFoundError:
            raise CommandError(f'File {file_path} does not exist')

    def load_all_models(self):
        for model_name, (table_name, fields, csv_file) in MODEL_DATA.items():
            self.load_data_to_db(table_name, fields, csv_file)

    def handle(self, *args, **kwargs):
        model_name = kwargs.get('model_name').lower()
        if model_name == 'all':
            self.load_all_models()
        else:
            try:
                table_name, fields, csv_file = MODEL_DATA[model_name]
            except KeyError as e:
                raise CommandError(f'Model {str(e)} does not exist')
            self.load_data_to_db(table_name, fields, csv_file)
