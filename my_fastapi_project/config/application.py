"""Application configuration - FastAPI."""
from pydantic import BaseSettings
from my_fastapi_project.version import __version__


class Application(BaseSettings):
    """Define application configuration model.

    Constructor will attempt to determine the values of any fields not passed
    as keyword arguments by reading from the environment. Default values will
    still be used if the matching environment variable is not set.

    Environment variables:
        * FASTAPI_DEBUG
        * FASTAPI_PROJECT_NAME
        * FASTAPI_VERSION
        * FASTAPI_DOCS_URL
        * FASTAPI_USE_REDIS
        * FASTAPI_COS_SECRET_ID
        * FASTAPI_COS_SECRET_KEY
        * FASTAPI_COS_BUCKET
        * FASTAPI_COS_REGION

    Attributes:
        DEBUG (bool): FastAPI logging level. You should disable this for
            production.
        PROJECT_NAME (str): FastAPI project name.
        VERSION (str): Application version.
        DOCS_URL (str): Path where swagger ui will be served at.
        USE_REDIS (bool): Whether or not to use Redis.
        COS_SECRET_ID (str): Tencent Cloud COS secret ID.
        COS_SECRET_KEY (str): Tencent Cloud COS secret key.
        COS_BUCKET (str): Tencent Cloud COS bucket name.
        COS_REGION (str): Tencent Cloud COS region.

    """

    DEBUG: bool = True
    PROJECT_NAME: str = "my-fastapi-project"
    VERSION: str = __version__
    DOCS_URL: str = "/swaggerUi"
    USE_REDIS: bool = False
    DATABASE_URL: str = "mysql+aiomysql://root:123456@localhost:3306/home_cook"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    WX_APP_ID: str = ""
    WX_APP_SECRET: str = ""
    COS_SECRET_ID: str = ""
    COS_SECRET_KEY: str = ""
    COS_BUCKET: str = ""
    COS_REGION: str = "ap-guangzhou"
    # All your additional application configuration should go either here or in
    # separate file in this submodule.

    class Config:
        """Config sub-class needed to customize BaseSettings settings.

        Attributes:
            case_sensitive (bool): When case_sensitive is True, the environment
                variable names must match field names (optionally with a prefix)
            env_prefix (str): The prefix for environment variable.

        Resources:
            https://pydantic-docs.helpmanual.io/usage/settings/

        """

        case_sensitive = True
        env_prefix = "FASTAPI_"
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Application()
