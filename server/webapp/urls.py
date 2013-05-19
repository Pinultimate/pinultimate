from django.conf.urls import patterns, url

urlpatterns = patterns('webapp.views',
    url(r'map.html', 'index'),
    url(r'feedback.html', 'feedback_html'),
    url(r'resources/KMeans.js', 'kmeans_js'),
    url(r'resources/style.css', 'style_css'),
    url(r'resources/sampleData.js', 'sample_data_js'),
    url(r'resources/time_slider.js', 'time_slider_js'),
    url(r'resources/data.js', 'data_js'),
    url(r'resources/map.js', 'map_js'),
    url(r'resources/white_wall_hash.png', 'white_wall_hash_png'),
    url(r'resources/PauseButton.jpeg', 'pause_button_jpeg'),
    url(r'resources/PlayButton.jpeg', 'play_button_jpeg'),
)
