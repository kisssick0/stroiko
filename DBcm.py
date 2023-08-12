from pymysql import connect
from pymysql.err import OperationalError


class UseDatabase:

    def __init__(self, config: dict):
        self.config = config

    def __enter__(self):
        try:
            self.conn = connect(**self.config)
            self.cursor = self.conn.cursor()
            return self.cursor
        except OperationalError as err:
            if err.args[0] == 1045:
                print('Проверьте логин / пароль')
            elif err.args[0] == 1049:
                print('Проверьте имя базы данных')
            else:
                print(err)
            return None

    def __exit__(self, exc_type, exc_val, exc_tr):
        if exc_val:
            print(exc_val)
            print(exc_type)
            if exc_val.args[0] != 'Курсор не создан':
                self.cursor.close()
                self.conn.commit()
                self.conn.close()
        else:

            self.cursor.close()
            self.conn.commit()
            self.conn.close()
        return True

