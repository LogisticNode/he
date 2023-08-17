from click import Context


def check_config_file_extention(ctx: Context, param, value):
    logger = ctx.obj

    config_path = value
    file_extention = config_path.rsplit('.', 1)[1]
    
    if file_extention != 'yaml' and file_extention != 'yml':
        msg = f'Error: Unsupported extention of config file: {file_extention} config is not supported'
        logger.critical(msg)
        ctx.exit(1)        
