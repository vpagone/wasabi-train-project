import yaml
 
def read_yaml_file(file_path):
        try:
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)
                return data
        except FileNotFoundError as e:
            print(f"File '{file_path}' non trovato" )
            return None
        except PermissionError as e:
            print(f"Non ci sono i permessi sul file: {f}" )
            return None
        except yaml.YAMLError as e:
            print(f"Error parsing YAML: {e}")
            return None
                
 
if __name__ == "__main__":
    config_file_path = r"C:\Users\utente\source\repos\progetto_scraping\scrapy_project_1\cfg\conf.yml"  # Replace with your file name or use sys.argv for CLI
    config_data = read_yaml_file(config_file_path)
 
    if config_data:
        print("YAML content:")
        print(config_data)
 
    #dentro Keyword prende la chiave ricerca e stampa la lista (contenuto)
    print(config_data['keywords']['initial_query'])
    print(config_data['keywords']['content_filter'])
    print(config_data['max_depth'])



