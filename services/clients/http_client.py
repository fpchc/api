import json
import logging
import os
from typing import Any, Dict

import requests


class HttpClient:
    @staticmethod
    def post(url: str, data: Dict[str, any], headers: Dict[str, any] = None) -> requests.Response:
        response = requests.post(url, data, headers=headers)
        response.raise_for_status()
        return response
    
    
def search_query(query: str, headers: Dict[str, Any] = None) -> list:
    base_url = os.getenv("SPIDER_API_URL")
    if not base_url:
        print("Error: SPIDER_API_URL environment variable is not set.")
        return []

    url = f"{base_url}/search"
    headers = headers or {"Content-Type": "application/json"}
    data = {"query": query}
    
    try:
        response = HttpClient.post(url=url, data=json.dumps(data), headers=headers)
        response.raise_for_status()  # 确保请求成功
        
        # 解析响应数据
        response_json = response.json()
        return response_json.get("success", [])
    
    except requests.exceptions.HTTPError as err:
        logging.error(f"HTTPError: {err}")
        if response is not None:
            logging.error(f"Response content: {response.text}")
        return []  # 返回空列表或者你可以选择抛出异常
        
    except requests.exceptions.RequestException as e:
        logging.error(f"RequestException: {e}")
        return []  # 请求错误时返回空列表
    
    except Exception as ex:
        logging.error(f"An unexpected error occurred: {ex}")
        return []  # 未知错误时返回空列表
