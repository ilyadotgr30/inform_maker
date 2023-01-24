from flask import *
import json
import parsemaker



app = Flask(__name__)

@app.route('/tommorow_inform', methods=['GET'])

def request_inform():
    data_set = {'theme': parsemaker.themes[parsemaker.datetime.date.weekday(parsemaker.datetime.date.today() + parsemaker.datetime.timedelta(days=1))],
                 'tomm_date': parsemaker.get_date(parsemaker.tommorow_date()),
                 'm': parsemaker.get_mounth(parsemaker.tommorow_date()),
                 'y': parsemaker.tommorow_date().split('.')[2],
               # 'creator_name': ,
                 'header_1': parsemaker.headers[0],
                 'header_2': parsemaker.headers[1],
                 'header_3': parsemaker.headers[2],
                 'header_4': parsemaker.headers[3],
                 'header_5': parsemaker.headers[4],
                 'text_1': parsemaker.mod_texts[0],
                 'text_2': parsemaker.mod_texts[1],
                 'text_3': parsemaker.mod_texts[2],
                 'text_4': parsemaker.mod_texts[3],
                 'text_5': parsemaker.mod_texts[4],
                 'briefing_text': parsemaker.parse_briefing()}
    json_dump = json.dumps(data_set)

    return json_dump


app.run()

