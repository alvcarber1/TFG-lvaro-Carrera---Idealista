import pytest
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
import joblib
import os

class TestClusteringAnalysis:
    """Tests basados en el notebook clustering_analysis.ipynb"""
    
    @pytest.fixture
    def sample_data(self):
        """Crear datos de muestra para testing"""
        np.random.seed(42)
        return pd.DataFrame({
            'latitude': np.random.uniform(40.3, 40.6, 100),
            'longitude': np.random.uniform(-3.9, -3.5, 100),
            'sq_mt_built': np.random.uniform(50, 300, 100),
            'n_rooms': np.random.randint(1, 6, 100),
            'n_bathrooms': np.random.randint(1, 4, 100),
            'buy_price': np.random.uniform(200000, 1000000, 100),
            'rent_price': np.random.uniform(800, 3000, 100)
        })
    
    def test_data_preprocessing(self, sample_data):
        """Test del preprocesamiento de datos"""
        # Verificar columnas requeridas
        required_columns = ['latitude', 'longitude', 'sq_mt_built', 'n_rooms', 'n_bathrooms', 'buy_price', 'rent_price']
        
        for col in required_columns:
            assert col in sample_data.columns, f"Missing required column: {col}"
        
        # Test manejo de valores faltantes
        df_with_nulls = sample_data.copy()
        df_with_nulls.loc[0:5, 'buy_price'] = np.nan
        
        df_filled = df_with_nulls.fillna(df_with_nulls.median())
        assert not df_filled.isnull().any().any(), "Should not have null values after filling"
        
        print("✓ Data preprocessing test passed")

    def test_clustering_pipeline(self, sample_data):
        """Test del pipeline completo de clustering"""
        # Preprocesar datos
        clustering_df = sample_data.copy()
        clustering_df = clustering_df.fillna(clustering_df.median())
        
        # Normalizar
        scaler = StandardScaler()
        clustering_df_scaled = scaler.fit_transform(clustering_df)
        
        # K-means
        kmeans = KMeans(n_clusters=5, random_state=42)
        labels_kmeans = kmeans.fit_predict(clustering_df_scaled)
        
        # Verificar resultados
        assert len(set(labels_kmeans)) <= 5, "K-means should create at most 5 clusters"
        assert len(labels_kmeans) == len(sample_data), "Should have label for each data point"
        
        # Calcular silhouette score
        score = silhouette_score(clustering_df_scaled, labels_kmeans)
        assert score > 0, f"Silhouette score should be positive, got {score}"
        
        print(f"✓ K-means clustering test passed. Silhouette score: {score:.3f}")

    def test_anomaly_detection(self, sample_data):
        """Test detección de anomalías con Isolation Forest"""
        # Preparar datos
        features = ['buy_price', 'sq_mt_built', 'n_rooms', 'n_bathrooms']
        df_features = sample_data[features].fillna(sample_data[features].median())
        
        # Normalizar
        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(df_features)
        
        # Isolation Forest
        iso_forest = IsolationForest(contamination=0.05, random_state=42)
        anomaly_labels = iso_forest.fit_predict(df_scaled)
        
        # Verificar resultados
        n_anomalies = sum(anomaly_labels == -1)
        anomaly_ratio = n_anomalies / len(anomaly_labels)
        
        assert 0.01 <= anomaly_ratio <= 0.15, f"Anomaly ratio should be 1-15%, got {anomaly_ratio:.2%}"
        
        print(f"✓ Anomaly detection test passed. Anomalies: {anomaly_ratio:.1%}")

    def test_pca_reduction(self, sample_data):
        """Test reducción de dimensionalidad con PCA"""
        # Preprocesar
        clustering_df = sample_data.fillna(sample_data.median())
        scaler = StandardScaler()
        clustering_df_scaled = scaler.fit_transform(clustering_df)
        
        # PCA
        pca = PCA(n_components=2)
        df_pca = pca.fit_transform(clustering_df_scaled)
        
        # Verificar resultados
        assert df_pca.shape[1] == 2, "PCA should reduce to 2 components"
        assert df_pca.shape[0] == len(sample_data), "Should preserve number of samples"
        
        # Verificar varianza explicada
        total_variance = sum(pca.explained_variance_ratio_)
        assert total_variance > 0.3, f"PCA should explain >30% variance, got {total_variance:.2%}"
        
        print(f"✓ PCA test passed. Variance explained: {total_variance:.2%}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])