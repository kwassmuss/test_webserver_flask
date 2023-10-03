# test_webserver_flask
a smal flask test webserver

no nginx/apache; some shortcuts. Don't use in production

Note:
The POST request "curl -X POST --data-binary "@test.csv" leads to flask storing the binary file content *encoded as a string in request.form.keys* which disturbs the encoding of the data.
This code assumes that the app has to deal with this disturbed data submitted by a user.

Another way to send a binary file would be to use curl -F . The file content could then be accessed from request.files in binary form without the encoding problems.
This code assumes however that the app has to deal with the disturbed data submitted by a user and it filters out the resulting repesentation of the EURO SIGN using ord().

Note however that this solution depends on the encoding of the file and would most likely break with files using different encodings or with files containing other special characters.

A more general solution would be to filter out all characters above a certain threshold ( ord(c) > threshold ). 
Special characters could however also be present in the column headers of the csv file where they would also be removed so this solution would still be far from perfect.

When it is possible to control the request it would of course be better to first retrieve the binary data from request.files and deal with any possibly remaining encoding problems later.

From the curl manual:

-------------------
-F/--form

(HTTP) This lets curl emulate a filled-in form in which a user has pressed the submit button. This causes curl to POST data using the Content-Type multipart/form-data according to RFC2388. This enables uploading of binary files etc.

[...]

--data-binary <data>

(HTTP) This posts data exactly as specified with no extra processing whatsoever.

If you start the data with the letter @, the rest should be a filename. Data is posted in a similar manner as -d, --data does, except that newlines and carriage returns are preserved and conversions are never done.

Like -d, --data the default content-type sent to the server is application/x-www-form-urlencoded. If you want the data to be treated as arbitrary binary data by the server then set the content-type to octet-stream: -H "Content-Type: application/octet-stream".

[...]

