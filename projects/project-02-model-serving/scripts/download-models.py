#!/usr/bin/env python
"""
Download sample models for development and testing

TODO: Implement model downloading from various sources
"""

import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def download_sample_models():
    """
    Download sample ONNX models

    TODO: Implement downloading:
    - ResNet-50 from ONNX Model Zoo
    - BERT model
    - Simple scikit-learn model
    - Store in models/ directory
    """
    logger.info("Downloading sample models...")

    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)

    # TODO: Download ResNet-50
    # url = "https://github.com/onnx/models/raw/main/vision/classification/resnet/model/resnet50-v1-7.onnx"
    # download_file(url, models_dir / "resnet50.onnx")

    # TODO: Download BERT
    # url = "https://github.com/onnx/models/raw/main/text/machine_comprehension/bert-squad/model/bertsquad-10.onnx"
    # download_file(url, models_dir / "bert.onnx")

    logger.info("Sample models downloaded successfully")


def download_file(url: str, destination: Path):
    """
    Download a file from URL

    TODO: Implement file download with progress bar
    """
    import requests
    from tqdm import tqdm

    logger.info(f"Downloading {url}...")

    # TODO: Implement download
    # response = requests.get(url, stream=True)
    # total_size = int(response.headers.get('content-length', 0))
    #
    # with open(destination, 'wb') as f, tqdm(
    #     total=total_size,
    #     unit='B',
    #     unit_scale=True
    # ) as pbar:
    #     for chunk in response.iter_content(chunk_size=8192):
    #         f.write(chunk)
    #         pbar.update(len(chunk))

    logger.info(f"Downloaded to {destination}")


if __name__ == "__main__":
    download_sample_models()
