from flask import Flask
from flask_restful  import reqparse, Api, Resource

from optics import OPTICS

app = Flask(__name__)
api = Api(app)

all_exps = {}

def exists(exp_id):
    if exp_id not in all_exps:
        return 1
    return 0
    
#single experiment
class Experiment(Resource):
    def get(self, exp_id):
        not_exist = exists(exp_id)
        if (not_exist):
            return 404, "this experiment doesn't exist"
        return all_exps[exp_id]

    def post(self, exp_id):
        pars = reqparse.RequestParser()
        pars.add_argument('dataset')  
        pars.add_argument('eps', type=float)
        pars.add_argument('min_pts', type=int)
        args = pars.parse_args()

        if (all_exps[exp_id] != {}):
            return 409, "begin new experiment"

        if (args['dataset'] is None):
            return 400, "dataset is not given"

        if ((args['eps'] is None) or (args['min_pts'] is None)):
            return 400, "not enough parameters for OPTICS"

        labels = OPTICS(args['dataset'], args['eps'], args['min_pts'])
        all_exps[exp_id] = labels
        return labels, 201

    def delete(self, exp_id):
        not_exist = exists(exp_id)
        if (not_exist):
            return 404, "this experiment doesn't exist"
        del all_exps[exp_id]
        return '', 204

# multiple experiments
class ExperimentList(Resource):
    def get(self):
        return all_exps

    def post(self):
        if (len(all_exps.keys()) == 0):
            exp_id = 1
        else:
            exp_id = int(max(all_exps.keys())) + 1
        all_exps[exp_id] = {}
        return all_exps[exp_id], 201

api.add_resource(ExperimentList, '/all_exps')
api.add_resource(Experiment, '/all_exps/<int:exp_id>')

if __name__ == '__main__':
    app.run(debug=True)
