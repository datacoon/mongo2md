#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
import click
import json
import logging

from .cmds.documenter import Documenter
from .cmds.suggester import Suggester

# logging.getLogger().addHandler(logging.StreamHandler())
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)


def enableVerbose():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG,
    )


@click.group()
def cli1():
    pass


@cli1.command()
@click.argument("dbname")
@click.argument("collname", default=None, required=False)
@click.option("--host", "-h", default=None, help="Hostname")
@click.option("--port", "-p", default=None, help="Port")
@click.option(
    "--output", "-o", default=None, help="Default directory to create project data "
)
def prepare(dbname, collname=None, host=None, port=None, output=None):
    """Reads database information and prepares mock files"""
    acmd = Documenter(host, port)
    acmd.prepare_documents(dbname, collname, projpath=output)
    pass


@click.group()
def cli2():
    pass


@cli2.command()
@click.argument("projpath")
def document(projpath):
    """Generates documentation based on project information"""
    acmd = Documenter()
    acmd.generate_documents(projpath)
    pass


@click.group()
def cli3():
    pass


@cli3.command()
@click.argument("projpath")
@click.option("--fieldsmapfile", "-f", default=None, help="File with fields mapped")
def suggest(projpath, fieldsmapfile):
    """Interactively helps to fill gaps"""
    acmd = Suggester(fieldsmapfile)
    acmd.suggester(projpath)
    pass


cli = click.CommandCollection(sources=[cli1, cli2, cli3])

# if __name__ == '__main__':
#    cli()
