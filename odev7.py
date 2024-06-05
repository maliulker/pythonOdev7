from flask import Flask, render_template_string, send_file
import numpy as np
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

name = "Muhammed Ali"
surname = "ULKER"
student_id = "211213"

def generate_points():
    MIN_VALUE = 0
    MAX_VALUE = 2000
    POINT_COUNT = 5000
    GRID_SIZE = 250
    GROUP_COUNT = MAX_VALUE // GRID_SIZE

    points = np.random.randint(MIN_VALUE, MAX_VALUE, size=(POINT_COUNT, 2))

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_title("Random Points Distribution", fontsize=16)
    ax.set_xlabel("X Coordinate")
    ax.set_xticks(np.arange(MIN_VALUE, MAX_VALUE + 1, GRID_SIZE))
    ax.set_xlim([MIN_VALUE, MAX_VALUE])
    ax.set_ylabel("Y Coordinate")
    ax.set_yticks(np.arange(MIN_VALUE, MAX_VALUE + 1, GRID_SIZE))
    ax.set_ylim([MIN_VALUE, MAX_VALUE])
    ax.grid(True)

    groups = [[[] for _ in range(GROUP_COUNT)] for _ in range(GROUP_COUNT)]
    for point in points:
        x, y = point
        x //= GRID_SIZE
        y //= GRID_SIZE
        groups[x][y].append(point)

    colors = np.random.rand(GROUP_COUNT, GROUP_COUNT, 3)
    for x in range(GROUP_COUNT):
        for y in range(GROUP_COUNT):
            for point in groups[x][y]:
                ax.scatter(point[0], point[1], color=colors[x][y], s=10, alpha=0.75)

    output = io.BytesIO()
    plt.savefig(output, format='png')
    plt.close(fig)
    output.seek(0)

    return output

@app.route('/')
def index():
    return render_template_string('''
        <html>
            <head>
                <title>Ödev 7</title>
            </head>
            <body>
                <h1>{{ name }} {{ surname }} - {{ student_id }}</h1>
                <img src="/plot.png" alt="Plot">
                <form action="/refresh" method="post">
                    <button type="submit">Yenile</button>
                </form>
            </body>
        </html>
    ''', name=name, surname=surname, student_id=student_id)

@app.route('/plot.png')
def plot_png():
    output = generate_points()
    return send_file(output, mimetype='image/png')

@app.route('/refresh', methods=['POST'])
def refresh():
    return index()

if __name__ == "__main__":
    app.run(debug=True)
