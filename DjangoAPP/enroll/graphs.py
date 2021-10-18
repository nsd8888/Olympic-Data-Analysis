

from io import BytesIO
import base64
import matplotlib.pyplot as plt
import seaborn as sns

def get_graph(x):
    plt.switch_backend('AGG')
    plt.figure(figsize=(12,10))
    sns.set(font_scale=0.5)
    sns.heatmap(x,cmap='Blues',annot=True)
    buffer=BytesIO()
    plt.savefig(buffer,format='png')
    buffer.seek(0)
    image_png=buffer.getvalue()
    graph=base64.b64encode(image_png)
    graph=graph.decode('utf-8')
    buffer.close()
    return graph
