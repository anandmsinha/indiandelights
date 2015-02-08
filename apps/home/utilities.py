from collections import defaultdict
import logging


logger = logging.getLogger(__name__)

def processMenuItems(menu_items):
    """
        This method creates a dictionary of menu items and groups them.
    """
    main_dict = defaultdict(list)
    if menu_items:
        logger.debug("Process menu items called with list size - {0}".format(len(menu_items)))
        for item in menu_items:
            key = item.parent if item.parent else 'Categories'
            main_dict[key].append(item)
    logger.debug("Return size of dict is - {0}".format(len(main_dict)))
    return dict(main_dict)
