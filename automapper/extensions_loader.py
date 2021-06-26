from os.path import dirname, join, isfile, basename, dirname
import logging
import importlib
import importlib.util
import glob

from . import Mapper

__DEFAULT_EXTENSION__ = "default"
__EXTENSIONS_FOLDER__ = "extensions"
__PACKAGE_PATH__ = __package__ + "." + __EXTENSIONS_FOLDER__

log = logging.getLogger("automapper")


def load_extensions(mapper: Mapper) -> None:
    """It is designed that name of extension file should be the same as the module
    which extension is developed for.
    In this way current method will find and load the extension
    """
    extensions = glob.glob(join(dirname(__file__), __EXTENSIONS_FOLDER__, "*.py"))
    for extension in extensions:
        if isfile(extension) and not extension.endswith('__init__.py'):
            module_name = basename(extension)[:-3]
            if module_name == __DEFAULT_EXTENSION__ or importlib.util.find_spec(module_name) != None:
                try:
                    extension_package = importlib.import_module(__PACKAGE_PATH__ + "." + module_name)
                    extension_package.extend(mapper)
                except Exception:
                    log.exception(f"Found module {module_name} but could not load extension for it.")
