from flask import Flask, request, jsonify
from flask_restful import Resource, Api

from database import Database
from classifier import Classifier

class API:
    def __init__(self):
        self.app = Flask(__name__)
        api = Api(self.app)

        api.add_resource(Plugin, '/')
        api.add_resource(Classify, '/plugin/classify')
        api.add_resource(QnA, '/plugin/qna')
        api.add_resource(Relearn, '/plugin/relearn')

    def run_app(self):
        self.app.run(debug=True)
        # debug never in production


class Plugin(Resource):
    def get(self):
        return "Plugin For AI QnA Board"


class Classify(Resource):
    def __init__(self):
        self.db = Database()
        self.classifier = Classifier("model.pt")

    def get(self):
        res = -1
        analyzed = -1
        question = None

        try:
            data = request.get_json()
            if data is not None:
                question = data.get('question')

            if question is not None:
                analyzed = self.classifier.classify(question) 

            if analyzed != -1:
                answer = self.db.get_answer(analyzed)
                res = 1

        except Exception as e:
            print("Error in classify")
            print(e)

        finally:
            if data is None:
                return "QnA API - Classify"
            else:
                if res == 1:
                    return jsonify({"answer" : f"{analyzed}"})
                else:
                    return jsonify({"answer": res})


class QnA(Resource):
    def __init__(self):
        self.db = Database()

    def get(self):
        return "QnA API - QnA"

    def post(self):
        res = -1
        a_id = -1

        try:
            question = request.get_json().get('question')
            answer = request.get_json().get('answer')

            if answer is not None:
                a_id = self.db.add_answer(answer)

            if a_id != -1:
                res = self.db.add_question(question, a_id)

                if res != -1:
                    res = 1

        except Exception as e:
            print("Error in QnA")
            print(e)

        finally:
            return jsonify({"result": res})


class Relearn(Resource):
    def get(self):
        return "QnA API - Relearn"

    def post(self):
        try:
            return 1

        except Exception as e:
            print("Error in Relearn")
            print(e)

        finally:
            return 1


if __name__ == "__main__":
    CA = API()
    CA.run_app()


# 예제 나중에 지우기
# curl -i -H "Content-Type: application/json" -X POST -d "{\"question\":\"Rest API \uD14C\uC2A4\uD2B8\",\"answer\":\"REST API \uD14C\uC2A4\uD2B8\"}" http://localhost:5000/plugin/qna