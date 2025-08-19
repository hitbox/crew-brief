# Models

This document describes the application database models and their purposes and relations.

## OSWalk

The arguments and options for the os.walk function; and the files (LegFile) that were scanned from it.

## LegFile

A path discovered by OSWalk. Keeps some stats about the file and what type of file it is.

## LegIdentifier

A single leg identifier scraped from a LegFile.

## Scraper

Named object associated with one or more Regex objects and optionally a postmatch_handler function.
