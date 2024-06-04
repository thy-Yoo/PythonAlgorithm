import cx_Oracle, threading

class DbConnector:
    _instance = None
    _lock = threading.Lock()

    _client_path = "D:/내오라클드라이버경로/intantclient_21_9"
    _host = "내IP주소"
    _port = "내port번호"
    _sid = "MYDBNAME"
    _user = "MYID"
    _password = "MYPW"
    _dsn = cx_Oracle.makedsn(_host, _port, _sid)

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(DbConnector, cls).__new__(cls, *args, **kwargs)
                    cls._instance._init_db(*args, **kwargs)
                return cls._instance

    def _init_db(self):
        cx_Oracle.init_oracle_client(lib_dir=self._client_path)
        self.connection = cx_Oracle.connect(user=self._user, password=self._password, dsn=self._dsn)

    def get_connection(self):
        return self.connection