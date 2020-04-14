from flask import Flask, make_response, request
import io
import csv

DATE = 1
MEMO = 2
AMMT = 3

app = Flask(__name__)

@app.route('/')
def index():
    return """
        <html>
            <body>
                <h1>Combine NetSuite line items.</h1>

                <form action="/transform" method="post" enctype="multipart/form-data">
                    <p>Select .csv file to process:</p>
                    <input type="file" name="data_file" />
                    <input type="submit" value="Go" />
                </form>
            </body>
        </html>
    """

@app.route('/transform', methods=["POST"])
def transform_view():
    f = request.files['data_file']
    if not f:
        return "No file"

    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    reader = csv.reader(stream)

    result = []
    for row in reader:
    	if not result:
    		result.append(row)
    	elif row[DATE] == result[-1][DATE] and row[MEMO] == result[-1][MEMO]:
    		result[-1][AMMT] += float(row[AMMT])
    	else:
    		result.append(row)
    		result[-1][AMMT] = float(result[-1][AMMT])

    for row in result:
    	if isinstance(row[AMMT], float):
    		row[AMMT] = '%.2f' % row[AMMT]

    body = io.StringIO()
    writer = csv.writer(body)
    for row in result:
    	writer.writerow(row)

    response = make_response(body.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=result.csv"
    return response
