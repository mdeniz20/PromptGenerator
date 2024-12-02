class Topics:
    file_path = None
    
    
    def __init__(self, file_path):
        self.file_path = file_path
    
    def get_topics_list(self):
        if not self.file_path:
            return []
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return self.__get_list(file.readlines())
        except FileNotFoundError:
            print(f"Error: File '{self.file_path}' not found.")
            return []
        except IOError as e:
            print(f"IOError while reading the file: {e}")
            return []
        
    def __get_list(self, lines: list) -> list:
        return [line.strip() for line in lines if line.strip()]
    

