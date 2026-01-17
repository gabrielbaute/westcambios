from app.seeds.create_users import create_users
from app.seeds.create_rates import create_rates

if __name__ == "__main__":
    create_users()
    create_rates()