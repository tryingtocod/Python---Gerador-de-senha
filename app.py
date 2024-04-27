from flask import Flask, render_template, request
import random
import string

app = Flask(__name__, template_folder='templates')

def gerar_senha(comprimento):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    senha = ''.join(random.choice(caracteres) for i in range(comprimento))
    return senha

@app.route('/')
def index():
    return render_template('index.html', senha="")

@app.route('/gerar_senha', methods=['POST'])
def gerar_senha_route():
    comprimento = int(request.form['comprimento'])
    senha = gerar_senha(comprimento)
    return render_template('index.html', senha=senha)

if __name__ == '__main__':
    app.run(debug=True)
