# database_setup.py (修改后的版本)

import configparser
import urllib.parse
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import OperationalError

# --- 从配置文件读取设置 ---
config = configparser.ConfigParser()
config.read('config.ini') # 读取同目录下的config.ini文件

db_user = config.get('database', 'user')
raw_password = config.get('database', 'password')
db_password = urllib.parse.quote_plus(raw_password)
db_host = config.get('database', 'host')
db_port = config.get('database', 'port')
db_name = config.get('database', 'db_name')

engine = None # 初始化为 None
warning_table_name = "early_warning_information" # 预警表名
prediction_table_name = "risk_prediction_results_ysy" # 预测结果表名

def connect_to_db():
    """
    Establishes and tests the database connection.
    Returns the engine object if successful, otherwise prints an error and exits.
    """
    global engine # Declare engine as global to modify the global variable
    try:
        # 使用编码后的 db_password
        engine_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        engine = create_engine(engine_url)
        # 测试连接
        with engine.connect() as connection:
            print("✅ 数据库连接成功!")
            # 检查表是否存在
            inspector = inspect(engine)
            if not inspector.has_table(warning_table_name):
                print(f"⚠️ '{warning_table_name}' 表不存在。请先创建该表。")
                # Consider how to handle this: raise an error, or return a specific status
            else:
                print(f"✅ '{warning_table_name}' 表存在。")

            if not inspector.has_table(prediction_table_name):
                print(f"⚠️ '{prediction_table_name}' 表不存在。请先创建该表。")
                # Consider how to handle this
            else:
                print(f"✅ '{prediction_table_name}' 表存在。")
        return engine

    except OperationalError as e:
        print(f"❌ 数据库连接失败或数据库不存在: {e}")
        engine = None # Ensure engine is None on failure
        # exit() # Avoid exiting directly in a module, let the calling script decide
        return None
    except Exception as e:
        print(f"❌ 数据库连接时发生未知错误: {e}")
        engine = None # Ensure engine is None on failure
        # exit()
        return None

# --- Main execution block (optional, for testing this script directly) ---
if __name__ == "__main__":
    print("Attempting to connect to the database...")
    db_engine = connect_to_db()
    if db_engine:
        print("Database engine initialized successfully and tables checked.")
    else:
        print("Failed to initialize database engine.")
    # You could add more direct tests here if needed, e.g., fetching a small piece of data.
    # Note: pandas options and unused imports like datetime, numpy, IPython.display
    # are commented out or removed if not directly used by the connection logic itself.
    # If other parts of your application that will import this module need them,
    # they should be in those respective files or a shared utility file.