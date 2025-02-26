import requests
from loguru import logger


class APIMaster:
    def __init__(self, base_url: str, base_port: str, api_key: str):
        self.base_url = base_url
        self.port = base_port
        self.api_key = api_key
        self.headers = {"api_key": self.api_key}
        self.orchestration_endpoint = f'http://{self.base_url}:{self.port}'
        logger.info(f"Initialized APIMaster with base URL: {self.base_url}")

    def register_heartbeat(self):
        endpoint = '/api/register_heartbeat'
        url = f'{self.orchestration_endpoint}{endpoint}'
        logger.info(f"Registering heartbeat at endpoint: {endpoint}")

        try:
            response = requests.post(url=url, headers=self.headers)
            logger.debug(f"Response status code: {response.status_code}")
            result = response.json()
            logger.success(f"Successfully registered heartbeat")
            return result
        except Exception as e:
            logger.error(f"Error registering heartbeat: {str(e)}")
            raise

    def get_task_information(self, task_uuid: str, work_package_uuid: str) -> dict:
        endpoint = '/api/get_task_information'
        url = f'{self.orchestration_endpoint}{endpoint}'
        data = {'task_uuid': task_uuid, 'work_package_uuid': work_package_uuid}
        logger.info(f"Getting task information at endpoint: {endpoint}")
        logger.debug(f"Task UUID: {task_uuid}, Work Package UUID: {work_package_uuid}")

        try:
            response = requests.post(url=url, json=data, headers=self.headers)
            logger.debug(f"Response status code: {response.status_code}")
            result = response.json()
            logger.success(f"Successfully retrieved task information")
            return result
        except Exception as e:
            logger.error(f"Error getting task information: {str(e)}")
            raise

    def get_task_meta(self, task_meta_id: str) -> dict:
        endpoint = '/get_task_meta'
        url = f'{self.orchestration_endpoint}{endpoint}'
        data = {'task_meta_id': task_meta_id}
        logger.info(f"Getting task meta at endpoint: {endpoint}")
        logger.debug(f"Task meta ID: {task_meta_id}")

        try:
            response = requests.post(url=url, json=data, headers=self.headers)
            logger.debug(f"Response status code: {response.status_code}")
            result = response.json()
            logger.success(f"Successfully retrieved task meta")
            return result
        except Exception as e:
            logger.error(f"Error getting task meta: {str(e)}")
            raise

    def check_for_checkpoints(self, task_uuid: str, work_package_uuid: str) -> dict:
        endpoint = '/api/check_checkpoint_information'
        url = f'{self.orchestration_endpoint}{endpoint}'
        data = {'task_uuid': task_uuid, 'work_package_uuid': work_package_uuid}
        logger.info(f"Getting checkpoints at endpoint: {endpoint}")

        try:
            response = requests.post(url=url, json=data, headers=self.headers)
            logger.debug(f"Response status code: {response.status_code}")
            result = response.json()
            logger.success(f"Successfully retrieved checkpoints")
            return result
        except Exception as e:
            logger.error(f"Error getting checkpoints: {str(e)}")
            raise




if __name__ == '__main__':
    run = APIMaster()