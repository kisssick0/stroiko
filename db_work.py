from DBcm import UseDatabase


def work_with_db(dbconfig: dict, _sql: str):
    schema = []
    result = {}
    with UseDatabase(dbconfig) as cursor:

        if cursor is None:
            raise ValueError('Курсор не создан')

        cursor.execute(_sql)
        schema = [column[0] for column in cursor.description]
        result = cursor.fetchall()
    return result, schema


def call_proc(dbconfig: dict, proc_name: str, *args):
    with UseDatabase(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('Курсор не курсор')
        param_list = []
        for arg in args:
            print('args=', arg)
            param_list.append(arg)
        print('param_list', param_list)
        print('proc_name = ', proc_name)
        res = cursor.callproc(proc_name, param_list)
    return res


