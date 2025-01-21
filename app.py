from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def mm2_queue_calculation(lam, mu):
    rho = lam / (2 * mu)
    if rho >= 1:
        return {"error": "Sistem tidak stabil (\u03c1 >= 1)."}

    Wq = (lam ** 2) / (2 * mu * (2 * mu - lam))
    W = 1 / (mu - lam / 2)

    return {
        "lam": lam,
        "mu": mu,
        "\u03c1": rho,
        "Wq": Wq,
        "W": W
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            lam = float(request.form['lam'])
            mu = float(request.form['mu'])

            if lam <= 0 or mu <= 0:
                error_message = "Tingkat kedatangan (λ) dan tingkat layanan (μ) harus lebih besar dari 0."
                return render_template('index.html', error_message=error_message)

            result = mm2_queue_calculation(lam, mu)
            return render_template('result.html', result=result)
        except ValueError:
            error_message = "Masukkan angka yang valid untuk λ dan μ."
            return render_template('index.html', error_message=error_message)

    return render_template('index.html', result=None, error_message=None)

@app.route('/result', methods=['POST'])
def result_page():
    try:
        # Ambil nilai input dari form
        waktu_antar_kedatangan = float(request.form['waktu_antar_kedatangan'])
        waktu_pelayanan = float(request.form['waktu_pelayanan'])

        # Validasi input
        if waktu_antar_kedatangan <= 0 or waktu_pelayanan <= 0:
            return render_template('result.html', error_message="Waktu antar kedatangan dan waktu pelayanan harus lebih besar dari 0.")

        # Perhitungan parameter
        lambda_val = 1 / waktu_antar_kedatangan
        mu = 1 / waktu_pelayanan

        # Validasi kestabilan sistem
        if mu <= lambda_val / 2:
            return render_template('result.html', error_message="Sistem tidak stabil (\u03bc \u2264 \u03bb/2).")

        # Perhitungan parameter lainnya
        rho = lambda_val / (2 * mu)
        W = 1 / (mu - lambda_val / 2)
        Wq = lambda_val / (2 * mu * (mu - lambda_val / 2))

        # Mengembalikan hasil perhitungan
        result = {
            "lambda": lambda_val,
            "mu": mu,
            "rho": rho,
            "W": W,
            "Wq": Wq
        }
        return render_template('result.html', result=result)
    except ValueError:
        return render_template('result.html', error_message="Masukkan nilai yang valid.")

if __name__ == '__main__':
    app.run(debug=True)
