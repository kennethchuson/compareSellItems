from flask import Flask, render_template, url_for, request, redirect
import openpyxl

app = Flask(__name__)

workbook = openpyxl.load_workbook("storage/storage_one.xlsx")


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        result_enter = request.form['content'] 
        print(result_enter) 

    return render_template('index.html')


if __name__ == '__main__':
   app.run()