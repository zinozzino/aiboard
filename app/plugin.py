from flask import Flask, request, jsonify
from flask_restful import Resource, Api

from database import Database

class API:
    def __init__(self):
        self.app = Flask(__name__)
        api = Api(self.app)

        api.add_resource(Plugin, '/')
        api.add_resource(RequestAnalysis, '/plugin/RA')
        api.add_resource(AddQnA, '/plugin/AQA')

    def run_app(self):
        self.app.run(debug=True)
        # debug never in production


class Plugin(Resource):
    def get(self):
        return "Plugin For AI QnA Board"


class RequestAnalysis(Resource):
    def __init__(self):
        self.db = Database();

    def get(self):
        return "QnA API - Request Analysis"

    def put(self):
        res = -1
        analyzed = -1

        try:
            question = request.get_json().get('question')
            # print(question)

            if question is not None:
                analyzed = 1
                # 자연어 처리 함수 여기에

            if analyzed != -1:
                answer = self.db.get_answer(analyzed)
                # print(answer)
                res = 1

        except Exception as e:
            print("Error in RA")
            print(e)

        finally:
            if res == 1:
                return jsonify({"answer": answer})
            else:
                return jsonify({"answer": res})


class AddQnA(Resource):
    def __init__(self):
        self.db = Database()

    def get(self):
        return "QnA API - Add QnA"

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
            print("Error in AQA")
            print(e)

        finally:
            return jsonify({"result": res})


if __name__ == "__main__":
    CA = API()
    CA.run_app()

# 예제 나중에 지우기
'''
    qna_db = DBFuncs()
    row = qna_db.get_question_list()
    if row != -1:
        for i in row:
            print(i['question'])

    count = qna_db.question_count()
    if count != -1:
        print(count[0]['count'])

    res = qna_db.add_answer('답변 벡터값에 대한 벡터 분류로 구분합니다.')
    if res == -1:
        print('insert error')
    else:
        res = qna_db.add_question('유사한 질문은 어떻게 구분하나요?', res)

    res = qna_db.modify_pt(1, -1)
    if res != -1:
        row = qna_db.get_question_list()
        if row != -1:
            for i in row:
                print(i['l_pt'])

    res = qna_db.get_answer(2)
    print(res)
    
    # curl -i -H "Content-Type: application/json" -X POST -d "{\"question\":\"Rest API \uD14C\uC2A4\uD2B8\",\"answer\":\"REST API \uD14C\uC2A4\uD2B8\"}" http://localhost:5000/plugin/AQA
'''