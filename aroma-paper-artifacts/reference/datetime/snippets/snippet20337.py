from contextlib import contextmanager
from datetime import datetime
import difflib
import os
import tempfile
import click
import sqlparse
from agnostic import create_backend, Migration, MigrationStatus


@click.command('list')
@pass_config
def list_(config):
    '\n    List migrations.\n\n    This shows migration metadata: migrations that have been applied (and the\n    result of that application) and migrations that are pending.\n\n        * bootstrapped: a migration that was inserted during the bootstrap\n          process.\n        * failed: the migration did not apply cleanly; the migrations system\n          will not be able to operate until this is rectified, typically by\n          restoring from a backup.\n        * pending: the migration has not been applied yet.\n        * succeeded: the migration applied cleanly.\n\n    Applied migrations are ordered by the "started_at" timestamp. Pending\n    migrations follow applied migrations and are sorted in the same order that\n    they would be applied.\n    '
    with _get_db_cursor(config) as (db, cursor):
        try:
            (applied, pending) = _get_all_migrations(config, cursor)
            migrations = (applied + pending)
            if (len(migrations) == 0):
                raise click.ClickException('No migrations exist.')
            column_names = ('Name', 'Status', 'Started At', 'Completed At')
            max_name = max([len(m.name) for m in migrations])
            max_status = max([len(m.status.name) for m in migrations])
            row_format = '{{:<{}}} | {{:{}}} | {{:<19}} | {{:<19}}'
            name_col_width = max(max_name, len(column_names[1]))
            status_col_width = max(max_status, len(column_names[2]))
            row = row_format.format(name_col_width, status_col_width)
            date_format = '%Y-%m-%d %H:%I:%S'
            click.echo(row.format(*column_names))
            click.echo(((((((('-' * (name_col_width + 1)) + '+') + ('-' * (status_col_width + 2))) + '+') + ('-' * 21)) + '+') + ('-' * 20)))
            for migration in migrations:
                if (migration.started_at is None):
                    started_at = 'N/A'
                else:
                    started_at = migration.started_at.strftime(date_format)
                if (migration.completed_at is None):
                    completed_at = 'N/A'
                elif isinstance(migration.completed_at, datetime):
                    completed_at = migration.completed_at.strftime(date_format)
                msg = row.format(migration.name, migration.status.name, started_at, completed_at)
                if (migration.status == MigrationStatus.bootstrapped):
                    click.echo(msg)
                elif (migration.status == MigrationStatus.failed):
                    click.secho(msg, fg='red')
                elif (migration.status == MigrationStatus.pending):
                    click.echo(msg)
                elif (migration.status == MigrationStatus.succeeded):
                    click.secho(msg, fg='green')
                else:
                    msg = 'Invalid migration status: "{}".'
                    raise ValueError(msg.format(migration.status.name))
        except Exception as e:
            if config.debug:
                raise
            msg = 'Cannot list migrations: {}'
            raise click.ClickException(msg.format(e))
