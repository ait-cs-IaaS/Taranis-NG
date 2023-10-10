import worker.publishers
from worker.publishers.base_publisher import BasePublisher
from worker.log import logger
from worker.core_api import CoreApi
from requests.exceptions import ConnectionError

core_api = CoreApi()

publishers = {
    "email_publisher": worker.publishers.EMAILPublisher(),
    "twitter_publisher": worker.publishers.TWITTERPublisher(),
    "wordpress_publisher": worker.publishers.WORDPRESSPublisher(),
    "ftp_publisher": worker.publishers.FTPPublisher(),
}


def get_product(product_id: int) -> tuple[dict[str, str] | None, str | None]:
    try:
        product = core_api.get_product(product_id)
    except ConnectionError as e:
        logger.critical(e)
        return None, str(e)

    if not product:
        logger.error(f"Product with id {product_id} not found")
        return None, f"Product with id {product_id} not found"
    return product, None


def get_publisher(product) -> tuple[BasePublisher | None, str | None]:
    publisher_type = product.get("type")
    if not publisher_type:
        logger.error(f"Product {product['id']} has no publisher_type")
        return None, f"Product {product['id']} has no publisher_type"

    if publisher := publishers.get(publisher_type):
        return publisher, None

    return None, f"Publisher {publisher_type} not implemented"


def publish_product(product_id: int):
    err = None

    product, err = get_product(product_id)
    if err or not product:
        return err

    logger.debug(f"Rendering product {product}")

    publisher, err = get_publisher(product)
    if err or not publisher:
        return err

    published_product = publisher.publish(product)
    if not published_product:
        return "Error generating product"
    if "error" in published_product:
        return published_product["error"]

    return "Product published successfully"
