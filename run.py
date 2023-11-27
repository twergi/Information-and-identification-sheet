from source.main import run
import logging

LOG_FILENAME = "errors.log"
logging.basicConfig(filename=LOG_FILENAME, level=logging.ERROR)

if __name__ == "__main__":
    try:
        run()
    except Exception as ex:
        print("Возникла ошибка:", ex)

        logging.error(ex, exc_info=True)

    input("\n\nНажмите Enter для завершения программы")
