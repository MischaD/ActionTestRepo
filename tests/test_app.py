
class TestApp:
    def test_apis(self):
        from app.database import RDB
        RDB()
        assert True
