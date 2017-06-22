from database_services.database_writer import DatabaseWriter
from inventory import VIDEO_TABLE_NAME

class VideoWriter(DatabaseWriter):
    def __init__(self):
        DatabaseWriter.__init__(self)
        self._table = VIDEO_TABLE_NAME

    def write_video_to_db(self, datetime_obj, file_path, session_id, camera_idx):
        t = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
        statement = 'INSERT INTO %s (task_time, file_path, session_id, camera_idx) VALUES ("%s", "%s", %s, %s)' % \
                    (self._table, t, file_path, session_id, camera_idx)
        self.execute(statement)

    def get_all_tasks(self, is_complete):
        statement = 'SELECT * FROM %s where complete = %s ORDER BY task_time' % (self._table, is_complete)
        c = self.make_connection()
        with c.cursor() as cursor:
            cursor.execute(statement)
            res = cursor.fetchall()
        c.close()
        return res

    def get_all_tasks_by_session(self, is_complete, session_id):
        statement = 'SELECT * FROM % s where complete = %s and session_id = %s' % (self._table, is_complete, session_id)
        c = self.make_connection()
        with c.cursor() as cursor:
            cursor.execute(statement)
            res = cursor.fetchall()
        c.close()
        return res

    def set_complete(self, file_path):
        statement = 'UPDATE %s SET complete = 1 where file_path = "%s"' % (self._table, file_path)
        self.execute(statement)

    def clear_finished_task(self, f):
        statement = 'DELETE FROM %s where complete = 1 and file_path = "%s"' % (self._table, f)
        self.execute(statement)