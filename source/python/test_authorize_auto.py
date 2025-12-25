import unittest
from unittest.mock import patch, MagicMock
from authorize import Authorize

class TestAuthorize(unittest.TestCase):

    def setUp(self):
        self.auth = Authorize("localhost", 5432, "testdb", "testuser", "testpass")

    @patch("psycopg2.connect")
    def test_get_magic_number_success(self, mock_connect: MagicMock):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchone.return_value = (1,)
        mock_cursor.rowcount = 1

        result = self.auth.get_magic_number("testuser")
        self.assertTrue(100000 <= result <= 999999)

    @patch("psycopg2.connect")
    def test_get_magic_number_user_not_found(self, mock_connect: MagicMock):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchone.return_value = None

        result = self.auth.get_magic_number("unknown_user")
        self.assertEqual(result, -1)

    @patch("psycopg2.connect")
    def test_try_unlock_success(self, mock_connect: MagicMock):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchone.return_value = (1, "password123")
        mock_cursor.rowcount = 1

        # 正しいハッシュを生成
        import zlib
        magic = 123456
        combined = f"password123{magic}"
        pass_hash = format(zlib.crc32(combined.encode()) & 0xFFFFFFFF, '08x')

        result = self.auth.try_unlock("testuser", magic, pass_hash)
        self.assertTrue(100000 <= result <= 999999)

    @patch("psycopg2.connect")
    def test_try_unlock_invalid_hash(self, mock_connect: MagicMock):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchone.return_value = (1, "password123")

        result = self.auth.try_unlock("testuser", 123456, "wronghash")
        self.assertEqual(result, -2)

    @patch("psycopg2.connect")
    def test_try_unlock_extend_success(self, mock_connect: MagicMock):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchone.return_value = (1,)
        mock_cursor.rowcount = 1

        result = self.auth.try_unlock_extend("testuser", 654321)
        self.assertTrue(100000 <= result <= 999999)

    @patch("psycopg2.connect")
    def test_get_feature_list_success(self, mock_connect: MagicMock):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchall.return_value = [
            (1, "Feature A", "/feature/a", None, None),
            (2, "Feature B", "/feature/b", b"icon", "image/png")
        ]

        result = self.auth.get_feature_list("testuser")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["fname"], "Feature A")
        self.assertEqual(result[1]["icon_mime_type"], "image/png")

if __name__ == "__main__":
    unittest.main()
