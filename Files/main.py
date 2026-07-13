from database.database import initialize_database
from gui.registration import RegistrationPage


def main():

    initialize_database()

    app = RegistrationPage()

    app.mainloop()


if __name__ == "__main__":
    main()