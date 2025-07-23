from unittest import result
from duckduckgo_search import DDGS
from googlesearch import search
from read_conf_file import read_yaml_file
import time

def cerca_links_DDGS(logger, config_data):
    # Input da file di configurazione
    query_array = config_data['search_links']['keywords']

    #mette insieme gli elementi dell'array separati da virgola
    query = ",".join(query_array)

    # Cerca link
    logger.info("\n📡 Cerco link...")
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=10):
            results.append(r["href"])
            time.sleep(5)

    if not results:
        logger.error("❌ Nessun risultato trovato.")
#            exit()

    return results


def cerca_links_GOOGLE(logger, config_data):
    query_array = config_data['search_links']['keywords']

    #mette insieme gli elementi dell'array separati da virgola
    query = ",".join(query_array)

    results = []
    for result in search(query, num_results=100):
        results.append(result)
        
    print(results)

    if not results:
        logger.error("❌ Nessun risultato trovato.")
#            exit()

    return results

def cerca_links(logger, config_data):

    if (config_data['mode'] == 'search_links'):

        # result = cerca_links_DDGS(logger, config_data)
        results = cerca_links_GOOGLE(logger, config_data)

        urls_string = ",".join(results)

        logger.info(f"URL trovate: {urls_string.replace(',','\n')}")

        #save found links in 'output_file'
        with open(config_data['search_links']['output_file'], 'w', encoding='utf-8') as f:
            f.write(urls_string.replace(',','\n'))

        return urls_string
    elif (config_data['mode'] == 'read_links'):
        with open(config_data['read_links']['saved_links_file'], 'r', encoding='utf-8') as f:
            righe = f.readlines()

        with open(config_data['read_links']['saved_links_file'], 'r', encoding='utf-8') as f:
            righe = [riga.rstrip('\n') for riga in f]

        return ','.join(righe)






