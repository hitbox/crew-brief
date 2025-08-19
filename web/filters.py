def short_number(n):
    n = abs(n)

    units = 'BMK'
    divisors = reversed([1_000 ** i for i in range(1, 4)])

    for unit, divisor in zip(units, divisors):
        if n >= divisor:
            return f'{n / divisor:.1f}{unit}'

    return str(n)

def init_app(app):
    app.jinja_env.filters['short_number'] = short_number
