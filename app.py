import flask

from api import main

app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def app_home():
    return flask.render_template('index.html')


@app.route('/receive', methods=['GET'])
def receive():
    args = flask.request.args.to_dict()

    if main(args['name'], args['roll'], args['room'], args['form_id'], args['def_opt']):
        return "Successful"
    else:
        return "Failed! Please check form_id<br/><br/>For a link 'https://docs.google.com/forms/d/e/1FAIpQLSd0DODVQPFPUYI2uEs9qNmXaJIaYxl4EKtJd8k_WlRTJ_l3wg/viewform'\n" \
               "<br/>form id is '1FAIpQLSd0DODVQPFPUYI2uEs9qNmXaJIaYxl4EKtJd8k_WlRTJ_l3wg'"


if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True)
