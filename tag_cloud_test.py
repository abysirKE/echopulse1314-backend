import matplotlib.pyplot as plt
from wordcloud import WordCloud

tag_cloud = [
    {"tag": "harambee", "count": 2},
    {"tag": "jua kali", "count": 1},
    {"tag": "matatu", "count": 1}
]

def render_tag_cloud(tag_cloud):
    freq = {item["tag"]: item["count"] for item in tag_cloud}
    wc = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate_from_frequencies(freq)

    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig("tag_cloud.png", format="png")
    plt.show()

render_tag_cloud(tag_cloud)
