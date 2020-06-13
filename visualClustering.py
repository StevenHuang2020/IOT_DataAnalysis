import matplotlib.pyplot as plt
from matplotlib import cm
from sklearn.manifold import TSNE
from modelCreate import createKMeans,createAgglomerate,createDBSCAN
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.metrics import silhouette_score,silhouette_samples
import numpy as np

from plotApplication import gRes

def visualClusterResult(data, labels, bestK, title):
    print('data.shape=',data.shape,'labels.shape=',labels.shape,'bestK=',bestK)
    #Y = tsne(data, 2, 10, 50,max_iter=500)
    Y = TSNE(n_components=2, verbose=0, perplexity=50, n_iter=1000).fit_transform(data)#data.values

    plt.title(title)
    plt.scatter(Y[:, 0], Y[:, 1], 20, labels) #marker='s',edgecolor='black'
    plt.savefig(gRes+title+'.png')
    plt.show()
    
def plotSilhouetteValues(datasetName,modelName,k, X, y_km):
    if k<=1:
        return
    
    ax = plt.subplot(1,1,1)
    title = datasetName+ '_' + modelName + '_CSM_k=' +str(k)
    plt.title(title)
    
    cluster_labels = np.unique(y_km)
    n_clusters = cluster_labels.shape[0]
    
    print('cluster_labels=',cluster_labels,',n_clusters=',n_clusters)
    
    
    silhouette_vals = silhouette_samples(X, y_km, metric='euclidean')
    y_ax_lower, y_ax_upper = 0, 0
    yticks = []
    for i, c in enumerate(cluster_labels):
        c_silhouette_vals = silhouette_vals[y_km == c]
        c_silhouette_vals.sort()
        
        y_ax_upper += len(c_silhouette_vals)
        color = cm.jet(float(i) / n_clusters)
        plt.barh(range(y_ax_lower, y_ax_upper), c_silhouette_vals, height=1.0, 
                edgecolor='none', color=color)

        yticks.append((y_ax_lower + y_ax_upper) / 2.)
        y_ax_lower += len(c_silhouette_vals)
        
    silhouette_avg = np.mean(silhouette_vals)
    plt.axvline(silhouette_avg, color="red", linestyle="--") 

    plt.yticks(yticks, cluster_labels + 1)
    plt.ylabel('Cluster')
    plt.xlabel('Silhouette coefficient')

    plt.tight_layout()
    plt.savefig(gRes+title+'.png')
    plt.show()

def main():
    pass
    
if __name__=='__main__':
    main()