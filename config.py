import configparser


class AppConfig:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")

    def ConnectionString(self):
        return self.config["config"]["connectionstring"]

   
    def OptionChianUrlFormat(self):
        return self.config["config"]["optionchianurlformat"]
    
   
    def TableName(self):
        return self.config["config"]["tablename"]

