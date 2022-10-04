import os
import csv
import sqlite3

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'db.sqlite3')
files_folder = os.path.join(base_dir, 'static', 'data')


def load_category(cursor, dictionary_reader):
    to_db = (
        [(row['id'], row['name'], row['slug'])
            for row in dictionary_reader]
    )
    cursor.execute('DELETE FROM reviews_category;')
    cursor.executemany(
        'INSERT INTO reviews_category (id, name, slug) VALUES (?, ?, ?);',
        to_db
    )


def load_users(cursor, dictionary_reader):
    to_db = ([
        (r['id'], r['username'], r['email'], r['role'], r['bio'],
            r['first_name'], r['last_name']) for r in dictionary_reader
    ])
    cursor.execute('DELETE FROM reviews_customuser;')
    cursor.executemany(
        '''INSERT INTO reviews_customuser (
            id, username, email, role,
            bio, first_name, last_name
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);''',
        to_db
    )


def load_genre(cursor, dictionary_reader):
    to_db = (
        [
            (row['id'], row['name'], row['slug'])
            for row in dictionary_reader
        ]
    )
    cursor.execute('DELETE FROM reviews_genre;')
    cursor.executemany(
        'INSERT INTO reviews_genre (id, name, slug) VALUES (?, ?, ?);',
        to_db
    )


def load_titles(cursor, dictionary_reader):
    to_db = (
        [(row['id'], row['name'], row['year'], row['category'])
            for row in dictionary_reader]
    )
    cursor.execute('DELETE FROM reviews_title;')
    cursor.executemany(
        '''INSERT INTO reviews_title (id, name, year, category_id)
        VALUES (?, ?, ?, ?);''',
        to_db
    )


def load_genre_titles(cursor, dictionary_reader):
    to_db = (
        [(row['id'], row['title_id'], row['genre_id'])
            for row in dictionary_reader]
    )
    cursor.execute('DELETE FROM reviews_genretitle;')
    cursor.executemany(
        '''INSERT INTO reviews_genretitle (id, title_id, genre_id)
            VALUES (?, ?, ?);''',
        to_db
    )


def load_reviews(cursor, dictionary_reader):
    to_db = (
        [(row['id'], row['title_id'], row['text'], row['author'],
            row['score'], row['pub_date'])
            for row in dictionary_reader]
    )
    cursor.execute('DELETE FROM reviews_review;')
    cursor.executemany(
        '''INSERT INTO reviews_review
        (id, title_id, text, author_id, score, pub_date)
        VALUES (?, ?, ?, ?, ?, ?);''',
        to_db
    )


def load_comments(cursor, dictionary_reader):
    to_db = (
        [(row['id'], row['review_id'], row['text'], row['author'],
            row['pub_date'])
            for row in dictionary_reader]
    )
    cursor.execute('DELETE FROM reviews_comment;')
    cursor.executemany(
        '''INSERT INTO reviews_comment
        (id, review_id, text, author_id, pub_date)
        VALUES (?, ?, ?, ?, ?);''',
        to_db
    )


FILES = {
    'users': load_users,
    'category': load_category,
    'genre': load_genre,
    'titles': load_titles,
    'genre_title': load_genre_titles,
    'review': load_reviews,
    'comments': load_comments,
}


if __name__ == '__main__':
    print('connect to db:', db_path)
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    for file, loader in FILES.items():
        file_path = os.path.join(files_folder, file + '.csv')
        with open(file_path, 'r', encoding='utf8') as f:
            print('loading from file: {} ...'.format(file))
            dr = csv.DictReader(f, delimiter=',')
            loader(cursor, dr)
            connection.commit()
            print('success!')
            print('')

    connection.close()
