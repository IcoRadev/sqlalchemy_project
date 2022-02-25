import functools


@functools.lru_cache()
def get_configuration():
    configuration = {
        "url": "mysql+mysqlconnector://root:XXr0898523290!@localhost:3306/sqlalchemy_db",
        "url_tests": "mysql+mysqlconnector://root:XXr0898523290!@localhost:3306/sqlalchemy_db_tests",
        "API_KEY": "Gp${_AZ`:~DYb_af]df?D<g_8/hPU;c`bR>&$m"
    }
    return configuration
