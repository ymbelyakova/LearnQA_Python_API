import requests
import pytest

class TestUserAgentCheck:
    data = {
        "user_agents": [
            {
                "id": 1,
                "user_agent": "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
                "platform": "Mobile",
                "browser": "No",
                "device": "Android"
            },
            {
                "id": 2,
                "user_agent": "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
                "platform": "Mobile",
                "browser": "Chrome",
                "device": "iOS"
            },
            {
                "id": 3,
                "user_agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
                "platform": "Googlebot",
                "browser": "Unknown",
                "device": "Unknown"
            },
            {
                "id": 4,
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
                "platform": "Web",
                "browser": "Chrome",
                "device": "No"
            },
            {
                "id": 5,
                "user_agent": "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
                "platform": "Mobile",
                "browser": "No",
                "device": "iPhone"
            }
        ]
    }

    @pytest.mark.parametrize("ua_entry", data["user_agents"])
    def test_user_agent_check(self, ua_entry):
        url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
        headers = {"User-Agent": ua_entry["user_agent"]}

        response = requests.get(url, headers=headers)
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

        resp_json = response.json()

        # Проверка соответствия поля platform
        assert resp_json.get("platform") == ua_entry["platform"], (
            f"Platform mismatch for User-Agent={ua_entry['user_agent']}: "
            f"expected '{ua_entry['platform']}', got '{resp_json.get('platform')}'"
        )
        # Проверка соответствия поля browser
        assert resp_json.get("browser") == ua_entry["browser"], (
            f"Browser mismatch for User-Agent={ua_entry['user_agent']}: "
            f"expected '{ua_entry['browser']}', got '{resp_json.get('browser')}'"
        )
        # Проверка соответствия поля device
        assert resp_json.get("device") == ua_entry["device"], (
            f"Device mismatch for User-Agent={ua_entry['user_agent']}: "
            f"expected '{ua_entry['device']}', got '{resp_json.get('device')}'"
        )

