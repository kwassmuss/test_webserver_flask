#!/usr/bin/python3

from flask import Flask, request
import pandas
import tempfile
import logging


app = Flask(__name__)

FILESIZE_LIMIT = 1 * 1000 * 1000 * 1000 # 1GB
app.config["MAX_CONTENT_LENGTH"] = FILESIZE_LIMIT

request_logger = logging.getLogger( __name__ )  # logs api requests 
# app.logger will default to loglevel WARNING outside of dev mode
request_logger.setLevel( logging.INFO )  


@app.route("/health/")
def health():
    """
    return 'OK'
    """
    app.logger.info("health()")
    return "<p>OK</p>"


@app.route(
    "/stats/", methods=("POST",)
)
def stats(sep=";", column="Krankenhauskosten"):
    """
    return sum and average of column grouped by 'Zeitindex' as json
    the implementation is currently not very pretty or robust but should at least work for the test file

    parameters
    ----------
    sep:    CSV field separator, defaults to ';'
    column: column from csv file, defaults to 'Krankenhauskosten'
    """
    app.logger.info("stats()")
    try:
        sep = request.args.get("sep")
        column = request.args.get("column")
        request_logger.info(f"stats request {sep} {column}")

        ## converters could be passed to pandas.read_csv to deal with special characters, but that doesnt solve the encoding problem
        # converters = { 'Krankenhauskosten': lambda s: float(s.replace('€', '')) }

        ## here the tricky part begins

        s = list(request.form.keys())[
            0
        ]  # this is where the binary file content ends up (as a string)

        ## we filter out the bytes of the problematic special characters directly to deal with the encoding problems
        fixencoding = lambda s: bytes(
            ord(" ") if ord(c) == 65533 else ord(c) for c in s
        )  # EUR -> ' ': will be directly parsable

        with tempfile.TemporaryFile() as fp:  # could also be done in memory with a buffer
            fp.write(fixencoding(s))
            fp.seek(0)  # reset position in file
            # df = pandas.read_csv( fp, delimiter=sep,
            #                       usecols=['PID', 'Zeitindex', column], converters=converters )
            df = pandas.read_csv(
                fp, delimiter=sep, usecols=["PID", "Zeitindex", column]
            )
        grouped = df.groupby("Zeitindex")
        count = grouped.count()[column]
        sums = grouped.sum()[column]
        response = {"Summe": sums.to_dict()}
        response["Durchschnitt"] = (sums / count).to_dict()
        request_logger.info(f"stats response {response}")
        return response
    except Exception as e:
        msg = f"exception in stats {e}"
        app.logger.warning(msg)
        logging.exception(msg)
        return msg
