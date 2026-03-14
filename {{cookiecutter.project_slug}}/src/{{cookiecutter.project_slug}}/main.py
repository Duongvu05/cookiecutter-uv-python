from loguru import logger
from {{ cookiecutter.project_slug }} import hello

def main():
    logger.info(hello())

if __name__ == "__main__":
    main()
