"""
Purpose: A parser that reads a yaml file and loads it into an OmegaConf object.
"""

from omegaconf import OmegaConf
from loguru import logger


class ConfigParser:

    def __init__(self, config_path: str, config_root: str, environment: str, **kwargs):
        self.config_path = config_path
        self.config_root = config_root
        self.environment = environment
        self.config = self.parse(**kwargs)

    def collect_environment_template(self):
        path = f"{self.config_root}/envs.yaml"
        with open(path, "r") as file:
            template = OmegaConf.load(file)
            logger.info(f"Environment: {self.environment}")
            logger.debug(f"Environment template: {template[self.environment]}")
            return template[self.environment]

    def parse(self, **kwargs):
        environment_template = self.collect_environment_template()
        with open(f"{self.config_root}/{self.config_path}.yaml", "r") as file:
            config = OmegaConf.load(file)

            # Inject environment config values
            for key, value in environment_template.items():
                OmegaConf.update(config, key, value)

            # Override any options
            for key, value in kwargs.items():
                OmegaConf.update(config, key, value)

            return config
