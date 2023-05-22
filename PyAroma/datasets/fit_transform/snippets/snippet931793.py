
from sklearn.decomposition import NMF
model = NMF(n_components=6)
model.fit(articles)
nmf_features = model.transform(articles)
print(nmf_features)
import pandas as pd
df = pd.DataFrame(nmf_features, index=titles)
print(df.loc['Anne Hathaway'])
print(df.loc['Denzel Washington'])
import pandas as pd
components_df = pd.DataFrame(model.components_, columns=words)
print(components_df.shape)
from matplotlib import pyplot as plt
digit = samples[(0, :)]
print(digit)
bitmap = digit.reshape(13, 8)
print(bitmap)
plt.imshow(bitmap, cmap='gray', interpolation='nearest')
plt.colorbar()
plt.show()
from sklearn.decomposition import NMF
model = NMF(n_components=7)
features = model.fit_transform(samples)
for component in model.components_:
    show_as_image(component)
digit_features = features[(0, :)]
print(digit_features)
from sklearn.decomposition import PCA
model = PCA(n_components=7)
features = model.fit_transform(samples)
for component in model.components_:
    show_as_image(component)
import pandas as pd
from sklearn.preprocessing import normalize
norm_features = normalize(nmf_features)
df = pd.DataFrame(norm_features, index=titles)
article = df.loc['Cristiano Ronaldo']
similarities = df.dot(article)
print(similarities.nlargest())
from sklearn.decomposition import NMF
from sklearn.preprocessing import Normalizer, MaxAbsScaler
from sklearn.pipeline import make_pipeline
scaler = MaxAbsScaler()
nmf = NMF(n_components=20)
normalizer = Normalizer()
pipeline = make_pipeline(scaler, nmf, normalizer)
norm_features = pipeline.fit_transform(artists)
import pandas as pd
df = pd.DataFrame(norm_features, index=artist_names)
artist = df.loc[('Bruce Springsteen', :)]
similarities = df.dot(artist)
print(similarities.nlargest())
