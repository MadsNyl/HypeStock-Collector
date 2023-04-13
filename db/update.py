from db.setup import pool, db
from db.model import Query

class UPDATE():

    @staticmethod
    def legacy(symbol: str):
        """
            Updates legacy for a symbol to true.
        """
        try:
            pool.execute(
                Query.update_legacy(),
                (symbol, )
            )

            db.commit()
        except Exception as e:
            print(f"Updating legacy error: {e}")