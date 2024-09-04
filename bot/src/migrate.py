from yoyo import get_backend, read_migrations

from bot import settings


def migrate():
	backend = get_backend(
		f'postgresql://'
		f'{settings.DB_USER}:'
		f'{settings.DB_PASSWORD}@'
		f'{settings.DB_HOST}:'
		f'{settings.DB_PORT}/'
		f'{settings.DB_NAME}'
	)
	migrations = read_migrations('./migrations/')

	with backend.lock():
		# Apply any outstanding migrations
		backend.apply_migrations(backend.to_apply(migrations))


if __name__ == '__main__':
	migrate()
