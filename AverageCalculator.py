import requests
from flask import Flask, jsonify
from random import randint

app = Flask(__name__)


def generate_primes(n):
    primes = []
    for num in range(2, n + 1):
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                break
        else:
            primes.append(num)
    return primes


def generate_fibonacci(n):
    fib = [0, 1]
    while True:
        next_fib = fib[-1] + fib[-2]
        if next_fib > n:
            break
        fib.append(next_fib)
    return fib


def generate_even(n):
    return list(range(2, n + 1, 2))


def generate_random(n):
    return [random.randint(1, 100) for _ in range(n)]


def fetch_numbers_from_test_server():
    try:

        response = requests.get("http://20.244.56.144/numbers")
        response.raise_for_status()
        return response.json()['numbers']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []


@app.route('/test/primes')
def primes():

    primes_list = generate_primes(100)
    return jsonify({'numbers': primes_list})


@app.route('/test/fibo')
def fibonacci():

    fib_list = generate_fibonacci(100)
    return jsonify({'numbers': fib_list})


@app.route('/test/even')
def even():

    even_list = generate_even(100)
    return jsonify({'numbers': even_list})


@app.route('/test/rand')
def random():
    rand_list = generate_random(10)
    return jsonify({'numbers': rand_list})


@app.route('/test/test_server_numbers')
def test_server_numbers():
    numbers = fetch_numbers_from_test_server()
    return jsonify({'numbers': numbers})


if __name__ == '__main__':
    app.run(debug=True)
