##########################
# Setting the parameters #
##########################

import configparser

class CommonConfig:
    def config_generator():
        config = configparser.ConfigParser()

        # config['log'] = {}
        # config['log']['path'] = './common/log/'
        # config['log']['name'] = 'server.log'

        # Save set_file
        with open('./common/config.ini', 'w', encoding='utf-8') as configfile:
            config.write(configfile)


    def config_read():
        # Load set_file
        config = configparser.ConfigParser()
        config.read('./common/config.ini', encoding='utf-8')
        return config
