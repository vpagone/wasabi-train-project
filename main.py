import sys
import yaml
import logging
from pathlib import Path
import subprocess

from read_conf_file import read_yaml_file
from cerca_links import cerca_links
#from scrapy_project_1.scrapy_project_1.spiders.generic_spider import run_spider
  
def init(config_file_path):

    #carica il file di configurazione
    config_data = read_yaml_file(config_file_path)

    # Default log file path (can also be pulled from config if needed)
    log_file_path = Path(config_data['general']['file_log_name'])
 
    # Create a logger object
    logger = logging.getLogger("main_logger")
 
    # Optional: Set the logging level
    logger.setLevel(logging.INFO)
 
    # Add a file handler
    file_handler = logging.FileHandler(log_file_path)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
 
    logger.addHandler(file_handler)

    # Example: log part of the config
    logger.info(f"Loaded config keys: {list(config_data.keys()) if config_data else 'Empty config'}")

    return logger, config_data
 
if __name__ == "__main__":

#    if len(sys.argv) != 2:
#        print("Usage: python load_config_and_log.py <path_to_config.yaml>")
#        sys.exit(1)
#
#    logger, config_data = init(Path(sys.argv[1]))

    logger, config_data = init(Path(r"C:\Users\utente\source\repos\progetto_scraping\scrapy_project_1\cfg\conf.yml"))

    # Trova url dalle keyword nel file di configurazione
    logger.info("Avvio cerca links...")
    #urls_string = cerca_links(logger, config_data['cerca_links'])
    #urls_string = "https://www.pluswatch.it/?srsltid=AfmBOoqHUi435jtBVV10eTSxReKoasAroKO8Z8xLd_afuaB_XZLTsjYf"
    #urls_string = "https://replichedilusso.co/categoria-prodotto/imitazione-e-repliche-rolex/datejust/"
    urls_string="https://opsobjects.com/en/product/sport-orologio-con-cassa-e-bracciale-in-metallo/?attribute_pa_colore=oro-giallo"
    #urls_string="https://opsobjects.com"

    logger.info("Avvio scraping...")
    # Avvia Scrapy con i parametri
    content_filter_array = config_data['spider']['keywords']
    content_filter = ",".join(content_filter_array)

    #file_log_name_scrapy = config_data['file_log_name_scrapy']

    max_depth = config_data['spider']['max_depth']

    #logger.info("\n🕷️ Avvio Scrapy Spider con filtro contenuti attivo...")
    logger.info("\nAvvio Scrapy Spider con filtro contenuti attivo...")
    subprocess.run([
#       "scrapy", "crawl", "generic_spider",
#        "scrapy", "crawl", "shopclues",
#       "scrapy", "crawl", "ecommerce",
        "scrapy", "crawl", "detect",              #detect, product_detector
        "-a", f"urls={urls_string}",
        "-a", f"keywords={content_filter}",
        "-O", "RISULTATI.csv",
        "-s", f"DEPTH_LIMIT={max_depth}",
        "-s", "LOG_LEVEL=INFO"
    ], cwd="scrapy_project_1")

#    run_spider(urls_string,content_filter)


