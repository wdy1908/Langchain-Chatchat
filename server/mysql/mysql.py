from sqlalchemy import create_engine
from configs import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT

def connect_sql():
    # from sqlalchemy import create_engine
    # from sshtunnel import SSHTunnelForwarder
    # SSH_HOST = '211.86.155.133'
    # SSH_PORT = 22
    # SSH_USER = 'vana'
    # SSH_PASSWORD = 'vanapwd2022'



    # # 创建 SSHTunnelForwarder 实例并启动
    # server = SSHTunnelForwarder(
    #     (SSH_HOST, SSH_PORT),
    #     ssh_username=SSH_USER,
    #     ssh_password=SSH_PASSWORD,
    #     remote_bind_address=(DB_HOST, 9030)
    # )
    # server.start()

    # engine = create_engine(
    #     f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@localhost:{server.bind_port}/{DB_NAME}",
    #     echo=True,
    # )
    engine = create_engine(
            f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4",
            echo=False,
        )
    return engine.connect()