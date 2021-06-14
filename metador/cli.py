"""
Utility CLI for the application.
"""

from typing import Optional

import uvicorn  # type: ignore
import typer

from . import __version__, __pkg_path__
from . import config as c
from .orcid import Auth
from .util import prepare_dirs
from .log import patch_uvicorn_log_format

app = typer.Typer()


@app.command()
def version() -> None:
    """Print current version."""

    print(__version__)


@app.command()
def default_conf() -> None:
    """Output a default metador.toml file.
    It contains  all available configuration options."""

    print(open(c.DEF_CONFIG_FILE, "r").read(), end="")


@app.command()
def tusd_hook_url(config: Optional[str] = None) -> None:
    """
    Output the route to construct a hook path for tusd.
    """

    c.init_conf(config)  # correct result depends on configured metador.site
    print(c.conf().metador.site + c.TUSD_HOOK_ROUTE)


@app.command()
def orcid_redir_url(config: Optional[str] = None) -> None:
    """
    URL that should be registered as the ORCID API redirect.
    """

    c.init_conf(config)  # correct result depends on configured metador.site
    print(Auth(c.conf().metador.site, c.conf().orcid).get_orcid_redir())


@app.command()
def run(config: Optional[str] = None) -> None:
    """Serve application using uvicorn."""

    c.init_conf(config)
    prepare_dirs()

    # add date and time to uvicorn log
    patch_uvicorn_log_format()
    # run server. if reload is active, it watches for changes in the Python code.
    # The templates and static files can be changed on runtime anyway.
    # If you want to change a conf and reload, just "touch" a Python file forcing reload
    uvicorn.run(
        "metador.server:app",
        host=c.conf().uvicorn.host,
        port=c.conf().uvicorn.port,
        reload=c.conf().uvicorn.reload,
        reload_dirs=[__pkg_path__],
    )


if __name__ == "__main__":
    app()
