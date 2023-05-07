from io import StringIO
import glob
import grt
import mforms
import datetime
from wb import DefineModule, wbinputs
from workbench.ui import WizardForm, WizardPage
from mforms import newButton, newCodeEditor, FileChooser


@ModuleInfo.plugin('wb.util.generate_laravel5_migration', caption='Export Laravel 5 Migration', input=[wbinputs.currentCatalog()], groups=['Catalog/Utilities', 'Menu/Catalog'], pluginMenu='Catalog')
@ModuleInfo.export(grt.INT, grt.classes.db_Catalog)
def generate_laravel5_migration(catalog):

    def create_tree(table_schema):
        tree = {}
        for tbl in sorted(table_schema.tables, key=(lambda table: table.name)):
            table_references = []
            for key in tbl.foreignKeys:
                if ((key.name != '') and hasattr(key, 'referencedColumns') and (len(key.referencedColumns) > 0) and (tbl.name != key.referencedColumns[0].owner.name)):
                    table_references.append(key.referencedColumns[0].owner.name)
            tree[tbl.name] = table_references
        d = dict(((k, set(tree[k])) for k in tree))
        r = []
        while d:
            t = (set((i for v in d.values() for i in v)) - set(d.keys()))
            t.update((k for (k, v) in d.items() if (not v)))
            r.append(t)
            d = dict(((k, (v - t)) for (k, v) in d.items() if v))
        return r

    def addslashes(s):
        replaces = ['\\', "'", '\x00']
        for i in replaces:
            if (i in s):
                s = s.replace(i, ('\\' + i))
        return s

    def export_schema(table_schema, tree):
        if (len(table_schema.tables) == 0):
            return
        foreign_keys = {}
        global migration_tables
        global migrations
        tables = sorted(table_schema.tables, key=(lambda table: table.name))
        ti = 0
        migrations = {}
        migration_tables = []
        for reference_tables in tree:
            for reference in reference_tables:
                for tbl in tables:
                    if (tbl.name != reference):
                        continue
                    table_name = tbl.name
                    table_engine = tbl.tableEngine
                    components = table_name.split('_')
                    migration_tables.append(table_name)
                    migrations[ti] = []
                    migrations[ti].append(migrationTemplate.format(tableNameCamelCase=''.join((x.title() for x in components[0:])), tableName=table_name))
                    migrations[ti].append("{}$table->engine = '{}';\n".format((' ' * 12), table_engine))
                    created_at = created_at_nullable = updated_at = updated_at_nullable = deleted_at = timestamps = timestamps_nullable = False
                    for col in tbl.columns:
                        if (col.name == 'created_at'):
                            created_at = True
                            if (col.isNotNull != 1):
                                created_at_nullable = True
                        elif (col.name == 'updated_at'):
                            updated_at = True
                            if (col.isNotNull != 1):
                                updated_at_nullable = True
                    if ((created_at is True) and (updated_at is True) and (created_at_nullable is True)):
                        if (updated_at_nullable is True):
                            timestamps_nullable = True
                        elif ((created_at is True) and (updated_at is True)):
                            timestamps = True
                    elif ((created_at is True) and (updated_at is True)):
                        timestamps = True
                    primary_key = [col for col in tbl.indices if (col.isPrimary == 1)]
                    primary_key = (primary_key[0] if (len(primary_key) > 0) else None)
                    if hasattr(primary_key, 'columns'):
                        primary_col = primary_key.columns[0].referencedColumn
                    else:
                        primary_col = None
                    default_time_values = ['CURRENT_TIMESTAMP', 'NULL ON UPDATE CURRENT_TIMESTAMP', 'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP']
                    for col in tbl.columns:
                        try:
                            if (((col.name == 'created_at') or (col.name == 'updated_at')) and ((timestamps is True) or (timestamps_nullable is True))):
                                continue
                            if (col.name == 'deleted_at'):
                                deleted_at = True
                                continue
                            if col.simpleType:
                                col_type = col.simpleType.name
                            else:
                                col_type = col.userType.name
                            if (col == primary_col):
                                if (col_type == 'BIGINT'):
                                    col_type = 'BIG_INCREMENTS'
                                elif (col_type == 'MEDIUMINT'):
                                    col_type = 'MEDIUM_INCREMENTS'
                                elif (col_type == 'VARCHAR'):
                                    col_type = 'VARCHAR'
                                elif ((col_type == 'CHAR') and (col.length == 36)):
                                    col_type = 'UUID'
                                else:
                                    col_type = 'INCREMENTS'
                            if (((col_type == 'BIGINT') or (col_type == 'INT') or (col_type == 'TINYINT') or (col_type == 'MEDIUMINT') or (col_type == 'SMALLINT')) and ('UNSIGNED' in col.flags)):
                                col_type = ('u' + col_type)
                            col_data = "'"
                            if (col_type not in typesDict):
                                continue
                            if (typesDict[col_type] == 'char'):
                                if (col.length > (- 1)):
                                    col_data = ("', %s" % str(col.length))
                            elif (typesDict[col_type] == 'decimal'):
                                if ((col.precision > (- 1)) and (col.scale > (- 1))):
                                    col_data = ("', %s, %s" % (str(col.precision), str(col.scale)))
                            elif (typesDict[col_type] == 'double'):
                                if ((col.precision > (- 1)) and (col.length > (- 1))):
                                    col_data = ("', %s, %s" % (str(col.length), str(col.precision)))
                            elif (typesDict[col_type] == 'enum'):
                                col_data = ("', [%s]" % col.datatypeExplicitParams[1:(- 1)])
                            elif (typesDict[col_type] == 'string'):
                                if ((- 1) < col.length < 255):
                                    col_data = ("', %s" % str(col.length))
                                else:
                                    col_data = "'"
                            if ((col.name == 'remember_token') and (typesDict[col_type] == 'string') and (str(col.length) == '100')):
                                migrations[ti].append('{}$table->rememberToken();\n'.format((' ' * 12)))
                            elif typesDict[col_type]:
                                migrations[ti].append("{}$table->{}('{}{})".format((' ' * 12), typesDict[col_type], col.name, col_data))
                                if ((typesDict[col_type] == 'integer') and ('UNSIGNED' in col.flags)):
                                    migrations[ti].append('->unsigned()')
                                if ((col == primary_col) and (typesDict[col_type] == 'string')):
                                    migrations[ti].append('->primary()')
                                if ((col.isNotNull != 1) and (col != primary_col)):
                                    migrations[ti].append('->nullable()')
                                if ((col.defaultValue != '') and (col.defaultValueIsNull != 0)):
                                    migrations[ti].append('->default(null)')
                                elif (col.defaultValue != ''):
                                    default_value = col.defaultValue.replace("'", '')
                                    if (default_value in default_time_values):
                                        migrations[ti].append("->default(DB::raw('{}'))".format(default_value))
                                    else:
                                        migrations[ti].append("->default('{}')".format(default_value))
                                if (col.comment != ''):
                                    migrations[ti].append("->comment('{}')".format(addslashes(col.comment)))
                                migrations[ti].append(';\n')
                            if ((col.name == 'id') and (typesDict[col_type] == 'uuid')):
                                migrations[ti].append("{}$table->primary('id');\n".format((' ' * 12)))
                        except AttributeError:
                            pass
                    indexes = {'primary': {}, 'unique': {}, 'index': {}}
                    for index in tbl.indices:
                        index_type = index.indexType.lower()
                        if (index_type == 'primary'):
                            continue
                        index_name = index.name
                        indexes[index_type][index_name] = []
                        for column in index.columns:
                            indexes[index_type][index_name].append(column.referencedColumn.name)
                    for index_type in indexes:
                        for index_name in indexes[index_type]:
                            if (len(indexes[index_type][index_name]) != 0):
                                index_key_template = indexKeyTemplate.format(indexType=index_type, indexColumns=', '.join(['"{}"'.format(column_name) for column_name in indexes[index_type][index_name]]), indexName=index_name)
                                migrations[ti].append(index_key_template)
                    if (deleted_at is True):
                        migrations[ti].append('{}$table->softDeletes();\n'.format((' ' * 12)))
                    if (timestamps is True):
                        migrations[ti].append('{}$table->timestamps();\n'.format((' ' * 12)))
                    elif (timestamps_nullable is True):
                        migrations[ti].append('{}$table->nullableTimestamps();\n'.format((' ' * 12)))
                    first_foreign_created = False
                    for key in tbl.foreignKeys:
                        if ((key.name != '') and hasattr(key.index, 'name')):
                            index_name = key.index.name
                            foreign_key = key.columns[0].name
                            if (index_name == 'PRIMARY'):
                                index_name = ((tbl.name + '_') + key.columns[0].name)
                            if (key.referencedColumns[0].owner.name in migration_tables):
                                if (not first_foreign_created):
                                    migrations[ti].append('\n')
                                    first_foreign_created = True
                                delete_rule = key.deleteRule
                                if (delete_rule == ''):
                                    delete_rule = 'RESTRICT'
                                update_rule = key.updateRule
                                if (update_rule == ''):
                                    update_rule = 'RESTRICT'
                                migrations[ti].append(foreignKeyTemplate.format(foreignKey=foreign_key, foreignKeyName=index_name, tableKeyName=key.referencedColumns[0].name, foreignTableName=key.referencedColumns[0].owner.name, onDeleteAction=delete_rule.lower(), onUpdateAction=update_rule.lower()))
                            else:
                                if (key.referencedColumns[0].owner.name not in foreign_keys):
                                    foreign_keys[key.referencedColumns[0].owner.name] = []
                                foreign_keys[key.referencedColumns[0].owner.name].append({'table': key.columns[0].owner.name, 'key': foreign_key, 'name': index_name, 'referenced_table': key.referencedColumns[0].owner.name, 'referenced_name': key.referencedColumns[0].name, 'update_rule': key.updateRule, 'delete_rule': key.deleteRule})
                    migrations[ti].append('{}}});\n'.format((' ' * 8)))
                    for (key, val) in foreign_keys.items():
                        if (key == tbl.name):
                            keyed_tables = []
                            schema_table = 0
                            for item in val:
                                if (item['table'] not in keyed_tables):
                                    keyed_tables.append(item['table'])
                                    foreign_table_name = item['table']
                                    if (schema_table == 0):
                                        migrations[ti].append('\n')
                                        migrations[ti].append(schemaCreateTemplate.format(tableName=item['table']))
                                        schema_table = 1
                                    elif (foreign_table_name != item['table']):
                                        migrations[ti].append('{}});\n'.format((' ' * 12)))
                                        migrations[ti].append('\n')
                                        migrations[ti].append(schemaCreateTemplate.format(tableName=item['table']))
                                    migrations[ti].append(foreignKeyTemplate.format(foreignKey=item['key'], foreignKeyName=item['name'], tableKeyName=item['referenced_name'], foreignTableName=item['referenced_table'], onDeleteAction=item['delete_rule'].lower(), onUpdateAction=item['update_rule'].lower()))
                            if (schema_table == 1):
                                migrations[ti].append('{}}});\n'.format((' ' * 12)))
                    migrations[ti].append('    }\n')
                    migrations[ti].append(migrationDownTemplate)
                    migrations[ti].append(migrationEndingTemplate.format(tableName=table_name))
                    ti += 1
        return migrations
    out = StringIO()
    try:
        for schema in [(s, (s.name == 'main')) for s in catalog.schemata]:
            table_tree = create_tree(schema[0])
            migrations = export_schema(schema[0], table_tree)
    except GenerateLaravel5MigrationError as e:
        grt.modules.Workbench.confirm(e.typ, e.message)
        return 1
    now = datetime.datetime.now()
    for name in sorted(migrations):
        save_format = '{year}_{month}_{day}_{number}_create_{tableName}_table.php'.format(year=now.strftime('%Y'), month=now.strftime('%m'), day=now.strftime('%d'), number=''.zfill(6), tableName=migration_tables[name])
        out.write('Table name: {0}  Migration File: {1}\n\n'.format(migration_tables[name], save_format))
        out.write(''.join(migrations[name]))
        out.write('\n\n\n'.format(name))
    sql_text = out.getvalue()
    out.close()
    wizard = GenerateLaravel5MigrationWizard(sql_text)
    wizard.run()
    return 0
